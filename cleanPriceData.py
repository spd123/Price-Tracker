bad_char = {"," , "₹"}
def Clean_price(price):
    for char in bad_char:
        price = price.replace(char,'')
    return float(price)

