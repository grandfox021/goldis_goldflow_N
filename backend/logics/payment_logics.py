# from backend.logics.validation import calculate_gold_or_rial_by_one_of_them_and_price
from models import Users_Orm, Transaction_Orm,Asset_Orm
import time
import logging
from fastapi import HTTPException
# from validation import calculate_gold_or_rial_by_one_of_them_and_price
import uuid

logger = logging.getLogger(__name__)


price_per_gram = Asset_Orm.get_asset_by_code("GOLD").get("current_price_per_gram")
buy_price = Asset_Orm.get_asset_by_code("GOLD").get("buy_price")
sell_price = Asset_Orm.get_asset_by_code("GOLD").get("sell_price")
goldis_vault = Users_Orm.get_user_by_type(3)
    
#--------------------------------logic--------------------------------------

# def round_to_precision(value, precision=8):
#     """
#     Rounds a given value to the specified decimal precision.
#     """
#     return round(value, precision)


# def convert_rial_to_gold_or_vice_versa(rial_amount=0, gold_amount=0, price_per_gram=None, buy_or_sell='buy'):

#     if price_per_gram is None or price_per_gram <= 0:
#         return None, None, "Invalid price per gram"

#     error = None
    
#     if gold_amount > 0 and rial_amount == 0:
#         # Convert Gold → Rial
#         rial_amount = gold_amount * price_per_gram
#     elif rial_amount > 0 and gold_amount == 0:
#         # Convert Rial → Gold with full precision, then round to 10⁻⁸
#         gold_amount = rial_amount / price_per_gram
#         gold_amount = round_to_precision(gold_amount, 8)
#     else:
#         error = "Error: Invalid input. Provide either rial_amount or gold_amount, not both."

#     return gold_amount, rial_amount, error


#-----------------------------------end logic-----------------------------------

