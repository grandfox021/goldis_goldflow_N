from mysql.connector import pooling, Error
from passlib.context import CryptContext
from dotenv import load_dotenv,set_key
import asyncio
import datetime
import hashlib
import aiofiles
import os
import secrets
# from jose import jwt
import logging
import jdatetime
import enum
# import time
# import uuid
from fastapi import HTTPException
from typing import List
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Goldis123456!",
    "database": "gold_flow",
}

# Create a Connection Pool
try:
    db_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,  # Number of connections in the pool
        **DB_CONFIG
    )
    print(" Connection pool created successfully!")
except Error as err:
    print(f" Error creating connection pool: {err}")


def get_db_connection():
    """Get a connection from the pool"""
    try:
        connection = db_pool.get_connection()
        print(" Connection obtained from pool")
        return connection
    except Error as err:
        print(f" Error getting connection: {err}")
        return None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    
    #returns the hashed password
    return pwd_context.hash(password)

print(generate_password_hash("Goldisvault123456!"))


def verify_password(password: str, hashed_password: str) -> bool:
    
    #returns the bool from checking password
    return pwd_context.verify(password, hashed_password)


load_dotenv()

ENV_FILE = ".env"


async def generate_daily_secret() -> str:
    """Generate a new secret key once per day."""
    today = datetime.date.today().isoformat()  # Get today's date as a string
    random_bytes = secrets.token_bytes(64)  # Generate 64 random bytes
    daily_secret = hashlib.sha256((today + random_bytes.hex()).encode()).hexdigest()  # Hash the combination
    return daily_secret


async def get_or_update_secret() -> None:
    """
    Ensure SECRET_KEY is present in .env and updates it if the date has changed.
    """
    # Create .env file if it does not exist
    if not os.path.exists(ENV_FILE):
        async with aiofiles.open(ENV_FILE, mode="w") as f:
            await f.write("")  # Create an empty .env file

    load_dotenv()  # Load existing environment variables

    old_secret_key = os.getenv("SECRET_KEY")

    # Generate new secret key
    new_secret_key = await generate_daily_secret()

    if old_secret_key != new_secret_key:

        # Write to .env file (async & atomic)
        async with aiofiles.open(ENV_FILE, mode="w") as f:
            await f.write(f"SECRET_KEY={new_secret_key}\n")

        # Also update the current process environment
        set_key(ENV_FILE, "SECRET_KEY", new_secret_key)


async def background_secret_updater():
    """
    Periodically updates secret key.
    """
    while True:
        await get_or_update_secret()
        await asyncio.sleep(21600)  # Check prices every 6 hours
        
    
    

