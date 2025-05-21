import random

class Accounts:
    all_accounts = {}
    IIN = '400000'

    def __init__(self):
        self.card_number = ''
        self.pin = ''
        customer = self.create_account()
        self.create_pin()
        self.balance = 0
        Accounts.all_accounts[customer] = self

    def create_account(self) -> str:
        checksum = 5
        customer_id = gen_customer_id()+str(checksum)
        while customer_id in Accounts.all_accounts:
            checksum = 9
            customer_id = gen_customer_id()+str(checksum)
        self.card_number = f'{Accounts.IIN}{customer_id}'
        return str(customer_id)

    def create_pin(self):
        pin_id = random.randrange(0000,9999)
        self.pin = f'{pin_id:04d}'
def gen_customer_id():
    return f'{random.randrange(000000000, 999999999):09d}'

def check_login(card, pin):
    res = False
    # print(f'Checking {card} and {pin}')
    # print(f'{card[0:6]} vs. IIN {Accounts.IIN}')
    # print(f'{card[6:]} is in Accounts: {card[6:] in Accounts.all_accounts}')
    # print(f'{Accounts.all_accounts.keys()}')
    if card[0:6] == Accounts.IIN and card[6:] in Accounts.all_accounts:
        if pin == Accounts.all_accounts[card[6:]].pin:
            print('You have successfully logged in!')
            res = True
    return res

def account_operations(account_id):
    # while True:
    operation = int(input('''
    1. Balance
    2. Log out
    0. Exit
    '''))
    if operation == 0:
        print('Bye!')
        # break
    elif operation == 1:
        print(f'Balance: {Accounts.all_accounts[account_id].balance}')
    # elif operation == 2:
    #     break


def account_login():
    # login into account
    card_id = input('Enter your card number:')
    pin_id = input('Enter your PIN:')
    if check_login(card_id, pin_id):
        account_operations(card_id[6:])
    else:
        print('Wrong card number or PIN!')

def create_card():
    """
    Account creation. Create the new object and
    adds it to the dictionary with key as the customer number
    prints card # and pin
    """
    new_account = Accounts()
    print('Your card has been created')
    print('Your card number:')
    print(new_account.card_number)
    print('Your card PIN: ')
    print(new_account.pin)
# Main system prompt





while True:
    choice = int(input('''
    1. Create an account
    2. Log into account
    0. Exit
    '''))
    if choice == 0:
        print('Bye!')
        break
    elif choice == 1:
        create_card()
    elif choice == 2:
        account_login()
