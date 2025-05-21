import random


class Accounts:
    all_accounts = []
    IIN = 400000

    def __init__(self):
        self.customer = ''
        self.pin = ''
        self.create_account()
        self.create_pin()
        self.balance = 0
        Accounts.all_accounts.append(self)

    def create_account(self) -> None:
        customer_id: int = random.randrange(000000000, 999999999)
        while customer_id in Accounts.all_accounts:
            customer_id: int = random.randrange(000000000, 999999999)
        self.customer = f'{customer_id:09d}'

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
    {Accounts.IIN}{new_account.customer}
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
    print(Accounts.all_accounts[0])
    for x in Accounts.all_accounts:
        print(x.pin)

# initial test
# Can't get this foing woth GIT
