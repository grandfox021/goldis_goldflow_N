from sys import exception
from urllib import response
from fastapi import FastAPI,HTTPException,Response,Request,Depends
from httpx import get
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import random
from models import background_secret_updater,Users_Orm,Asset_Orm,WithdrawalRequests_Orm,Tickets_Orm,Transaction_Orm
import logging
import asyncio
from contextlib import asynccontextmanager
import datetime
from typing import Dict,List,Any
from fastapi.security import OAuth2PasswordBearer
from  logics.payment_logics import rial_deposit,gold_buy,gold_sell,rial_withdraw
import jwt
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
import uuid
from schemas import *
import requests
from fastapi import FastAPI, Form, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from decimal import Decimal
import jdatetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend




load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

otp_store = {}

# In-memory storage

failed_login_attempts: Dict[str, Dict] = {}    
MAX_LOGIN_ATTEMPTS = 5
LOGIN_COOLDOWN_PERIOD = datetime.timedelta(minutes=1)  # Cooldown duration
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# IdP Server URLs
IDP_URL = "http://127.0.0.1:8000"
IDP_PUBLIC_KEY_URL = f"{IDP_URL}/public-key"
IDP_LOGIN_URL = f"{IDP_URL}/login-with-phone"

# Load environment variables from .env file
load_dotenv()

# Read values from .env
PUBLIC_KEY_FILE = os.getenv("PUBLIC_KEY_FILE", "public.pem")


IDP_PUBLIC_KEY = None  # Cached in-memory key



# Store user sessions and refresh tokens (temporary storage)
stored_users = {}  # {user_id: user_info}
stored_refresh_tokens = {}  # {refresh_token: user_id}


def fetch_and_store_public_key():
    """Fetch and convert the IdP's public key to PKCS#8 format before storing it."""
    global IDP_PUBLIC_KEY

    try:
        response = requests.get(IDP_PUBLIC_KEY_URL, timeout=5)
        response.raise_for_status()
        raw_public_key = response.json().get("public_key")

        if not raw_public_key:
            raise HTTPException(status_code=500, detail="Invalid response: No public key received")

        # Convert the key to PKCS#8 format
        public_key_obj = serialization.load_pem_public_key(raw_public_key.encode(), backend=default_backend())
        converted_key = public_key_obj.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

        # Save the new key to the PEM file
        with open(PUBLIC_KEY_FILE, "w") as file:
            file.write(converted_key)
        IDP_PUBLIC_KEY = converted_key  # Update in-memory cache
        return IDP_PUBLIC_KEY

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch IdP public key: {str(e)}")


def get_idp_public_key():
    """Retrieve the IdP's public key, checking first in the PEM file, then requesting if needed."""
    global IDP_PUBLIC_KEY

    # Check if the key is already cached in memory
    if IDP_PUBLIC_KEY is not None:
        return IDP_PUBLIC_KEY

    # Check if the public.pem file exists
    if os.path.exists(PUBLIC_KEY_FILE):
        with open(PUBLIC_KEY_FILE, "r") as file:
            IDP_PUBLIC_KEY = file.read().strip()

        # If the file exists but is empty, fetch a new key
        if not IDP_PUBLIC_KEY:
            return fetch_and_store_public_key()
        
        return IDP_PUBLIC_KEY

    # If the file does not exist, fetch the key and create the file
    return fetch_and_store_public_key()


def verify_jwt_token(token: str):
    """Verify JWT using IdP's public key. If signature error occurs, fetch a new key and retry."""
    global IDP_PUBLIC_KEY

    try:
        public_key = get_idp_public_key()
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
        return decoded_token  # Successfully decoded token

    except jwt.ExpiredSignatureError:
        print("🚨 Token has expired!")
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError as e:
        print(f"🚨 Invalid Token Error: {e}")

        # Fetch a new key and retry
        IDP_PUBLIC_KEY = fetch_and_store_public_key()
        print("🔄 Refetched Public Key:", IDP_PUBLIC_KEY)

        try:
            decoded_token = jwt.decode(token, IDP_PUBLIC_KEY, algorithms=["RS256"])
            print(f"✅ Decoded token after key refresh: {decoded_token}")
            return decoded_token

        except jwt.InvalidTokenError as e:
            print(f"🚨 Still Invalid after key refresh: {e}")
            raise HTTPException(status_code=401, detail="Invalid token, even after fetching a new public key")


