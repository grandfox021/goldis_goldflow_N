# import email
# from http.client import BAD_GATEWAY
from pydantic import BaseModel,Field
from typing import Optional

class FinishRialTransaction(BaseModel):
    transaction_id : int
    asset_id : int = 2
    
    
class RialDepositRequest(BaseModel):
    # goldis_fee : float
    rial_amount: float
    banck_card_number: Optional[int] = None 
    transaction_id: Optional[int] = None 

    
    
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    national_id: str
    email : str
    password: str  # Store hashed passwords in a real application

class OTPRequest(BaseModel):
    phone_number: str= "09217974330"  # Or email, depending on your method of communication


class OTPVerification(BaseModel):
    phone_number: str
    otp: str
 
 
class VerifyOTPRequestSchema(BaseModel):
    mobile_number: str
    user_id : str
    otp: str


class GoldBuyRequest(BaseModel):
    gold_amount: float = Field(..., gt=0, description="Amount of gold in grams")
    final_price: float = Field(..., gt=0, description="Amount of rials")
    current_price : float = Field(..., gt=0, description="Amount of rials")
    goldis_fee : float
    
class GoldSellRequest(BaseModel):
    gold_amount: float = Field(..., gt=0, description="Amount of gold in grams")
    final_price: float = Field(..., gt=0, description="Amount of rials")
    current_price : float = Field(..., gt=0, description="Amount of rials")
    goldis_fee : float
       
    
    
class RialWithdrawRequest(BaseModel):
    withdraw_amount: float  # Amount to withdraw in Rial
    bank_card_id: int  # Bank card ID for withdrawal
    description: str = "Rial Withdrawal Request"  # Default description


class CardNumberRequest(BaseModel):
    card_number : str
    
    
class WithdrawalRequestCreate(BaseModel):
    amount: float
    card_number : str
    # bank_name : str

class WithdrawalRequestUpdate(BaseModel):
    status: str
    

class TicketCreate(BaseModel):
    subject: str
    priority: int


class TicketMessageCreate(BaseModel):
    ticket_id: int
    message: str
    
    
class TicketCreateWithMessage(BaseModel):
    subject: str
    message: str