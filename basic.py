blockchain = []

def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def add_transaction(transaction_amount, last_transaction=[1]):
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])

def get_transaction_value():
    user_input = float(input('Your transaction amount please:  '))
    return user_input

def get_user_choice():
    user_input = input('Your choice please: ')
    return user_input

def print_blockchain_elements():
    for block in blockchain:
        print('Outputting Block')
        print(block)
def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid

"""tx_amount = get_user_input()
add_value(last_transaction = get_last_blockchain_value(), transaction_amount = tx_amount)

tx_amount =get_user_input()
add_value(tx_amount, get_last_blockchain_value())
"""
while True:
    print('Please Choose')
    print('1. Add a new Transaction value')
    print('2. Output the Blockchain Block')
    print('3. Quit')
    print('4. Manipulate the chain')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == '3':
        break
    elif user_choice == '4':
        if len(blockchain) >= 1:
           blockchain[0] = [2]
    else:
        print('Invalid Input')
    if not verify_chain():
        print('Invalid Blockchain')
        break

print('Done!')
