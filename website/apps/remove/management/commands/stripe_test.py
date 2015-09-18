from billing import get_gateway, CreditCard

stripe = get_gateway('stripe')

'''
first_name = raw_input('First Name (as it appears on your card): ')
last_name = raw_input('Last Name (as it appears on your card): ')
month = int(raw_input('Expiration date - month: '))  # selection list
year = int(raw_input('Expiration date - year: '))  # selection list
number = raw_input('Card number (no dashes or spaces): ')
verification = raw_input('Security code (3 on back, Amex: 4 on front): ')

credit_card = CreditCard(first_name=first_name, last_name=last_name,
                         month=month, year=year,
                         number=number,
                         verification_value=verification)
'''

credit_card = CreditCard(first_name="Test", last_name="User",
                         month=10, year=2016,
                         number="4242424242424242",
                         verification_value="100")

resp = stripe.purchase(0.50, credit_card)

print resp