# Add middleware to FastAPI app

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    task_update_secret_key = asyncio.create_task(background_secret_updater())
    try:
        yield  # application running
    finally:
        task_update_secret_key.cancel()
        await task_update_secret_key  

app = FastAPI(lifespan=lifespan)


def generate_random_otp() -> str:
    """Generate a random 4-digit OTP"""
    return str(random.randint(1000, 9999))

class RateLimitExceeded(Exception):
    def __init__(self, remaining_time: datetime.timedelta):
        self.remaining_time = remaining_time


def generate_random_national_id():
    """Generate a random 10-digit national ID"""
    return str(random.randint(1000000000, 9999999999))


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to check JWT token from cookies and allow public routes."""
    
    async def dispatch(self, request: Request, call_next):
        # ✅ Allow unauthenticated access to these routes
        public_paths = {"/callback", "/update-user-info", "/auth/callback","/set-cookie-for-backend","/get-gold-current-price"}

        # ✅ Print full request info for debugging
        # print("\n🔹🔹🔹 Incoming Request Details 🔹🔹🔹")
        # print(f"➡️ URL: {request.url}")
        # print(f"➡️ Method: {request.method}")
        # print(f"➡️ Headers: {dict(request.headers)}")  # Convert headers to dictionary
        # print(f"➡️ Cookies: {request.cookies}")  # Print all cookies
        # print(f"➡️ Query Params: {request.query_params}")  # Print query params

        # 🔹 Read and print the request body safely
        
        if request.method == "OPTIONS" :
            
            pass
        else:
            body = await request.body()
            # print(f"➡️ Body: {body.decode('utf-8')}" if body else "➡️ Body: No body")
            token = request.cookies.get("access_token")
            # print(f"➡️token : {token}")
            # ✅ Skip token check for public paths
            if request.url.path in public_paths:
                return await call_next(request)

            # 🔹 Check for access token in cookies



            if not token:
                print("🚨 No token found in cookies! ****")
                return JSONResponse(
                    status_code=401,
                    content={"error": "No token in cookies"}
                )

            if not verify_jwt_token(token):
                print("🚨 Invalid token!")
                return JSONResponse(
                    status_code=401,
                    content={"error": "Invalid or missing access token"}
                )

            return await call_next(request)
        return await call_next(request)


# Add middleware to FastAPI app
# app.add_middleware(JWTAuthMiddleware)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, session_cookie="session_id")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9000","http://localhost:9000/","http://localhost:9005","http://127.0.0.1:9000","http://127.0.0.1:9005","http://127.0.0.1:8000","http://localhost:8000",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/auth/callback")
async def callback(response: Response, request: Request):
    """
    ✅ Receives authentication data from IdP frontend as JSON.
    ✅ Stores user data & sets access token in cookies.
    """
    try:
        data = await request.json()
        print("🔹 Received authentication data:", data)

        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        user_info = data.get("user")
        if not access_token or not user_info:
            raise HTTPException(status_code=400, detail="Missing authentication data")

        user_id = user_info["sso_unique_id"]
        print(f"✅ Access Token: {access_token[:5]}..., User: {user_id}")

        # ✅ Store user session & refresh token
        stored_users[user_id] = user_info
        if refresh_token:
            stored_refresh_tokens[refresh_token] = user_id

        # ✅ Set the access token in cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,              # Use False for HTTP on localhost
            max_age=3600 * 72,
            samesite="None",            # "Lax" or "Strict" works better for non-HTTPS; "None" requires secure
                     # Optional: ensures the cookie is set for localhost
        )


        print("✅ Successfully stored user session & set cookies")
        
        print(user_info)
        asyncio.create_task(update_or_create_user_from_callback(user_info)) 
        
        
        return {"success": True}

        
    except Exception as e:
        print("🚨 Callback error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing callback: {str(e)}")
    
    
    
async def update_or_create_user_from_callback(user_info: dict):
    """
    ✅ Updates an existing user or creates a new one using Users_Orm.
    """
    try:
        sso_unique_id = user_info.get("sso_unique_id")
        first_name = user_info.get("firstname", "")
        last_name = user_info.get("lastname", "")
        email = user_info.get("email", "")
        phone_number = user_info.get("phone_number", "")
        national_id = user_info.get("national_id", "")
        # user_type = user_info.get("user_type", Users_Orm.Types.customer.value)  # Default to customer if not provided
        password = user_info.get("password", "")
        
        # 🔹 Check if the user already exists by email
        existing_user = Users_Orm.get_user_by_sso_unique_id(sso_unique_id) or Users_Orm.get_user_by_email(email) or Users_Orm.get_user_by_phone_number(phone_number) or Users_Orm.get_user_by_id(national_id)

        if existing_user:
            # 🔹 Update the existing user
            update_fields = {
                "first_name": first_name or existing_user["first_name"],
                "last_name": last_name or existing_user["last_name"],
                "email": email or existing_user["email"],
                "phone_number": phone_number or existing_user["phone_number"],
                "national_id": national_id or existing_user["national_id"],
                # "user_type": user_type or existing_user["user_type"],
                "password": password or existing_user["password"],
                
            }
            Users_Orm.update_user(sso_unique_id, **update_fields)
            print(f"✅ User {sso_unique_id} updated successfully.")
        else:
            # 🔹 Create a new user only if email, phone, and national_id are unique
            Users_Orm.create_user(
                sso_unique_id=sso_unique_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                national_id=national_id,
                password=password,  # Default empty password (since it's coming from SSO)
                user_type=Users_Orm.Types.customer.value,
            )
            print(f"🆕 New user {sso_unique_id} created successfully.")

    except Exception as e:
        print(f"🚨 Error in update_or_create_user: {str(e)}")

    
@app.get("/home")
def home():
    
    return {"data" :  "hello from hassan"}


@app.post("/register-user")
def register_user(data: UserCreate):
    """Register a new user"""
    try:
        # Check if phone number already exists
        existing_user = Users_Orm.get_user_by_phone_number(data.phone_number)
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number already registered")

        # # Check if email already exists
        # existing_email = Users_Orm.get_user_by_email(data.email)  # Implement this in Users_Orm
        # if existing_email:
        #     raise HTTPException(status_code=400, detail="Email already registered")

        # Generate random national ID (ensure this function exists)
        national_id = generate_random_national_id()

        # Hash the password before saving
        hashed_password =data.password

        # Create new user
        result = Users_Orm.create_user(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone_number=data.phone_number,
            national_id=national_id,
            password=hashed_password,
            user_type=4  # Default user type (e.g., Guest)
        )

        if result:
            return {"message": "User registered successfully", "user_id": result["user_id"]}
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")

    except HTTPException as http_err:
        logger.error(f"HTTP Exception: {http_err.detail}")
        raise http_err  # Re-raise HTTP exceptions for proper handling

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

    
    
# Reusable Dependency to Protect Routes
def get_current_user_with_session(request: Request):
    """Dependency function to check if the user is authenticated."""
    user_id = request.session.get("user_id")
    user = Users_Orm.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized: Please log in")
    
    return user  # Return the user ID for further use    


def get_current_user(request: Request):
    """
    Dependency that verifies the JWT token in cookies, extracts the sso_unique_id,
    and returns the corresponding user from the database.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="No access token provided")

    token_payload = verify_jwt_token(access_token)
    if not token_payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    sso_unique_id = token_payload.get("sub")
    if not sso_unique_id:
        raise HTTPException(status_code=401, detail="Token missing sso_unique_id")

    # Fetch the user from the database using the sso_unique_id
    user = Users_Orm.get_user_by_sso_unique_id(sso_unique_id)
    
    if user : 
        sso_unique_id = user["sso_unique_id"]
    else:
        raise HTTPException(status_code=404, detail="User not found")

    return user  # Return the full user record for further use


