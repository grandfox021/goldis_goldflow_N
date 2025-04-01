

def g_round(number, rounding_for= 'buy', digits= 7):
    inc = 0 
    n_pow = 10 ** digits
    if rounding_for == 'buy':
        if (number * n_pow) % 1 != 0:
            inc = 1 / n_pow
    truncated_number = (int(number * n_pow) / n_pow) + inc
    return truncated_number

# def calculate_gold_or_rial_by_one_of_them_and_price(gold_amount, rial_amount, price, buy_or_sell='buy'):
#     error = None
#     #using nano gram
#     gold_floating_number_count = 8
#     if gold_amount > 0 and rial_amount == 0:
#         rial_amount = (gold_amount * price) // (10 ** gold_floating_number_count)
#         if rial_amount == 0:
#             gold_amount = 0
#             error = 'Invalid gold amount'
#     elif rial_amount > 0 and gold_amount == 0:
#         temp_rial_amount =  rial_amount * (10 ** gold_floating_number_count)
#         gold_amount = temp_rial_amount // price
#         if buy_or_sell == 'buy' and temp_rial_amount % price !=0:
#             gold_amount+= 1
#     else:
#         error = 'Error: Data received is invalid.'
        
#     return gold_amount, rial_amount, error
    

# def rial_deposit_transaction(rial_amount) :
    
#     gold_flow_vault = Users_Orm.get_user_by_id(1)
    
#     gold_flow_vault_rial_balance = gold_flow_vault["rial_balance"]
    
    
    
# Case 1: Convert gold amount to rial amount
# gold_amount = 500000000  # 5 grams (assuming gold is stored in nano-grams)
# price = 25000000  # Price per gram
# rial_amount, _, error = calculate_gold_or_rial_by_one_of_them_and_price(gold_amount, 0, price)
# print(rial_amount)  # Should return the equivalent amount in rials
# print("/-----------------------------------------------------/")
# # Case 2: Convert rial amount to gold amount
# rial_amount = 125000000  # 125 million rials
# gold_amount, _, error = calculate_gold_or_rial_by_one_of_them_and_price(0, rial_amount, price)
# print(gold_amount)  # Should return the equivalent amount in gold
  
def round_to_precision(value, precision=8):
    """
    Rounds a given value to the specified decimal precision.
    
    Parameters:
    - value: The number to be rounded.
    - precision: The number of decimal places to round to (default is 8).

    """
    return round(value, precision)

def convert_rial_to_gold_or_vice_versa(rial_amount=0, gold_amount=0, price_per_gram=None, buy_or_sell='buy'):

    if price_per_gram is None or price_per_gram <= 0:
        return None, None, "Invalid price per gram"

    error = None
    
    if gold_amount > 0 and rial_amount == 0:
        # Convert Gold → Rial
        rial_amount = gold_amount * price_per_gram
    elif rial_amount > 0 and gold_amount == 0:
        # Convert Rial → Gold with full precision, then round to 10⁻⁸
        gold_amount = rial_amount / price_per_gram
        gold_amount = round_to_precision(gold_amount, 8)
    else:
        error = "Error: Invalid input. Provide either rial_amount or gold_amount, not both."

    return gold_amount, rial_amount, error
print(convert_rial_to_gold_or_vice_versa(rial_amount=6561555561,gold_amount=0,price_per_gram=651616155))