import random
import sqlite3


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
        # checksum = 5
        customer_id = gen_customer_id()
        customer_id += luhn_check(Accounts.IIN + customer_id)

        while customer_id in Accounts.all_accounts:
            # checksum = 9
            # customer_id = gen_customer_id()+str(checksum)
            customer_id = gen_customer_id()
            customer_id += luhn_check(Accounts.IIN + customer_id)
        self.card_number = f'{Accounts.IIN}{customer_id}'
        return str(customer_id)

    def create_pin(self):
        pin_id = random.randrange(0000,9999)
        self.pin = f'{pin_id:04d}'


def gen_customer_id():
    return f'{random.randrange(000000000, 999999999):09d}'

def luhn_check(raw_number):
    digits = [int(x) for x in raw_number]
    for i in range(len(digits)):
        digit = digits[i]
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        digits[i] = digit

    checksum = (10 - sum(digits) % 10) %10
    return str(checksum)


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

def account_login():
    # login into account
    card_id = input('Enter your card number:')
    pin_id = input('Enter your PIN:')
    if check_login(card_id, pin_id):
        return Accounts.all_accounts[card_id[6:]]
    else:
        print('Wrong card number or PIN!')
        return None

def create_card(connector):
    """
    Account creation. Create the new object and
    adds it to the dictionary with key as the customer number
    prints card # and pin
    It also records all in the cards database for which connector is
    supplied.
    """
    new_account = Accounts()
    number = new_account.card_number
    id = number[6:-1]
    pin = new_account.pin
    print('Your card has been created')
    print('Your card number:')
    print(new_account.card_number)
    print('Your card PIN: ')
    print(new_account.pin)
    cursor = connector.cursor()
    command = f'INSERT INTO card (id, number, pin) VALUES ("{id}", "{number}", "{pin}")'
    # print(command)
    cursor.execute(command)
    connector.commit()

#Program start here

# Database creation
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    )
''')
conn.commit()
# Main system prompt

logged_in = False
account_id = None
prompts = ['Exit', 'Create an account', 'Log into account']

while True:
    if logged_in:
        prompts[1] = 'Balance'
        prompts[2] = 'Log out'
    else:
        prompts[1] = 'Create an account'
        prompts[2] = 'Log into account'
    print(f'1. {prompts[1]}')
    print(f'2. {prompts[2]}')
    print(f'0. {prompts[0]}')
    choice = int(input())
    if choice == 0:
        print('Bye!')
        conn.close()
        break
    elif choice == 1:
        if logged_in and account_id:
            print(f'Balance: {account_id.balance}')
        else:
            create_card(conn)
    elif choice == 2:
        if logged_in and account_id:
            account_id = None
            logged_in = False
        else:
            account_id = account_login()
            logged_in = True if account_id else False
