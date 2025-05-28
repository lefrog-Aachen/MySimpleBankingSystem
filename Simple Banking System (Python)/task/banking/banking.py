import random
import sqlite3
IIN = '400000'


def create_pin():
    pin_id = random.randrange(0000,9999)
    return f'{pin_id:04d}'

def check_id(connector, customer_id):
    """ Checks whether a customer_id exists in the database
     connector: connector to the db with a table card
     """
    cid_cur = connector.cursor()
    cid_cur.execute(f'SELECT * FROM card WHERE id = {customer_id}')
    result = cid_cur.fetchone()
    return True if result else False

def create_account(connector):
    cac_cur = connector.cursor()
    customer_id = gen_customer_id()
    while check_id(connector, customer_id):
        customer_id = gen_customer_id()
    raw_card = IIN + customer_id
    card_number = raw_card + luhn_check(raw_card)
    card_pin = create_pin()
    return card_number, card_pin

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


def check_login(card, pin, connector):
    res = False
    # print(f'Checking {card} and {pin}')
    # print(f'{card[0:6]} vs. IIN {Accounts.IIN}')
    # print(f'{card[6:]} is in Accounts: {card[6:] in Accounts.all_accounts}')
    # print(f'{Accounts.all_accounts.keys()}')
    cursor = connector.cursor()
    command = f'SELECT * FROM card WHERE number="{card}" AND pin="{pin}"'
    cursor.execute(command)
    c_result = cursor.fetchone()
    if c_result:
        print('You have successfully logged in!')
        res = True
    return res

def account_login(connector):
    """
    Performs the account login mechanism.
    Checks against the database the existence of an account
    and whether the provided card number and pin are correct.
    """
    # log into account
    card_id = input('Enter your card number:')
    pin_id = input('Enter your PIN:')
    if check_login(card_id, pin_id, connector):
        return card_id[6:-1]
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
    number, pin = create_account(connector)
    customer_id = number[6:-1]
    print('Your card has been created')
    print('Your card number:')
    print(number)
    print('Your card PIN: ')
    print(pin)
    cursor = connector.cursor()
    command = f'INSERT INTO card (id, number, pin) VALUES ("{customer_id}", "{number}", "{pin}")'
    # print(command)
    cursor.execute(command)
    connector.commit()

def check_balance(account_id, connector):
    cursor = connector.cursor()
    command = f'SELECT balance FROM card WHERE id="{account_id}"'
    cursor.execute(command)
    result = cursor.fetchone()
    return result[0]

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
prompts_unlogged = ['Exit', 'Create an account', 'Log into account']
prompts_logged = ['Exit', 'Balance', 'Add income', 'Do transfer', 'Close account', 'Logout']




while True:
    if logged_in:
        prompts = prompts_logged
        # prompts[1] = 'Balance'
        # prompts[2] = 'Log out'
    else:
        prompts = prompts_unlogged
        # prompts[1] = 'Create an account'
        # prompts[2] = 'Log into account'
    for i in range(1, len(prompts)):
        print(f'{i}. {prompts[i]}')
    # print(f'1. {prompts[1]}')
    # print(f'2. {prompts[2]}')
    # print(f'0. {prompts[0]}')
    print(f'0. {prompts[0]}')
    choice = int(input())
    if choice == 0:
        print('Bye!')
        conn.close()
        break
    elif choice == 1:
        if logged_in and account_id:
            balance = check_balance(account_id, conn)
            print(f'Balance: {balance}')
        else:
            create_card(conn)
    elif choice == 2:
        if logged_in and account_id:
            pass
        else:
            account_id = account_login(conn)
            logged_in = True if account_id else False
    elif choice == 3:
        if logged_in and account_id:
            pass
    elif choice == 4:
        if logged_in and account_id:
            pass
    elif choice == 5:
        if logged_in and account_id:
            account_id = None
            logged_in = False