class Users_Orm:
    @staticmethod
    def get_all_users():
        """Fetch all users from the database"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users;")
                users = cursor.fetchall()
                return users
            except Error as err:
                print(f"Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")
                

    @staticmethod
    def get_user_by_phone_number(phone_number):
        """Fetch a user by phone number"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE phone_number = %s"
                cursor.execute(query, (phone_number,)) 
                user = cursor.fetchone()
                return user
            except Error as err:
                print(f" Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")
                
    @staticmethod
    def get_user_by_id(id):
        """Fetch a user by phone number"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE id = %s"
                cursor.execute(query, (id,)) 
                user = cursor.fetchone()
                return user
            except Error as err:
                print(f" Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")
                

    @staticmethod
    def get_user_by_id_for_transaction(id):
        """Fetch a user by phone number"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE id = %s"
                cursor.execute(query, (id,)) 
                user = cursor.fetchone()
                return user
            except Error as err:
                print(f" Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")


    @staticmethod
    def get_user_by_sso_unique_id(sso_unique_id):
        """Fetch a user by sso_unique_id"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE sso_unique_id = %s"
                cursor.execute(query, (sso_unique_id,)) 
                user = cursor.fetchone()
                return user
            except Error as err:
                print(f" Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")


    @staticmethod
    def get_user_by_type(type):
        """Fetch a user by phone number"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE user_type = %s"
                cursor.execute(query, (type,)) 
                user = cursor.fetchone()
                return user
            except Error as err:
                print(f" Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")
                
                
    @staticmethod
    def get_user_by_email(email):
        """Fetch a user by phone number"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE email = %s"
                cursor.execute(query, (email,)) 
                user = cursor.fetchone()
                return user
            except Error as err:
                print(f" Query Error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()  # Return connection to pool
                print(" Connection returned to pool")
                


    @staticmethod
    def create_user(sso_unique_id,first_name, last_name, email, phone_number, national_id, password, user_type):
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """
                INSERT INTO users (sso_unique_id, first_name, last_name, email, phone_number, national_id, password, user_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                # hashed_password = generate_password_hash(password)
                values = (sso_unique_id, first_name, last_name, email, phone_number, national_id, password, user_type)
                cursor.execute(sql, values)
                connection.commit()
                return {"message": "User created successfully", "user_id": cursor.lastrowid}
            except Error as err:
                connection.rollback()
                logger.error(f"Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()
                

    @staticmethod
    def update_user(sso_unique_id, **kwargs):
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # 🔹 Fetch the current user data
                existing_user = Users_Orm.get_user_by_sso_unique_id(sso_unique_id)
                if not existing_user:
                    return {"message": "User not found"}

                # 🔹 Remove fields that have the same value (prevent duplicate entry error)
                filtered_fields = {key: value for key, value in kwargs.items() if existing_user.get(key) != value}
                
                if not filtered_fields:
                    print("✅ No changes detected, skipping update.")
                    return {"message": "No changes detected"}

                # 🔹 Construct the update query dynamically
                update_parts = ", ".join([f"{key} = %s" for key in filtered_fields.keys()])
                sql = f"UPDATE users SET {update_parts} WHERE sso_unique_id = %s"
                values = tuple(filtered_fields.values()) + (sso_unique_id,)

                cursor.execute(sql, values)
                connection.commit()
                return {"message": "User updated successfully"} if cursor.rowcount > 0 else {"message": "No changes made"}

            except Error as err:
                connection.rollback()
                print(f"🚨 Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()
                

    @staticmethod
    def update_card_number(user_id, new_card_number):
        """Update user's full card number"""
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "UPDATE users SET card_number = %s WHERE id = %s"
                    values = (new_card_number, user_id)
                    cursor.execute(sql, values)
                    connection.commit()

                    return {"message": "✅ Card number updated successfully"} if cursor.rowcount > 0 else {"message": "⚠ No changes made"}
            except Error as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                connection.close()

    @staticmethod
    def get_card_number(user_id):
        """Retrieve user's full card number"""
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor(dictionary=True) as cursor:
                    sql = "SELECT card_number FROM users WHERE id = %s"
                    cursor.execute(sql, (user_id,))
                    result = cursor.fetchone()

                    return result if result else {"message": "⚠ Card number not found"}
            except Error as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                connection.close()

    @staticmethod
    def delete_card_number(user_id):
        """Remove stored card number for a user"""
        connection = get_db_connection()
        if connection:
            try:
                with connection.cursor() as cursor:
                    sql = "UPDATE users SET card_number = NULL WHERE id = %s"
                    cursor.execute(sql, (user_id,))
                    connection.commit()

                    return {"message": "✅ Card number removed successfully"} if cursor.rowcount > 0 else {"message": "⚠ No changes made"}
            except Error as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                connection.close()
            
                
    @staticmethod
    def update_user_rial_balance(phone_number,updated_rial_balance):
        connection = get_db_connection()
        if connection :
            try :
                cursor = connection.cursor()
                sql = """
                        update users set_rial_balance = %s where phone_number = %s for update
                """
                                
                values = (updated_rial_balance , phone_number)
                
                
                cursor.execute(sql, values)
                connection.commit()

                return {"message": "user_rial_balnace updated successfully", "log_id": cursor.lastrowid}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()
                print(" Connection returned to pool")
                
            
            
    @staticmethod                   
    def deposit_rial_transaction(transaction_id):
        """Processes the rial deposit transaction by updating user balances safely"""
        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")

        try:
            cursor = connection.cursor(dictionary=True)
            connection.start_transaction()

            # Fetch and lock transaction row
            cursor.execute("SELECT * FROM transactions WHERE id = %s FOR UPDATE", (transaction_id,))
            transaction = cursor.fetchone()
            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            # Ensure transaction is still pending
            if transaction['status'] != Transaction_Orm.Status.pending.value:
                raise HTTPException(status_code=400, detail="Transaction already processed")

            # Fetch and lock seller's balance
            cursor.execute("SELECT id, rial_balance FROM users WHERE id = %s FOR UPDATE", (transaction['seller_id'],))
            seller = cursor.fetchone()

            # Fetch and lock buyer's balance
            cursor.execute("SELECT id, rial_balance FROM users WHERE id = %s FOR UPDATE", (transaction['buyer_id'],))
            buyer = cursor.fetchone()

            if not seller or not buyer:
                raise HTTPException(status_code=400, detail="Invalid buyer or seller")

            # Calculate net rial amount after fees
            rial_amount = transaction['rial_amount'] - transaction['goldis_fee'] - transaction['payment_fee']

            # Ensure seller has enough rial balance
            if seller['rial_balance'] < rial_amount:
                raise HTTPException(status_code=400, detail="Seller does not have enough balance")

            # Deduct from seller's rial balance
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance - %s WHERE id = %s",
                (rial_amount, seller['id'])
            )

            # Add to buyer's rial balance
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance + %s WHERE id = %s",
                (rial_amount, buyer['id'])
            )

            # Mark transaction as successful
            successful_value = Transaction_Orm.Status.successful.value
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (successful_value, transaction_id)
            )

            connection.commit()
            return transaction_id
        
        except HTTPException as e:
            connection.rollback()
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (Transaction_Orm.Status.failed.value, transaction_id)
            )
            connection.commit()
            logger.error(f"Transaction error: {e.detail}")
            raise e
        except Exception as e:
            connection.rollback()
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (Transaction_Orm.Status.failed.value, transaction_id)
            )
            connection.commit()
            logger.error(f"Unexpected error in deposit_rial_transaction: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            connection.close()

    @staticmethod        
    def gold_buy_transaction(transaction_id):
        """Processes a gold buy transaction by updating user balances and gold holdings safely."""
        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")

        try:
            cursor = connection.cursor(dictionary=True)
            connection.start_transaction()

            # Fetch and lock transaction row
            cursor.execute("SELECT * FROM transactions WHERE id = %s FOR UPDATE", (transaction_id,))
            transaction = cursor.fetchone()
            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            # Fetch and lock buyer's balance
            cursor.execute("SELECT id, rial_balance, gold_balance FROM users WHERE id = %s FOR UPDATE", (transaction['buyer_id'],))
            buyer = cursor.fetchone()

            # Fetch and lock seller's balance
            cursor.execute("SELECT id, rial_balance, gold_balance FROM users WHERE id = %s FOR UPDATE", (transaction['seller_id'],))
            seller = cursor.fetchone()

            if not seller or not buyer:
                raise HTTPException(status_code=400, detail="Invalid buyer or seller")

            # Ensure transaction is still pending
            if transaction['status'] != Transaction_Orm.Status.pending.value:
                raise HTTPException(status_code=400, detail="Transaction already processed")

            total_rial_cost = transaction['rial_amount']
            gold_amount = transaction['gold_amount']

            # Ensure buyer has enough rial balance
            if buyer['rial_balance'] < total_rial_cost:
                raise HTTPException(status_code=400, detail="Buyer does not have enough rial balance")

            # Ensure seller has enough gold balance
            if seller['gold_balance'] < gold_amount:
                raise HTTPException(status_code=400, detail="Seller does not have enough gold balance")

            # Deduct Rial from buyer's balance
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance - %s WHERE id = %s",
                (total_rial_cost, buyer['id'])
            )

            # Add Rial to seller's balance
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance + %s WHERE id = %s",
                (total_rial_cost, seller['id'])
            )

            # Deduct Gold from seller's balance
            cursor.execute(
                "UPDATE users SET gold_balance = gold_balance - %s WHERE id = %s",
                (gold_amount, seller['id'])
            )

            # Add Gold to buyer's balance
            cursor.execute(
                "UPDATE users SET gold_balance = gold_balance + %s WHERE id = %s",
                (gold_amount, buyer['id'])
            )

            # Mark transaction as successful
            successful_value = Transaction_Orm.Status.successful.value
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (successful_value, transaction_id)
            )

            connection.commit()
            return transaction_id
        
        except HTTPException as e:
            connection.rollback()
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (Transaction_Orm.Status.failed.value, transaction_id)
            )
            connection.commit()
            logger.error(f"Transaction error: {e.detail}")
            raise e
        except Exception as e:
            connection.rollback()
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (Transaction_Orm.Status.failed.value, transaction_id)
            )
            connection.commit()
            logger.error(f"Unexpected error in gold_buy_transaction: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_users_by_ids(user_ids: List[int]):
        """
        ✅ Fetch multiple users in one query for efficiency.
        """
        if not user_ids:
            return []

        connection = get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)

            # ✅ Query users efficiently using IN clause
            query = "SELECT id, first_name, last_name FROM users WHERE id IN ({})".format(
                ",".join(["%s"] * len(user_ids))
            )
            cursor.execute(query, tuple(user_ids))
            users = cursor.fetchall()
            
            return users

        except Error as err:
            logger.error(f"❌ Database error in get_users_by_ids: {err}")
            return []

        finally:
            cursor.close()
            connection.close()  
            
                          
    @staticmethod
    def gold_sell_transaction(transaction_id):
        """Processes a gold sell transaction by updating user balances safely."""
        connection = get_db_connection()
        if not connection:
            raise HTTPException(status_code=500, detail="Database connection error")

        try:
            cursor = connection.cursor(dictionary=True)
            connection.start_transaction()

            # Fetch and lock transaction row
            cursor.execute("SELECT * FROM transactions WHERE id = %s FOR UPDATE", (transaction_id,))
            transaction = cursor.fetchone()
            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            # Fetch and lock seller's balance
            cursor.execute("SELECT id, rial_balance, gold_balance FROM users WHERE id = %s FOR UPDATE", (transaction['seller_id'],))
            seller = cursor.fetchone()

            # Fetch and lock buyer's balance
            cursor.execute("SELECT id, rial_balance, gold_balance FROM users WHERE id = %s FOR UPDATE", (transaction['buyer_id'],))
            buyer = cursor.fetchone()

            if not seller or not buyer:
                raise HTTPException(status_code=400, detail="Invalid buyer or seller")

            # Ensure transaction is still pending
            if transaction['status'] != Transaction_Orm.Status.pending.value:
                raise HTTPException(status_code=400, detail="Transaction already processed")


            # - transaction['goldis_fee'] currently handled in frontend
            total_rial_value = transaction['rial_amount'] 

            # Ensure seller has enough gold balance
            if seller['gold_balance'] < transaction['gold_amount']:
                raise HTTPException(status_code=400, detail="Seller does not have enough gold balance")

            # Deduct Gold from the seller
            cursor.execute(
                "UPDATE users SET gold_balance = gold_balance - %s WHERE id = %s",
                (transaction['gold_amount'], seller['id'])
            )

            # Add Gold to the buyer
            cursor.execute(
                "UPDATE users SET gold_balance = gold_balance + %s WHERE id = %s",
                (transaction['gold_amount'], buyer['id'])
            )

            # Deduct Rial from buyer's balance
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance - %s WHERE id = %s",
                (total_rial_value, buyer['id'])
            )

            # Add Rial to the seller's balance
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance + %s WHERE id = %s",
                (total_rial_value, seller['id'])
            )

            # Mark transaction as successful
            successful_value = Transaction_Orm.Status.successful.value
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (successful_value, transaction_id)
            )

            connection.commit()
            return transaction_id
        
        except Exception as e:
            connection.rollback()
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (Transaction_Orm.Status.failed.value, transaction_id)
            )
            connection.commit()
            logger.error(f"Unexpected error in gold_sell_transaction: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            connection.close()



    @staticmethod
    def rial_withdraw_transaction(transaction_id):
        """Processes a Rial withdraw transaction by safely updating user & buyer balances."""

        connection = get_db_connection()
        if not connection:
            return "Database connection error", None

        try:
            cursor = connection.cursor(dictionary=True)
            connection.start_transaction()

            # ✅ Fetch and lock transaction row
            cursor.execute("SELECT * FROM transactions WHERE id = %s FOR UPDATE", (transaction_id,))
            transaction = cursor.fetchone()

            if not transaction:
                return "Transaction not found", None  # Ensure tuple return

            rial_amount = transaction['rial_amount']
            if rial_amount is None or rial_amount == 0:
                return "Invalid withdrawal amount", None

            # ✅ Fetch and lock the seller (User withdrawing Rial)
            cursor.execute("SELECT id, rial_balance FROM users WHERE id = %s FOR UPDATE", (transaction['seller_id'],))
            seller = cursor.fetchone()

            if not seller:
                return "Invalid seller", None

            # ✅ Fetch and lock the buyer (goldis_vault, the platform handling withdrawals)
            cursor.execute("SELECT id, rial_balance FROM users WHERE user_type = 3 FOR UPDATE")  # Goldis Vault
            buyer = cursor.fetchone()

            if not buyer:
                return "Goldis Vault (Buyer) not found", None

            # ✅ Ensure transaction is still pending
            if transaction['status'] != Transaction_Orm.Status.pending.value:
                return "Transaction already processed", None

            # ✅ Ensure seller has enough balance
            seller_balance = seller['rial_balance'] if seller['rial_balance'] is not None else 0
            if seller_balance < abs(rial_amount):
                return "Insufficient balance", None

            # ✅ Deduct Rial from Seller (User withdrawing money)
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance - %s WHERE id = %s",
                (abs(rial_amount), seller['id'])
            )

            # ✅ Add Rial to Buyer (Goldis Vault)
            cursor.execute(
                "UPDATE users SET rial_balance = rial_balance + %s WHERE id = %s",
                (abs(rial_amount), buyer['id'])
            )

            # ✅ Mark transaction as successful
            successful_value = Transaction_Orm.Status.successful.value
            cursor.execute(
                "UPDATE transactions SET status = %s WHERE id = %s",
                (successful_value, transaction_id)
            )

            connection.commit()
            return None, transaction_id  # Return transaction_id when successful

        except Error as err:
            connection.rollback()
            logger.error(f"❌ Database error: {err}")
            return str(err), None  # Always return tuple

        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_user_gold_balance(user_id):
        """Fetch user's gold balance by user ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT gold_balance FROM users WHERE id = %s"
                cursor.execute(query, (user_id,))
                user = cursor.fetchone()

                return user["gold_balance"] if user else None  # Return gold balance or None if user not found

            except Error as err:
                print(f"❌ Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()               
                
    class Types(enum.Enum):

        super_user = 1
        admin = 2
        system_user = 3
        customer = 4
        


class Log_Orm:
    @staticmethod
    def create_log(user_id, user_ip, user_agent, referer_url, request_method, full_request_query, request_duration, description, log_level):
        """Insert a new log entry into the database"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Convert Gregorian datetime to Shamsi
                shamsi_date = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                sql = """
                INSERT INTO logs (
                    create_datetime, shamsi_create_datetime, user_id, user_ip, user_agent, 
                    referer_url, request_method, full_request_query, request_duration, 
                    description, log_level
                ) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    shamsi_date, user_id, user_ip, user_agent, referer_url, 
                    request_method, full_request_query, request_duration, 
                    description, log_level
                )

                cursor.execute(sql, values)
                connection.commit()

                return {"message": "Log created successfully", "log_id": cursor.lastrowid}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()
                print(" Connection returned to pool")

    @staticmethod
    def get_log(log_id):
        """Retrieve a specific log entry by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                sql = "SELECT * FROM logs WHERE id = %s"
                cursor.execute(sql, (log_id,))
                log = cursor.fetchone()

                return log if log else {"message": "Log not found"}

            except Error as err:
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_logs(limit=100):
        """Retrieve all log entries (default limit = 100)"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                sql = "SELECT * FROM logs ORDER BY create_datetime DESC LIMIT %s"
                cursor.execute(sql, (limit,))
                logs = cursor.fetchall()

                return logs if logs else {"message": "No logs found"}

            except Error as err:
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def update_log(log_id, description, log_level):
        """Update an existing log entry"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                sql = """
                UPDATE logs 
                SET description = %s, log_level = %s 
                WHERE id = %s
                """
                values = (description, log_level, log_id)

                cursor.execute(sql, values)
                connection.commit()

                return {"message": "Log updated successfully"} if cursor.rowcount > 0 else {"message": "Log not found"}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_log(log_id):
        """Delete a log entry by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                sql = "DELETE FROM logs WHERE id = %s"
                cursor.execute(sql, (log_id,))
                connection.commit()

                return {"message": "Log deleted successfully"} if cursor.rowcount > 0 else {"message": "Log not found"}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()
                
                
