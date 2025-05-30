import random
import sqlite3
IIN = '400000'

logfile = open('debug.log', 'a')


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
    global logfile
    number, pin = create_account(connector)
    customer_id = number[6:-1]
    print('Your card has been created')
    print('Your card number:')
    print(number)
    print('Your card PIN: ')
    print(pin)
    cursor = connector.cursor()
    command = f'INSERT INTO card (id, number, pin) VALUES ("{customer_id}", "{number}", "{pin}")'
    cursor.execute(command)
    print(f'Card created: {customer_id}', file=logfile)
    print('DATABASE CONTENTS')
    cursor.execute(f'SELECT * FROM card')
    print(cursor.fetchall(), file=logfile)
    connector.commit()

def check_balance(account, connector):
    cursor = connector.cursor()
    command = f'SELECT balance FROM card WHERE id="{account}"'
    cursor.execute(command)
    result = cursor.fetchone()
    return result[0]

def add_income(account, connector):
    cursor = connector.cursor()
    income = int(input('Enter income:'))
    cursor.execute(f'UPDATE card SET balance = balance + {income} WHERE id = "{account}"')
    connector.commit()
    print('Income was added!')

def close_account(account, connector):
    cursor = connector.cursor()
    cursor.execute(f'DELETE FROM card WHERE id = "{account}"')
    connector.commit()
    print('The account has been closed!')
    return None


def do_transfer(account, connector, amount, dest_id):
    cursor = connector.cursor()
    source_bal = cursor.execute(f'SELECT balance FROM card WHERE id = "{account}"')
    source_amount = source_bal.fetchone()[0]
    dest_bal = cursor.execute(f'SELECT balance FROM card WHERE id = "{dest_id}"')
    dest_amount = dest_bal.fetchone()[0]
    cursor.execute(f'UPDATE card SET balance = balance - {amount} WHERE id = "{account}"')
    cursor.execute(f'UPDATE card SET balance = balance + {amount} WHERE id = "{dest_id}"')
    source_new = check_balance(account, connector)
    dest_new = check_balance(dest_id, connector)
    if source_amount - source_new == dest_new - dest_amount:
        connector.commit()
        print("Success!")

def money_transfer(account, connector):
    global logfile
    cursor = connector.cursor()
    print('Transfer')
    print('Transfer', file = logfile)
    dest_card = input('Enter card number:')
    print('Enter card number:', file = logfile)
    print(f'des card: {dest_card}', file = logfile)
    cursor.execute(f'SELECT * FROM card WHERE id = "{dest_card}"')
    print(f'DATABASE: {cursor.fetchone()}', file = logfile)
    dest_id = dest_card[6:-1]
    dest_iin = dest_card[0:6]
    raw_card = dest_card[0:-1]
    if dest_id == account:
        print("You can't transfer money to the same account!")
        print(f'dest: {dest_id}, account: {account}', file = logfile)
        print("You can't transfer money to the same account!", file = logfile)
    elif (len(dest_card) != 16) or (luhn_check(raw_card) != dest_card[-1]):
        print('Probably you made mistake in card number. Please try again!')
        print(f'dest_card: {dest_card}, raw_card: {raw_card}', file=logfile)
        print('Probably you made mistake in card number. Please try again!', file=logfile)
    elif dest_iin != IIN or check_id(connector, dest_id) == False:
        print('Such a card does not exist!')
        print(f'dest_iin: {dest_iin}, dest_id: {dest_id}', file = logfile)
        print('Such a card does not exist!', file = logfile)
    else:
        print('Enter how much money you want to transfer:')
        amount = int(input())
        if amount < 0 or amount > check_balance(account, connector):
            print('Not enough money!')
        else:
            do_transfer(account, connector, amount, dest_id)

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
    else:
        prompts = prompts_unlogged
    for i in range(1, len(prompts)):
        print(f'{i}. {prompts[i]}')
    print(f'0. {prompts[0]}')
    choice = int(input())
    if choice == 0:
        print('Bye!')
        conn.close()
        logfile.close()
        exit()
        break
    elif choice == 1:
        if logged_in and account_id:  # Check balance
            balance = check_balance(account_id, conn)
            print(f'Balance: {balance}')
        else:  # Create card
            create_card(conn)
    elif choice == 2:
        if logged_in and account_id:  # Add income
            add_income(account_id, conn)
        else:  # log into account
            account_id = account_login(conn)
            logged_in = True if account_id else False
    elif choice == 3:
        if logged_in and account_id:  # Transfer money to another account
            print('Money Transfer operations from account {account_id}', file = logfile)

            money_transfer(account_id, conn)
    elif choice == 4:  # Close account
        if logged_in and account_id:
            close_account(account_id, conn)
            account_id = None
            logged_in = False
    elif choice == 5:
        if logged_in and account_id:
            account_id = None
            logged_in = False