def rial_deposit(
    buyer_user_id=None, seller_user_id=None, rial_amount=None, payment_fee=None, current_price=None,
    goldis_fee=None, description='', transaction_id=None,
    payment_provider_type=None, payment_ref_id=None, related_transaction_id=0,
    create_datetime=None, invoice_id=None, bank_card_id=0, asset_id=None
):
    """Handles Rial deposit transactions (New & Existing Transactions)"""

    error = None
    new_transaction_id = None

    # ✅ Ensure asset_id is properly set
    if asset_id is None:
        asset = Asset_Orm.get_asset_by_code("IRR")
        if not asset:
            return "Invalid asset", None  # If asset is not found
        asset_id = asset.get("id")
    print(f"✅ Using Asset ID: {asset_id}")

    try:
        if transaction_id is None:
            buyer = Users_Orm.get_user_by_id(buyer_user_id)
            if not buyer:
                return "Invalid buyer", None

            seller = Users_Orm.get_user_by_id(seller_user_id) if seller_user_id else Users_Orm.get_user_by_type(3)
            if not seller:
                return "Invalid seller", None

            # ✅ Generate a **new unique payment_ref_id** for this transaction
            new_payment_ref_id = str(uuid.uuid4())

            # ✅ Determine transaction type
            transaction_type = (
                Transaction_Orm.Types.admin_rial_deposit.value if buyer["user_type"] == Users_Orm.Types.admin.value
                else Transaction_Orm.Types.ipg_rial_deposit.value
            )

            transaction_status = Transaction_Orm.Status.pending.value
            asset_price_at_time = current_price if current_price else Asset_Orm.get_asset_by_code("GOLD").get("current_price_per_gram")
            description = "Rial deposit transaction"
            create_datetime = create_datetime if create_datetime else int(time.time())

            # ✅ Create New Transaction
            transaction_result = Transaction_Orm.create_transaction(
                user_id=buyer_user_id,
                sso_unique_id=buyer["sso_unique_id"],
                asset_id=asset_id,
                rial_amount=rial_amount,
                gold_amount=0,
                transaction_type=transaction_type,
                status=transaction_status,
                asset_price_at_transaction_time=asset_price_at_time,
                description=description,
                buyer_rial_balance=buyer["rial_balance"],
                buyer_gold_balance=buyer["gold_balance"],
                seller_rial_balance=seller["rial_balance"],
                seller_gold_balance=seller["gold_balance"],
                buyer_id=buyer_user_id,
                seller_id=seller["id"],
                goldis_fee=goldis_fee,
                payment_fee=payment_fee,
                payment_provider_type=Transaction_Orm.Payment_provider_types.sepehr_ipg.value,
                payment_ref_id=new_payment_ref_id,  # ✅ Always generates a new UUID
            )

            if transaction_result:
                new_transaction_id = transaction_result
                print(f"✅ Rial deposit transaction created successfully with ID: {new_transaction_id}")
                return new_transaction_id
            else:
                return "Transaction creation failed", None
        else:
            # ✅ Process existing transaction
            print(f"🔄 Processing existing Rial deposit transaction: {transaction_id}")
            new_transaction_id = Users_Orm.deposit_rial_transaction(transaction_id)
            if new_transaction_id:
                print(f"✅ Rial deposit transaction completed successfully: {new_transaction_id}")
            else:
                print(f"⚠️ Error processing transaction: {transaction_id}")
            return new_transaction_id
    except HTTPException as e:
        print(f"🚨 HTTP Exception in rial_deposit: {e.detail}")
        raise e
    except Exception as e:
        print(f"🚨 Unexpected error in rial_deposit: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
def gold_buy(
    buyer_user_id=None, seller_user_id=None, gold_amount=None, rial_amount=None, 
    payment_fee=None, goldis_fee=None, description='', transaction_id=None, current_price=None,
    payment_provider_type=None, payment_ref_id='None', related_transaction_id=0,
    create_datetime=None, invoice_id='None', bank_card_id=0, asset_id=None
):
    """Handles Gold Buy Transactions (New & Existing Transactions)"""

    error = None
    new_transaction_id = None

    # ✅ Fix Asset ID Validation
    if asset_id is None:
        asset_id = Asset_Orm.get_asset_by_code("GOLD").get("id")

    # ✅ Check if this is a NEW Transaction
    if transaction_id is None:
        # ✅ Fetch Buyer & Seller
        buyer = Users_Orm.get_user_by_id(buyer_user_id)
        if not buyer:
            return "Invalid buyer", None

        sso_unique_id = buyer["sso_unique_id"]
        print(f"🛠️ sso unique for buyer user in gold buy payment logics {sso_unique_id}")

        seller = goldis_vault
        if not seller:
            return "Invalid seller", None

        # ✅ Determine payment provider type and transaction type
        payment_provider_type = (
            Transaction_Orm.Types.admin_gold_buy.value
            if buyer["user_type"] == Users_Orm.Types.admin.value
            else Transaction_Orm.Types.gold_buy.value
        )

        transaction_type = payment_provider_type
        transaction_status = Transaction_Orm.Status.pending.value
        asset_price_at_time = current_price if current_price else price_per_gram
        description = "Gold buy transaction"
        create_datetime = create_datetime if create_datetime else int(time.time())

        try:
            # ✅ Create New Transaction
            transaction_result = Transaction_Orm.create_transaction(
                user_id=buyer_user_id,
                sso_unique_id=sso_unique_id,
                asset_id=asset_id,
                rial_amount=rial_amount,
                gold_amount=gold_amount,
                transaction_type=transaction_type,
                status=transaction_status,
                asset_price_at_transaction_time=asset_price_at_time,
                description=description,
                buyer_rial_balance=buyer["rial_balance"],
                buyer_gold_balance=buyer["gold_balance"],
                seller_rial_balance=seller["rial_balance"], 
                seller_gold_balance=seller["gold_balance"],
                buyer_id=buyer_user_id,
                seller_id=seller["id"],
                goldis_fee=goldis_fee,
                payment_fee=payment_fee if payment_fee else 0,
                payment_provider_type=Transaction_Orm.Payment_provider_types.cash.value,
                payment_ref_id=payment_ref_id,
            )

            # ✅ Debug Transaction Result
            print(f"🛠️ Transaction Result in gold buy: {transaction_result}")

            if transaction_result:
                new_transaction_id = transaction_result
            else:
                return "Transaction creation failed", None

        except HTTPException as e:
            print(f"🚨 HTTP Exception in gold_buy: {e.detail}")
            raise e
        except Exception as e:
            print(f"🚨 Unexpected error in gold_buy: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    else:
        # ✅ Process Existing Transaction
        try:
            print(f"🔄 Processing existing Gold Buy transaction: {transaction_id}")
            new_transaction_id = Users_Orm.gold_buy_transaction(transaction_id)

            if new_transaction_id:
                print(f"✅ Gold Buy transaction processed successfully: {new_transaction_id}")
            else:
                print(f"⚠️ Error processing transaction: {transaction_id}")
                return "Transaction processing failed", None

        except HTTPException as e:
            print(f"🚨 HTTP Exception in gold_buy (existing transaction): {e.detail}")
            raise e
        except Exception as e:
            print(f"🚨 Unexpected error in gold_buy (existing transaction): {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    return new_transaction_id


def gold_sell(
    buyer_user_id=None, seller_user_id=None, gold_amount=None, current_price=None, 
    goldis_fee=None, description='', transaction_id=None, rial_amount=None, 
    payment_provider_type=None, payment_ref_id='None', related_transaction_id=0,
    create_datetime=None, invoice_id='None', bank_card_id=0, asset_id=None
):
    """Handles Gold Sell Transactions (New & Existing Transactions)."""
    try:
        # ✅ Validate asset ID
        if asset_id is None:
            asset = Asset_Orm.get_asset_by_code("GOLD")
            if not asset:
                raise HTTPException(status_code=400, detail="Invalid asset")
            asset_id = asset.get("id")

        if transaction_id is None:
            # ✅ Fetch Seller (User Selling Gold) & Buyer (Marketplace)
            seller = Users_Orm.get_user_by_id(seller_user_id)  # The person selling gold
            buyer = goldis_vault  # The platform (goldis vault)

            if not seller or not buyer:
                raise HTTPException(status_code=400, detail="Invalid buyer or seller")

            # ✅ Check if user has enough gold balance
            user_gold_balance = seller["gold_balance"]
            if user_gold_balance < gold_amount:
                raise HTTPException(status_code=400, detail="Insufficient gold balance")

            # ✅ Determine transaction type
            if seller["user_type"] == Users_Orm.Types.admin.value:
                transaction_type = Transaction_Orm.Types.admin_gold_sell.value
            else:
                transaction_type = Transaction_Orm.Types.gold_sell.value

            transaction_status = Transaction_Orm.Status.pending.value
            asset_price_at_time = current_price if current_price else price_per_gram
            description = "Gold sell transaction"
            create_datetime = create_datetime if create_datetime else int(time.time())

            # ✅ Calculate Rial Amount after Fees
            # total_rial_value = (gold_amount * asset_price_at_time) - (goldis_fee if goldis_fee else 0)
            # if total_rial_value <= 0:
            #     raise HTTPException(status_code=400, detail="Invalid transaction amount")

            total_rial_value = rial_amount
            
            # ❗️ **Ensure Goldis Vault Has Enough Rial Balance**
            if buyer["rial_balance"] < total_rial_value:
                raise HTTPException(status_code=400, detail="Goldis Vault does not have enough Rial balance to process this transaction.")

            # ✅ Create New Transaction
            transaction_result = Transaction_Orm.create_transaction(
                user_id=seller_user_id,
                sso_unique_id=seller["sso_unique_id"],
                asset_id=asset_id,
                rial_amount=total_rial_value,  # User receives Rials
                gold_amount=gold_amount,  # Deducted from user
                transaction_type=transaction_type,
                status=transaction_status,
                asset_price_at_transaction_time=asset_price_at_time,
                description=description,
                buyer_rial_balance=buyer["rial_balance"],
                buyer_gold_balance=buyer["gold_balance"],
                seller_rial_balance=seller["rial_balance"],
                seller_gold_balance=seller["gold_balance"],
                buyer_id=buyer["id"],
                seller_id=seller["id"],
                goldis_fee=goldis_fee,
                payment_fee=0,
                payment_provider_type=Transaction_Orm.Payment_provider_types.cash.value,
                payment_ref_id=payment_ref_id,
            )

            if not transaction_result:
                raise HTTPException(status_code=500, detail="Transaction creation failed")

            return transaction_result  # Return the created transaction ID

        else:
            # ✅ Process Existing Transaction via ORM function
            try:
                print(f"🔄 Processing existing Gold Sell transaction: {transaction_id}")
                new_transaction_id = Users_Orm.gold_sell_transaction(transaction_id)

                if not new_transaction_id:
                    raise HTTPException(status_code=500, detail="Transaction processing failed")

                print(f"✅ Gold Sell transaction processed successfully: {new_transaction_id}")
                return new_transaction_id

            except HTTPException as e:
                print(f"🚨 HTTP Exception in gold_sell: {e.detail}")
                raise  # Directly re-raise HTTP exceptions without modification
            except Exception as e:
                print(f"🚨 Unexpected error in gold_sell: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    except HTTPException as e:
        print(f"🚨 HTTP Exception in gold_sell: {e.detail}")
        raise  # Ensure HTTPExceptions are propagated correctly
    except Exception as e:
        print(f"🚨 Critical error in gold_sell: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Critical error: {str(e)}")


def rial_withdraw(
    seller_user_id=None, rial_amount=None, bank_card_id=None, 
    transaction_id=None, description='Rial Withdraw', payment_provider_type=None, 
    payment_ref_id=None, create_datetime=None, asset_id=None
):
    """
    Handles Rial Withdraw Transactions (New & Existing Transactions).
    """

    error = None
    new_transaction_id = None

    # ✅ Fix Asset ID Validation
    if asset_id is None:
        asset = Asset_Orm.get_asset_by_code("IRR")
        if not asset:
            return "Invalid asset", None  # If asset is not found
        asset_id = asset.get("id")

    # ✅ Validate Rial Amount
    if rial_amount is None or rial_amount <= 0:
        return "Invalid withdrawal amount", None

    # ✅ Check if this is a NEW Transaction
    if transaction_id is None:
        # ✅ Fetch Seller (User Withdrawing Rial)
        seller = Users_Orm.get_user_by_id(seller_user_id)
        buyer = goldis_vault  # Platform's Vault

        if not seller:
            return "Invalid seller", None

        sso_unique_id = seller["sso_unique_id"]
        print(f"🛠️ SSO Unique ID for withdrawal: {sso_unique_id}")

        # ✅ Ensure User Has Sufficient Rial Balance
        if seller["rial_balance"] is None or seller["rial_balance"] < rial_amount:
            return "Insufficient balance", None

        # ✅ Determine Transaction Type
        transaction_type = Transaction_Orm.Types.rial_withdrawal.value
        transaction_status = Transaction_Orm.Status.pending.value
        create_datetime = create_datetime if create_datetime else int(time.time())
        new_payment_ref_id = str(uuid.uuid4())

        try:
            # ✅ Create New Transaction
            transaction_result = Transaction_Orm.create_transaction(
                user_id=seller_user_id,
                sso_unique_id=sso_unique_id,
                asset_id=asset_id,
                rial_amount=rial_amount,  # Deduct Rial from user
                gold_amount=0,
                transaction_type=transaction_type,
                status=transaction_status,
                asset_price_at_transaction_time=0,  # No asset price for Rial withdrawal
                description=description,
                buyer_rial_balance=buyer["rial_balance"],
                buyer_gold_balance=buyer["gold_balance"],
                seller_rial_balance=seller["rial_balance"],
                seller_gold_balance=seller["gold_balance"],
                buyer_id=buyer["id"],  # Platform
                seller_id=seller["id"],
                goldis_fee=0,
                payment_fee=0,
                payment_provider_type=Transaction_Orm.Payment_provider_types.third_party.value,
                payment_ref_id=new_payment_ref_id,
            )

            # ✅ Debug Transaction Result
            print(f"🛠️ Transaction Result in Rial Withdraw: {transaction_result}")

            if not transaction_result:
                return "Transaction creation failed", None

            new_transaction_id = transaction_result
            return None, new_transaction_id  # Return error as None if successful

        except HTTPException as e:
            print(f"🚨 HTTP Exception in rial_withdraw: {e.detail}")
            raise e
        except Exception as e:
            print(f"🚨 Unexpected error in rial_withdraw: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    else:
        # ✅ Process Existing Transaction (Deduct Balance & Complete Transaction)
        try:
            print(f"🔄 Processing existing Rial Withdraw transaction: {transaction_id}")
            error, processed_transaction_id = Users_Orm.rial_withdraw_transaction(transaction_id)

            if error:
                print(f"⚠️ Error processing transaction: {error}")
                return error, None

            print(f"✅ Rial Withdraw transaction processed successfully: {processed_transaction_id}")

            return None, processed_transaction_id

        except HTTPException as e:
            print(f"🚨 HTTP Exception in rial_withdraw (existing transaction): {e.detail}")
            raise e
        except Exception as e:
            print(f"🚨 Unexpected error in rial_withdraw (existing transaction): {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
