import random


class Accounts:
    all_accounts = {}
    IIN = 400000

    def __init__(self):
        self.card_number = ''
        self.pin = ''
        customer = self.create_account()
        self.create_pin()
        self.balance = 0
        Accounts.all_accounts[customer] = self

    def create_account(self) -> None:
        customer_id: int = random.randrange(000000000, 999999999)
        while customer_id in Accounts.all_accounts:
            customer_id: int = random.randrange(000000000, 999999999)
        self.card_number = f'{Accounts.IIN}{customer_id:09d}'

    def create_pin(self):
        pin_id = random.randrange(0000,9999)
        self.pin = f'{pin_id:04d}'

def check_login():
    pass

def account_login():
    pass

def create_card():
    """
    Account creation. Create the new object and
    adds it to the dictionary with key as the customer number
    prints card # and pin
    """
    new_account = Accounts()
    print(f"""
    Your card has been created
    Yout card number:
    {new_account.card_number}
    Your card PIN:
    {new_account.pin}
    """)

choice = int(input("""
1. Create an account
2. Log into account
0. Exit
"""))

if choice == 1:
    create_card()
elif choice == 2:
    account_login()
else:
    print("Bye!")

# toto = Accounts()
# tutu = Accounts()
print(Accounts.all_accounts)
for account in Accounts.all_accounts:
    print(account)
    print()
    for x in Accounts.all_accounts:
        print(Accounts.all_accounts[x].pin)