@app.post("/login")
async def authenticate_user_with_phone_number(data: OTPRequest, request: Request, response: Response):
    try:
        phone_number = data.phone_number

        # Attempt authentication
        try:
            user = Users_Orm.get_user_by_phone_number(phone_number)
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Authentication service unavailable"
            )

        if not user:
            raise HTTPException(status_code=401, detail="Invalid phone number")

        # Store user session (Set session cookie)
        request.session["user_id"] = user["id"]
        request.session["phone_number"] = user["phone_number"]
        request.session["is_authenticated"] = True

        return {"success": True, "message": "Login successful", "user_id": user["id"]}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in verify_user: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred"
        )
           
    
# Logout Route
@app.post("/logout")
async def logout(response: Response, request: Request):
    """Logs out the user by clearing the session and removing authentication cookies."""
    request.session.clear()  # Clear session data

    # Delete the access token cookie
    response.delete_cookie("access_token", httponly=True, secure=True, samesite="None")

    return {"success": True, "message": "Logged out successfully"}

    
@app.post("/rial-deposit")
def rial_deposit_route(data: RialDepositRequest, user: dict = Depends(get_current_user)):
    """Route for processing Rial deposits (new or existing transactions)"""

    user_id = user["id"]
    try:
            transaction_id = rial_deposit(
            buyer_user_id=user_id,
            seller_user_id=1,  # Assuming seller is always user ID 1
            rial_amount=data.rial_amount,
            payment_fee=0,
            goldis_fee=0,
            description="request_data.description",
            transaction_id= data.transaction_id if data.transaction_id else None,
            payment_provider_type= 1,
            payment_ref_id=f"{uuid.uuid4()}",
            create_datetime=None,
            invoice_id=None,
            bank_card_id=data.banck_card_number if data.banck_card_number else None,
            asset_id=None
        )
    except HTTPException as e:
            raise e

        # return {"message": "Rial deposit processed successfully", "transaction_id": transaction_id}
        #-----------------------------------------the process is instant for now---------------------------------------
        
    print(f"🆕 transaction rial_deposi initiated successfully id : {transaction_id}")
    try : 
        transaction_id = rial_deposit(transaction_id=transaction_id)  
        print(F"🆕 transaction rial_deposi finished successfully by id {id}")
            
        return{"success":True, "msg": f"rial_deposit transaction successfully processed for user {user["first_name"]} {user['last_name']} by id : {user["sso_unique_id"]}"}
    except HTTPException as e:
        raise e
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/gold-buy")
def gold_buy_route(data : GoldBuyRequest, user: dict = Depends(get_current_user)):
    """
    API Route for processing gold buy transactions.
    """
    user_id = user["id"] 
    print(f"the user in gold buy is {user_id}")
    
    print(f"gold amount is {type(data.gold_amount)}")
    try:
            transaction_id = gold_buy(
            buyer_user_id=user_id,
            seller_user_id=1,  # Assuming seller is a fixed entity (like a marketplace)
            # buy_price=data.buy_price,
            gold_amount=data.gold_amount,
            rial_amount=data.final_price,
            current_price = data.current_price,
            goldis_fee=data.goldis_fee,
            payment_ref_id= f"{uuid.uuid4()}",
            description="gold buy transaction",
        )
    except Exception as e :
        raise e

    print(f"transaction gold deposit initiated successfully with id :{transaction_id}")
    try : 
        transaction_id = gold_buy(transaction_id=transaction_id)   
        print(f"transaction gold deposit finished successfully with id :{transaction_id}")
        
        return{"success":True, "msg": f"gold_buy transaction successfully processed for user {user["first_name"]} {user['last_name']} by id : {user["sso_unique_id"]}"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    
    
@app.post("/gold-sell")
def gold_sell_route(data: GoldSellRequest, user: dict = Depends(get_current_user)):
    """
    API Route for processing gold sell transactions.
    """
    user_id = user["id"]
    
    try:
        # ✅ Step 1: Initialize the transaction
        transaction_id = gold_sell(
            seller_user_id=user_id,
            buyer_user_id=1,  # Assuming the buyer is always marketplace or fixed ID
            gold_amount=data.gold_amount,
            current_price=data.current_price,
            goldis_fee=data.goldis_fee,
            rial_amount=data.final_price,
            payment_ref_id=f"{uuid.uuid4()}",
            description="Gold Sell Transaction"
        )

        if not transaction_id:
            raise HTTPException(status_code=500, detail="Failed to initialize gold sell transaction")

        print(f"🆕 Gold sell transaction initiated successfully, ID: {transaction_id}")

        # ✅ Step 2: Process the transaction in database
        transaction_id = gold_sell(transaction_id=transaction_id)  

        print(f"✅ Gold sell transaction completed successfully, ID: {transaction_id}")

        return {
            "success": True,
            "message": f"Gold sell transaction processed for user {user['first_name']} {user['last_name']} (ID: {user['sso_unique_id']})"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
@app.post("/finish-rial-deposit")
def rial_deposit_route(data: FinishRialTransaction, user_id: int = Depends(get_current_user)):
    """process the transaction for rial deposit once initilized"""
    transaction_id = data.transaction_id
    asset_id = data.asset_id
    updated_transaction = rial_deposit(transaction_id=transaction_id,asset_id=asset_id)
    return {"message": "Rial deposit trnasaction successfully finished", "transaction_id": updated_transaction}


def serialize_user(user):
    """Convert datetime and Decimal fields to JSON-friendly formats"""
    return {
        "id": user["id"],
        "sso_unique_id": user["sso_unique_id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "national_id": user["national_id"],
        "phone_number": user["phone_number"],
        "card_number": user["card_number"],
        "user_type": user["user_type"],
        "created_at": user["created_at"].isoformat() if isinstance(user["created_at"], datetime.datetime) else user["created_at"],
        "updated_at": user["updated_at"].isoformat() if isinstance(user["updated_at"], datetime.datetime) else user["updated_at"],
        "rial_balance": float(user["rial_balance"]) if isinstance(user["rial_balance"], Decimal) else user["rial_balance"],
        "gold_balance": float(user["gold_balance"]) if isinstance(user["gold_balance"], Decimal) else user["gold_balance"],
    }

@app.get("/get-user-info")
def get_user_info(request: Request, user: dict = Depends(get_current_user)):
    print("✅get_user_info called")
    access_token = request.cookies.get("access_token")   
    print(access_token)
    
    token = verify_jwt_token(access_token)
    sso_unique_id = token["sub"]
    user = Users_Orm.get_user_by_sso_unique_id(sso_unique_id)

    print(f"✅user in get userinfo: {user}")


    # Convert problematic fields before sending response
    serialized_user = serialize_user(user)

    print(f"serialize_user in get userinfo: {serialized_user}")

    return {"success": True, "user_info":serialized_user}


@app.get("/get-gold-current-price")
def view_gold_current_price():
    
    try:
        gold_current_price = Asset_Orm.get_asset_by_code("GOLD").get("current_price_per_gram")    
    except exception as e :
        raise e
    return{"gold_current_price":gold_current_price,"success" :True}
    

@app.post("/post-card-number")
def update_card_number(data: CardNumberRequest, current_user: dict = Depends(get_current_user)):
    """
    ✅ Updates or sets the card number for the authenticated user.
    """
    user_sso_unique_id = current_user["sso_unique_id"]
    
    if not data.card_number or len(data.card_number) != 16:
        raise HTTPException(status_code=400, detail="Invalid card number. Must be exactly 16 digits.")
    
    result = Users_Orm.update_user(user_sso_unique_id, card_number=data.card_number)
    
    if result:
        return {"message": "✅ Card number updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update card number")


@app.get("/get-card-number")
def get_card_number(current_user: dict = Depends(get_current_user)):
    """
    ✅ Retrieves the card number for the authenticated user.
    """
    user_id = current_user["id"]
    user = Users_Orm.get_user_by_id(user_id)

    if not user or not user.get("card_number"):
        raise HTTPException(status_code=404, detail="⚠ Card number not found")

    return {"card_number": user["card_number"]}


@app.delete("/delete-card-number")
def delete_card_number(current_user: dict = Depends(get_current_user)):
    """
    ✅ Removes the stored card number for the authenticated user.
    """
    user_sso_unique_id = current_user["sso_unique_id"]
    result = Users_Orm.update_user(user_sso_unique_id, card_number=None)

    if result:
        return {"message": "✅ Card number removed successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete card number")

 
@app.post("/create-withdrawl-request")
def create_withdrawal_request(request : Request,data: WithdrawalRequestCreate, user: dict = Depends(get_current_user)):
    """
    ✅ Submit a new withdrawal request
    """
    print(f"request body is in create-withdrawl-request : {request.body}")
    
    user_id = user["id"]
    user_phone_number = user["phone_number"]
    if data.amount<1 :
        raise HTTPException(status_code=400, detail="invalid amount for withdrawl")   
    
    if user["card_number"] == None :
          raise HTTPException(status_code=400, detail="user does not have a valid card number")      
    else :
        user_banck_card = user["card_number"] 
        
    # Ensure user has enough balance
    current_balance = Users_Orm.get_user_by_id(user_id)["rial_balance"]
    if current_balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    
    result = WithdrawalRequests_Orm.create_withdrawal_request(
        user_id=user_id,
        user_phone_number = user_phone_number,
        status=WithdrawalRequests_Orm.Status.pending.value,
        amount=data.amount,
        bank_name="sep",
        card_number= user_banck_card
    )
    
    if result:
        return {"success": True, "message": "Withdrawal request submitted successfully", "request_id": result}
    else:
        raise HTTPException(status_code=500, detail="Failed to submit withdrawal request")



@app.get("/get-withdrawl-requests") 
def get_withdrawal_requests_route(user: dict = Depends(get_current_user)):
    """
    ✅ Retrieve all withdrawal requests (Admin only) with Shamsi dates, full names, and status mapping.
    """
    
    # ✅ Define status mapping
    STATUS_MAPPING = {
        0: "pending",
        1: "approved",
        2: "rejected",
        3: "processing",
        4: "completed"
    }
    
    if user["user_type"] not in [1, 2]:  # Only admin & superuser
        raise HTTPException(status_code=403, detail="Unauthorized")

    withdrawal_requests = WithdrawalRequests_Orm.get_withdrawal_requests_with_joining_users()
    
    if not withdrawal_requests:
        return {"message": "No withdrawal requests found"}

    # ✅ Convert Gregorian to Shamsi and return full details with mapped status
    formatted_requests = []
    for request in withdrawal_requests:
        formatted_requests.append({
            "id": request["id"],
            "user_id": request["user_id"],
            "full_name": f"{request['first_name']} {request['last_name']}",
            "user_phone_number": request["user_phone_number"],
            "amount": request["amount"],
            "status": STATUS_MAPPING.get(request["status"], "Unknown"),  # ✅ Map status
            "admin_id": request["admin_id"],
            "bank_name": request["bank_name"],
            "card_number": request["card_number"],
            "created_at": jdatetime.datetime.fromgregorian(datetime=request["created_at"]).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": jdatetime.datetime.fromgregorian(datetime=request["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
        })
    
    
    print("request : ", formatted_requests)  
    return {"success":True ,"withdrawal_requests": formatted_requests}

@app.patch("/update-withdrawal-request/{request_id}")
def update_withdrawal_status(request_id: int, data: WithdrawalRequestUpdate, user: dict = Depends(get_current_user)):
    """
    ✅ Admin approves or declines a withdrawal request.
    """

    if user["user_type"] not in [1, 2]:  # Only admin & superuser can approve
        raise HTTPException(status_code=403, detail="Unauthorized")

    request_details = WithdrawalRequests_Orm.get_withdrawl_request_by_id(request_id)
    if not request_details:
        raise HTTPException(status_code=404, detail="Withdrawal request not found")

    if request_details["status"] != WithdrawalRequests_Orm.Status.pending.value:
        raise HTTPException(status_code=400, detail="Request is already processed")

    

    # if data.status == WithdrawalRequests_Orm.Status.approved.value:  # Admin Approves
    if data.status == "approve" :
        try:
            print(f"✅ Admin approved withdrawal request for user: {request_details['user_id']}")

            # ✅ Step 1: Update Withdrawal Status to 'Processing'
            WithdrawalRequests_Orm.update_withdrawal_status(withdrawal_id=request_id,admin_id=user["id"], status=WithdrawalRequests_Orm.Status.processing.value)

            # ✅ Step 2: Create a Rial Withdraw Transaction
            error, transaction_id = rial_withdraw(
                seller_user_id=request_details["user_id"],
                rial_amount=request_details["amount"],
                description="Admin approved withdrawal request"
            )

            if error:
                raise HTTPException(status_code=500, detail=f"Failed to create withdrawal transaction: {error}")

            print(f"🆕 Rial withdrawal transaction created: {transaction_id}")

            # ✅ Step 3: Process the Rial Withdrawal Transaction
            error, processed_transaction_id = Users_Orm.rial_withdraw_transaction(transaction_id)
            
            if error:
                raise HTTPException(status_code=500, detail=f"Failed to process withdrawal transaction: {error}")
            
            print(f"✅ Rial withdrawal transaction completed: {processed_transaction_id}")

            # ✅ Step 4: Mark the Withdrawal Request as 'Completed'
            WithdrawalRequests_Orm.update_withdrawal_status(withdrawal_id=request_id,admin_id=user["id"],status= WithdrawalRequests_Orm.Status.completed.value)

            return {
                "success": True,
                "message": f"Withdrawal request processed successfully for user {request_details['user_id']}",
                "transaction_id": processed_transaction_id
            }

        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"🚨 Unexpected error in withdrawal process: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    else:  # Admin Declines the Request
        print(f"⚠️ Admin declined withdrawal request {request_id}")
        WithdrawalRequests_Orm.update_withdrawal_status(withdrawal_id=request_id,admin_id=user["id"],status=WithdrawalRequests_Orm.Status.rejected.value)
        return {"success": True, "message": "Withdrawal request declined"}


@app.post("/create-ticket-with-message")
def create_ticket_with_message(data: TicketCreateWithMessage, user: dict = Depends(get_current_user_with_session)):
    """
    ✅ API Route to create a ticket and add the first message.
    """
    ticket_id = Tickets_Orm.create_ticket_with_message(
        user_id=user["id"],
        subject=data.subject,
        status=Tickets_Orm.Status.OPEN.value,
        message=data.message,
        priority=1
    )

    if not ticket_id:
        raise HTTPException(status_code=500, detail="Failed to create ticket")

    return {"success": True, "message": "Ticket created successfully!", "ticket_id": ticket_id}


# ✅ Create a New Ticket
@app.post("/create-ticket")
def create_ticket(data: TicketCreate, user: dict = Depends(get_current_user_with_session)):
    ticket_id = Tickets_Orm.create_ticket(user_id=user["id"],status = Tickets_Orm.Status.OPEN.value , subject=data.subject, priority=data.priority)
    if not ticket_id:
        raise HTTPException(status_code=500, detail="Failed to create ticket")
    return {"success": True, "message": "Ticket created successfully", "ticket_id": ticket_id}

# ✅ Get Tickets for User/Admin
@app.get("/get-tickets")
def get_tickets(user: dict = Depends(get_current_user_with_session)):
    tickets = Tickets_Orm.get_tickets(user_id=user["id"], admin_view=(user["user_type"] in [1, 2]))
    if tickets is None:
        raise HTTPException(status_code=500, detail="Error fetching tickets")
    return {"success": True, "tickets": tickets}

# ✅ Update Ticket Status (Admin Only)
@app.patch("/update-ticket/{ticket_id}")
def update_ticket(ticket_id: int, status: int, user: dict = Depends(get_current_user_with_session)):
    if user["user_type"] not in [1, 2]:  # Only Admin
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    result = Tickets_Orm.update_ticket_status(ticket_id, status)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to update ticket")
    return {"success": True, "message": "Ticket updated successfully"}

# ✅ Add Message to Ticket
@app.post("/add-ticket-message")
def add_ticket_message(data: TicketMessageCreate, user: dict = Depends(get_current_user_with_session)):
    message_id = Tickets_Orm.add_ticket_message_for_user(ticket_id=data.ticket_id, sender_id=user["id"],user_type=user["user_type"], message=data.message)
    if not message_id:
        raise HTTPException(status_code=500, detail="Failed to send message")
    return {"success": True, "message": "Message sent successfully"}

# ✅ Get Ticket Messages
@app.get("/get-ticket-messages/{ticket_id}")
def get_ticket_messages(ticket_id: int, user: dict = Depends(get_current_user_with_session)):
    messages = Tickets_Orm.get_ticket_messages(ticket_id)
    if messages is None:
        raise HTTPException(status_code=500, detail="Error fetching messages")
    return {"success": True, "messages": messages}


@app.get("/get-transactions-by-user/{user_id}", response_model=List[Dict])
def get_transactions_by_user(user_id: int):
    transactions = Transaction_Orm.get_transactions_by_user(user_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this user")

    # Extract all unique buyer and seller IDs
    user_ids = set(tx["buyer_id"] for tx in transactions) | set(tx["seller_id"] for tx in transactions)

    # Fetch user details in one efficient query
    users = Users_Orm.get_users_by_ids(user_ids)

    # Create a mapping of user_id to full name, replacing "gold vault vault" with "گلدیس" immediately
    user_mapping = {
        user["id"]: (
            "گلدیس"
            if user["id"] == 1 or (user["first_name"].lower() == "gold vault" and user["last_name"].lower() == "vault")
            else f"{user['first_name']} {user['last_name']}"
        )
        for user in users
    }

    # Format transactions efficiently
    formatted_transactions = [
        {
            **tx,
            "buyer_name": user_mapping.get(tx["buyer_id"], "نامشخص"),
            "seller_name": user_mapping.get(tx["seller_id"], "نامشخص"),
            "rial_amount": float(tx["rial_amount"]),
            "gold_amount": float(tx["gold_amount"]),
            "asset_price_at_transaction_time": float(tx["asset_price_at_transaction_time"]),
            "buyer_rial_balance": float(tx["buyer_rial_balance"]),
            "buyer_gold_balance": float(tx["buyer_gold_balance"]),
            "seller_rial_balance": float(tx["seller_rial_balance"]),
            "seller_gold_balance": float(tx["seller_gold_balance"]),
            "goldis_fee": float(tx["goldis_fee"]),
            "payment_fee": float(tx["payment_fee"]),
            "create_datetime": tx["create_datetime"].isoformat() if "create_datetime" in tx else None,
            "last_update_datetime": tx["last_update_datetime"].isoformat() if "last_update_datetime" in tx else None,
        }
        for tx in transactions
    ]

    return formatted_transactions


@app.get("/get-all-transactions", response_model=Dict[str, Any])
def get_all_transactions(user = Depends(get_current_user)):
    
    
    if user["user_type"] not in [1, 2]:  # Only admin & superuser can approve
        raise HTTPException(status_code=403, detail="Unauthorized")    
    
    transactions = Transaction_Orm.get_all_transactions()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")

    # Extract all unique buyer and seller IDs
    user_ids = {tx["buyer_id"] for tx in transactions} | {tx["seller_id"] for tx in transactions}

    # Fetch user details in one efficient query
    users = Users_Orm.get_users_by_ids(user_ids)

    # Create a mapping of user_id to full name, replacing "gold vault vault" with "گلدیس"
    user_mapping = {
        user["id"]: "گلدیس" if user["id"] == 1 or (user["first_name"].lower() == "gold vault" and user["last_name"].lower() == "vault")
        else f"{user['first_name']} {user['last_name']}"
        for user in users
    }

    # Helper function to safely convert values to float
    def to_float(value):
        return float(value) if value is not None else 0.0

    # Format transactions efficiently
    formatted_transactions = [
        {
            **tx,
            "buyer_name": user_mapping.get(tx["buyer_id"], "نامشخص"),
            "seller_name": user_mapping.get(tx["seller_id"], "نامشخص"),
            "rial_amount": to_float(tx.get("rial_amount")),
            "gold_amount": to_float(tx.get("gold_amount")),
            "asset_price_at_transaction_time": to_float(tx.get("asset_price_at_transaction_time")),
            "buyer_rial_balance": to_float(tx.get("buyer_rial_balance")),
            "buyer_gold_balance": to_float(tx.get("buyer_gold_balance")),
            "seller_rial_balance": to_float(tx.get("seller_rial_balance")),
            "seller_gold_balance": to_float(tx.get("seller_gold_balance")),
            "goldis_fee": to_float(tx.get("goldis_fee")),
            "payment_fee": to_float(tx.get("payment_fee")),
            "create_datetime": tx.get("create_datetime").isoformat() if tx.get("create_datetime") else None,
            "last_update_datetime": tx.get("last_update_datetime").isoformat() if tx.get("last_update_datetime") else None,
        }
        for tx in transactions
    ]

    return {"success" : True , "transactions" : formatted_transactions}      


@app.get("/get-withdrawl-requests-for-user/{user_id}")
def get_withddrawl_requests_for_user(user_id):
    
    # ✅ Define status mapping
    STATUS_MAPPING = {
        0: "pending",
        1: "approved",
        2: "rejected",
        3: "processing",
        4: "completed"
    }
    
    user_withdralw_requests = WithdrawalRequests_Orm.get_withdrawal_requests_by_user_id_with_joining_user(user_id)
    
    formatted_requests = []
    for request in user_withdralw_requests:
        formatted_requests.append({
            "id": request["id"],
            "user_id": request["user_id"],
            "full_name": f"{request['first_name']} {request['last_name']}",
            "user_phone_number": request["user_phone_number"],
            "amount": request["amount"],
            "status": STATUS_MAPPING.get(request["status"], "Unknown"),  # ✅ Map status
            "admin_id": request["admin_id"],
            "bank_name": request["bank_name"],
            "card_number": request["card_number"],
            "created_at": jdatetime.datetime.fromgregorian(datetime=request["created_at"]).strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": jdatetime.datetime.fromgregorian(datetime=request["updated_at"]).strftime("%Y-%m-%d %H:%M:%S")
        })
    
    print("request : ", formatted_requests)  
    return {"success":True ,"withdrawal_requests": formatted_requests}
    
      
@app.get("/protected-with-session")
async def protected_route(user_id: int = Depends(get_current_user)):
    """A protected route that only authenticated users can access."""
    return {"message": f"Welcome, User {user_id}! You have access to this protected route."}


@app.get("/protected-route-with-token")
def protected_endpoint(current_user: Users_Orm = Depends(get_current_user)):
    return {"message": "You have access!", "user with sso_unique_id ": current_user}


# ---------------- PROTECTED ROUTE For Vue Checking----------------
@app.get("/protected-resource")
async def protected_route(request: Request):
    """A protected route that requires a valid JWT in cookies."""
    # print(current_user)
    return {"authenticated": True ,"message": "You have access!" }


if __name__ == "__main__":
    uvicorn.run(app, port=8080)