class Transaction_Orm:
    
    
    @staticmethod
    def create_transaction(
        user_id, sso_unique_id,asset_id, rial_amount, gold_amount, transaction_type, status, 
        asset_price_at_transaction_time, description, buyer_rial_balance,
        buyer_gold_balance, seller_rial_balance, seller_gold_balance, 
        buyer_id, seller_id, goldis_fee, payment_fee, payment_provider_type, 
        payment_ref_id, 
        invoice_number=None, invoice_id=""
    ):
        """Insert a new transaction record"""
        connection = get_db_connection()
        if not connection:
            return None  

        try:
            cursor = connection.cursor()

            # Convert Gregorian datetime to Shamsi
            shamsi_date = jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql = """
            INSERT INTO transactions (
                user_id,sso_unique_id, asset_id, rial_amount, gold_amount, create_datetime, shamsi_create_datetime, 
                transaction_type, status, asset_price_at_transaction_time, description, 
                last_update_datetime, buyer_rial_balance, buyer_gold_balance, seller_rial_balance, 
                seller_gold_balance, buyer_id, seller_id, goldis_fee, payment_fee, 
                payment_provider_type, payment_ref_id, 
                invoice_number, invoice_id
            ) VALUES (
                %s, %s,%s, %s, %s, NOW(), %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            values = (
                user_id,sso_unique_id ,asset_id, rial_amount, gold_amount, shamsi_date, transaction_type, 
                status, asset_price_at_transaction_time, description, buyer_rial_balance, 
                buyer_gold_balance, seller_rial_balance, seller_gold_balance, buyer_id, 
                seller_id, goldis_fee, payment_fee, payment_provider_type, payment_ref_id, 
                invoice_number, invoice_id
            )

            cursor.execute(sql, values)
            connection.commit()

            return cursor.lastrowid  

        except Error as err:
            connection.rollback()
            print(f"Database error: {err}")
            return None  

        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_transaction_by_id(transaction_id):
        """Fetch transaction by ID"""
        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            sql = "SELECT * FROM transactions WHERE id = %s FOR UPDATE"
            cursor.execute(sql, (transaction_id,))
            return cursor.fetchone()

        except Error as err:
            print(f"Database error: {err}")
            return None

        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def get_transactions_by_user(user_id, limit=100):
        """Retrieve transactions filtered by user_id"""
        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            sql = "SELECT * FROM transactions WHERE user_id = %s ORDER BY create_datetime DESC LIMIT %s"
            cursor.execute(sql, (user_id, limit))
            transactions = cursor.fetchall()

            return transactions if transactions else {"message": "No transactions found for this user"}

        except Error as err:
            print(f"Database error: {err}")
            return None

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_transactions(limit=100):
        """Retrieve all transactions (default limit = 100)"""
        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            sql = "SELECT * FROM transactions ORDER BY create_datetime DESC LIMIT %s"
            cursor.execute(sql, (limit,))
            transactions = cursor.fetchall()

            return transactions if transactions else {"message": "No transactions found"}

        except Error as err:
            print(f" Database error: {err}")
            return None

        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def update_transaction(transaction_id, status, description):
        """Update transaction status and description"""
        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()

            sql = """
            UPDATE transactions 
            SET status = %s, description = %s, last_update_datetime = NOW()
            WHERE id = %s
            """
            values = (status, description, transaction_id)

            cursor.execute(sql, values)
            connection.commit()

            return {"message": "Transaction updated successfully"} if cursor.rowcount > 0 else {"message": "Transaction not found"}

        except Error as err:
            connection.rollback()
            print(f" Database error: {err}")
            return None

        finally:
            cursor.close()
            connection.close()


    @staticmethod
    def delete_transaction(transaction_id):
        """Delete a transaction entry by ID"""
        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor()

            sql = "DELETE FROM transactions WHERE id = %s"
            cursor.execute(sql, (transaction_id,))
            connection.commit()

            return {"message": "Transaction deleted successfully"} if cursor.rowcount > 0 else {"message": "Transaction not found"}

        except Error as err:
            connection.rollback()
            print(f" Database error: {err}")
            return None

        finally:
            cursor.close()
            connection.close()


    # @staticmethod
    # def rial_deposit_transaction(transaction_id):
    #     """Processes the rial deposit transaction by updating user balances"""
    #     connection = get_db_connection()
    #     if not connection:
    #         return "Database connection error", None

    #     try:
    #         cursor = connection.cursor(dictionary=True)
    #         connection.start_transaction()

    #         transaction = Transaction_Orm.get_transaction_by_id(transaction_id)
    #         if not transaction:
    #             return "Transaction not found", None  

    #         seller = Users_Orm.get_user_by_id(transaction['seller_id'])
    #         buyer = Users_Orm.get_user_by_id(transaction['buyer_id'])

    #         if not seller or not buyer:
    #             return "Invalid buyer or seller", None

    #         if transaction['status'] != Transaction_Orm.Status.pending.value:
    #             return "Transaction already processed", None

    #         rial_amount = transaction['rial_amount'] - transaction['goldis_fee'] - transaction['payment_fee']

    #         if seller['rial_balance'] < rial_amount:
    #             return "Seller does not have enough balance", None

    #         cursor.execute(
    #             "UPDATE users SET rial_balance = rial_balance - %s WHERE id = %s",
    #             (rial_amount, seller['id'])
    #         )

    #         cursor.execute(
    #             "UPDATE users SET rial_balance = rial_balance + %s WHERE id = %s",
    #             (rial_amount, buyer['id'])
    #         )

    #         successful_value = Transaction_Orm.Status.successful.value
    #         cursor.execute(
    #             "UPDATE transactions SET status = %s WHERE id = %s",
    #             (successful_value, transaction_id)
    #         )

    #         connection.commit()
    #         return None, transaction_id

    #     except Error as err:
    #         connection.rollback()
    #         print(f"Database error: {err}")
    #         return str(err), None  

    #     finally:
    #         cursor.close()
    #         connection.close()

    class Status(enum.Enum):
        unknown = 1
        successful = 2
        failed = 3
        pending = 4
        expired = 5
        canceling = 6
        canceled = 7
        waiting_for_approval = 8
        scheduled_payment = 9
        scheduled_delivery = 10
        delivered = 11
        refund_pending = 12
        refunded = 13
        approved = 14
        accounting = 15
        approval_pending = 16


    class Types(enum.Enum):
        ipg_rial_deposit = 1
        admin_rial_deposit = 2
        rial_gift = 3
        rial_withdrawal = 4
        gold_buy = 5
        admin_gold_buy = 6
        gold_gift = 7
        gold_sell = 8
        gold_withdrawal = 9
        bank_rial_deposit = 10
        physical_gold_deposit = 11
        admin_gold_sell = 12

    class Payment_provider_types(enum.Enum):
        none = 1
        zarinpal_ipg = 2
        sepehr_ipg = 3
        third_party = 4
        cash = 5
        physical_bank_payment = 6


class Asset_Orm:
    @staticmethod
    def create_asset(title, code, unit_fa, image_path, description, buy_price, sell_price, 
                     total_buy_limit, total_sell_limit, daily_buy_limit_per_user, 
                     daily_sell_limit_per_user, total_balance):
        """Insert a new asset into the database"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                sql = """
                INSERT INTO assets (
                    title, code, unit_fa, image_path, description, buy_price, sell_price, 
                    total_buy_limit, total_sell_limit, daily_buy_limit_per_user, 
                    daily_sell_limit_per_user, total_balance
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (title, code, unit_fa, image_path, description, buy_price, 
                          sell_price, total_buy_limit, total_sell_limit, 
                          daily_buy_limit_per_user, daily_sell_limit_per_user, total_balance)

                cursor.execute(sql, values)
                connection.commit()

                return {"message": "Asset created successfully", "asset_id": cursor.lastrowid}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_asset_by_id(asset_id):
        """Retrieve a specific asset by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                sql = "SELECT * FROM assets WHERE id = %s"
                cursor.execute(sql, (asset_id,))
                asset = cursor.fetchone()

                return asset if asset else {"message": "Asset not found"}

            except Error as err:
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_asset_by_code(asset_code):
        """Retrieve a specific asset by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                sql = "SELECT * FROM assets WHERE code = %s"
                cursor.execute(sql, (asset_code,))
                asset = cursor.fetchone()

                return asset if asset else {"message": "Asset not found"}

            except Error as err:
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()


    @staticmethod
    def get_all_assets(limit=100):
        """Retrieve all assets (default limit = 100)"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)

                sql = "SELECT * FROM assets ORDER BY id ASC LIMIT %s"
                cursor.execute(sql, (limit,))
                assets = cursor.fetchall()

                return assets if assets else {"message": "No assets found"}

            except Error as err:
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def update_asset(asset_id, buy_price, sell_price, total_balance):
        """Update an asset's pricing and balance"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                sql = """
                UPDATE assets 
                SET buy_price = %s, sell_price = %s, total_balance = %s
                WHERE id = %s
                """
                values = (buy_price, sell_price, total_balance, asset_id)

                cursor.execute(sql, values)
                connection.commit()

                return {"message": "Asset updated successfully"} if cursor.rowcount > 0 else {"message": "Asset not found"}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_asset(asset_id):
        """Delete an asset by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()

                sql = "DELETE FROM assets WHERE id = %s"
                cursor.execute(sql, (asset_id,))
                connection.commit()

                return {"message": "Asset deleted successfully"} if cursor.rowcount > 0 else {"message": "Asset not found"}

            except Error as err:
                connection.rollback()
                print(f" Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()
                
class Invoice_Orm:
    @staticmethod
    def create_invoice(user_id, transaction_id, transaction_type, invoice_number, total_rial_amount, total_gold_amount, gold_price_at_transaction, status='pending'):
        """Insert a new invoice record into the database"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                sql = """
                INSERT INTO invoices 
                (user_id, transaction_id, transaction_type, invoice_number, total_rial_amount, total_gold_amount, gold_price_at_transaction, status, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                """
                
                values = (user_id, transaction_id, transaction_type, invoice_number, total_rial_amount, total_gold_amount, gold_price_at_transaction, status)

                cursor.execute(sql, values)
                connection.commit()

                return cursor.lastrowid  # ✅ Return the newly created invoice ID

            except Error as err:
                connection.rollback()
                print(f"Database error: {err}")
                return None  # Return None if creation fails

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_invoice_by_id(invoice_id):
        """Fetch invoice details by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM invoices WHERE id = %s"
                cursor.execute(sql, (invoice_id,))
                invoice = cursor.fetchone()
                return invoice if invoice else None  # Return None if not found

            except Error as err:
                print(f"Database error: {err}")
                return None

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_invoices(limit=100):
        """Retrieve all invoices (default limit = 100)"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM invoices ORDER BY created_at DESC LIMIT %s"
                cursor.execute(sql, (limit,))
                invoices = cursor.fetchall()
                return invoices if invoices else []

            except Error as err:
                print(f"Database error: {err}")
                return []

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def update_invoice_status(invoice_id, new_status):
        """Update invoice status"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "UPDATE invoices SET status = %s, updated_at = NOW() WHERE id = %s"
                values = (new_status, invoice_id)

                cursor.execute(sql, values)
                connection.commit()

                return cursor.rowcount > 0  # Returns True if an invoice was updated

            except Error as err:
                connection.rollback()
                print(f"Database error: {err}")
                return False  # Return False if update fails

            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def delete_invoice(invoice_id):
        """Delete an invoice by ID"""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "DELETE FROM invoices WHERE id = %s"
                cursor.execute(sql, (invoice_id,))
                connection.commit()

                return cursor.rowcount > 0  # Returns True if an invoice was deleted

            except Error as err:
                connection.rollback()
                print(f"Database error: {err}")
                return False  # Return False if deletion fails

            finally:
                cursor.close()
                connection.close()

class WithdrawalRequests_Orm:
    @staticmethod
    def create_withdrawal_request(user_id,user_phone_number,status, amount, bank_name, card_number):
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """
                INSERT INTO withdrawal_requests (user_id,user_phone_number, amount, status, bank_name, card_number, created_at, updated_at)
                VALUES (%s,%s, %s, %s, %s, %s, NOW(), NOW())
                """
                cursor.execute(sql, (user_id,user_phone_number, amount,status, bank_name, card_number))
                connection.commit()
                return cursor.lastrowid 
            except Error as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def update_withdrawal_status(withdrawal_id,admin_id, status):
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "UPDATE withdrawal_requests SET status = %s, admin_id = %s, updated_at = NOW() WHERE id = %s"
                cursor.execute(sql, (status,admin_id, withdrawal_id))
                connection.commit()
                return {"message": "✅ Withdrawal status updated successfully"}
            except Error as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_withdrawal_requests(limit=100):
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM withdrawal_requests ORDER BY created_at DESC LIMIT %s"
                cursor.execute(sql, (limit,))
                return cursor.fetchall()
            except Error as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_withdrawal_requests_with_joining_users(limit=100):
        """Fetches withdrawal requests with user full name in a single query."""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = """
                SELECT wr.*, 
                    u.first_name, 
                    u.last_name 
                FROM withdrawal_requests wr
                JOIN users u ON wr.user_id = u.id
                ORDER BY wr.created_at DESC 
                LIMIT %s
                """
                cursor.execute(sql, (limit,))
                return cursor.fetchall()
            except Error as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()


    @staticmethod
    def get_withdrawl_request_by_id(request_id):
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM withdrawal_requests WHERE id = %s"
                cursor.execute(sql, (request_id,))
                return cursor.fetchone()
            except Error as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    
    @staticmethod
    def get_withdrawal_requests_by_user_id(user_id, limit=100):
        """Fetches all withdrawal requests by user_id."""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM withdrawal_requests WHERE user_id = %s ORDER BY created_at DESC LIMIT %s"
                cursor.execute(sql, (user_id, limit))
                return cursor.fetchall()
            except Error as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()
                

    @staticmethod
    def get_withdrawal_requests_by_user_id_with_joining_user(user_id, limit=100):
        """Fetches all withdrawal requests by user_id."""
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = """SELECT wr.*, 
                        u.first_name, 
                        u.last_name 
                        FROM withdrawal_requests wr
                        JOIN users u ON wr.user_id = u.id
                        WHERE wr.user_id = %s
                        ORDER BY wr.created_at DESC 
                        LIMIT %s;
                    """
                cursor.execute(sql, (user_id, limit))
                return cursor.fetchall()
            except Error as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()
                            
                
    class Status(enum.Enum):
        pending = 0  # Corrected to match database
        approved = 1
        rejected = 2
        processing = 3
        completed = 4


class Tickets_Orm:

    @staticmethod
    def create_ticket(user_id,status, subject, priority=1):
        """
        Creates a new support ticket.
        """
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """
                INSERT INTO tickets (user_id, subject, priority, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """
                cursor.execute(sql, (user_id,subject, priority,status))
                connection.commit()
                return cursor.lastrowid  # Return ticket ID
            except Exception as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()


    @staticmethod
    def update_ticket_status(ticket_id, status):
        """
        Updates the status of a ticket.
        """
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "UPDATE tickets SET status = %s, updated_at = NOW() WHERE id = %s"
                cursor.execute(sql, (status, ticket_id))
                connection.commit()
                return True
            except Exception as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_tickets(user_id=None, admin_view=False):
        """
        Retrieves all tickets for a user or for an admin.
        """
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                if admin_view:
                    sql = "SELECT * FROM tickets ORDER BY created_at DESC"
                    cursor.execute(sql)
                else:
                    sql = "SELECT * FROM tickets WHERE user_id = %s ORDER BY created_at DESC"
                    cursor.execute(sql, (user_id,))
                return cursor.fetchall()
            except Exception as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def add_ticket_message(ticket_id, sender_id, message):
        """
        Adds a message to a ticket.
        """
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """
                INSERT INTO ticket_messages (ticket_id, sender_id, message, created_at)
                VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(sql, (ticket_id, sender_id, message))
                connection.commit()
                return cursor.lastrowid  # Return message ID
            except Exception as err:
                connection.rollback()
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def get_ticket_messages(ticket_id):
        """
        Retrieves all messages for a specific ticket.
        """
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM ticket_messages WHERE ticket_id = %s ORDER BY created_at ASC"
                cursor.execute(sql, (ticket_id,))
                return cursor.fetchall()
            except Exception as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()



    @staticmethod
    def create_ticket_with_message(user_id, subject, message,status, priority=1):
        """
        ✅ Creates a new support ticket and adds the first message.
        """
        connection = get_db_connection()
        if connection:
           
            try:
                cursor = connection.cursor()

                # ✅ Step 1: Insert Ticket
                sql_ticket = """
                INSERT INTO tickets (user_id, subject, priority, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, NOW(), NOW())
                """
                cursor.execute(sql_ticket, (user_id, subject, priority,status))
                ticket_id = cursor.lastrowid  # Get new ticket ID

                # ✅ Step 2: Insert First Message
                sql_message = """
                INSERT INTO ticket_messages (ticket_id, sender_id, message, created_at)
                VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(sql_message, (ticket_id, user_id, message))

                connection.commit()
                return ticket_id  # Return the created ticket ID

            except Exception as err:
                logger.error(f"❌ Database error: {err}")
                return None
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def add_ticket_message_for_user(ticket_id, sender_id, user_type, message):
        """
        ✅ Adds a message to a ticket.
        ✅ Users can only send a message if the last message was from an admin.
        ✅ Admins can send messages anytime.
        """

        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            # ✅ Step 1: Get Last Message Sender
            sql_last_message = """
            SELECT sender_id FROM ticket_messages WHERE ticket_id = %s ORDER BY created_at DESC LIMIT 1
            """
            cursor.execute(sql_last_message, (ticket_id,))
            last_message = cursor.fetchone()

            if last_message:
                last_sender_id = last_message["sender_id"]

                # ✅ Prevent User from Sending Consecutive Messages
                if user_type != "admin" and last_sender_id == sender_id:
                    return {"error": "Please wait for an admin response before sending another message."}

            # ✅ Step 2: Insert the Message
            sql_insert_message = """
            INSERT INTO ticket_messages (ticket_id, sender_id, message, created_at)
            VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(sql_insert_message, (ticket_id, sender_id, message))

            # ✅ Step 3: Update Ticket Last Updated Time
            sql_update_ticket = "UPDATE tickets SET updated_at = NOW() WHERE id = %s"
            cursor.execute(sql_update_ticket, (ticket_id,))

            connection.commit()
            return {"success": True, "message": "Message sent successfully."}

        except Error as err:
            connection.rollback()
            logging.error(f"❌ Database Error: {err}")
            return None

        finally:
            cursor.close()
            connection.close()

                
                
    class Status(enum.Enum):
        OPEN = 0               # Ticket is newly created
        IN_PROGRESS = 1        # Admin is working on it
        WAITING_FOR_USER = 2   # Waiting for user response
        WAITING_FOR_ADMIN = 3  # User responded, waiting for admin
        RESOLVED = 4           # Issue resolved but still visible
        CLOSED = 5             # Fully closed & archived