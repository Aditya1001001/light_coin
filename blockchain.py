from functools import reduce
import hashlib
import json
import pickle
from collections import OrderedDict


import hash_util
# The reward we give to miners (for creating a new block)
MINING_REWARD = 7.3

# Our starting block for the blockchain
GENESIS_BLOCK = block = {'previous_hash': '',
                         'index': 0, 'transactions': [], 'proof': 1001001}
# Initializing our (empty) blockchain list
blockchain = [GENESIS_BLOCK]
# Unhandled transactions
open_transactions = []
# the owner of this blockchain node
supes = "Lumiere"
# Registered participants: Ourself + other people sending/ receiving coins
participants = {"Lumiere"}


def load_data():
    """ """
    with open('node_data.txt', mode='r') as f:
        content = f.readlines()
        global blockchain
        global open_transactions
        blockchain = json.loads(content[0][:-1])
        updated_blockchain =[]
        for block in blockchain:
            updated_block = {
                'previous_hash': block['previous_hash'],
                 'index': block['index'],
                 'proof': block['proof'],
                 'transactions': [OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain
        open_transactions = json.loads(content[1])
        updated_transactions = []
        for tx in open_transactions:
            updated_transaction = OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])] )
            updated_transactions.append(updated_transaction)
        open_transactions = updated_transactions


load_data()


def save_data():
    """ """
    with open('node_data.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain, if there is one. """

    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_balance(participant):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    received = 0
    tx_receiver = [[tx['amount'] for tx in block['transactions']
                    if tx['recipient'] == participant] for block in blockchain]
    received = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_receiver, 0)
    return received - sent


def valid_pow(transactions, last_hash, proof):
    """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

    Arguments:
        :transactions: The transactions of the block for which the proof is created.
        :last_hash: The previous block's hash which will be stored in the current block.
        :proof: The proof number we're testing.
    """
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    g_hash = hash_util.hash_string(guess)
    # print(g_hash)
    return g_hash[0:3] == '000'


def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0
    while not valid_pow(open_transactions, last_hash, proof):
        proof += 1

    return proof


def mine_block():
    """Create a new block and add open transactions to it."""

    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()
    # # Miners should be rewarded, so let's create a reward transactioncreate a reward transaction
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', supes), ('amount', MINING_REWARD)])
    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    copy_transactions=open_transactions[:]
    copy_transactions.append(reward_transaction)
    block={
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copy_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient = input("Enter the recipient: ")
    tx_amount = float(input('Your transaction amount please: '))
    return (tx_recipient, tx_amount)


def add_transaction(recipient, sender=supes, amount=0.1):
    """ Add a new transaction to the list of open transactions.

    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amount: Transaction amount(default =  0.1).
    """
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False


def get_user_choice():
    """ Returns the user's choice """
    user_input=input("Your choice: ")
    return user_input


def print_blockchain():
    """Output the blockchain list to the console"""
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-'*50)


def verify_chain():
    """ Checks if the blockchain has been manipulated"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_util.hash_block(blockchain[index-1]):
            return False
        if not valid_pow(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False
    return True


def verify_transactions():
    """ Check if all open transactions are valid """
    return all([verify_transaction(tx) for tx in open_transactions])


def verify_transaction(transaction):
    """Verify a transaction by checking whether the sender has sufficient coins.

     Arguments:
         :transaction: The transaction that should be verified.
     """
    sender_bal=get_balance(transaction['sender'])
    return sender_bal >= transaction['amount']


# blockchain interface
pseudo_input=True
while pseudo_input:
    print("0: Print blockchain")
    print("1: Add a new transaction")
    print("2: Mine a block")
    print("3: Output list of participants")
    print("4: Check transaction validity")
    print("h: Manipulate the blockchain")
    print("q: Quit")
    user_choice=get_user_choice()
    if user_choice == '1':
        transaction_data=get_transaction_value()
        recipient, amount=transaction_data
        if add_transaction(recipient, amount = amount):
            print("Transaction successful")
        else:
            print("Transaction failed")
        print(open_transactions)
    elif user_choice == '0':
        print_blockchain()
    elif user_choice == '2':
        if mine_block():
            open_transactions=[]
            save_data()
    elif user_choice == '3':
        print(participants)
    elif user_choice == '4':
        if verify_transactions:
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0]={'previous_hash': '',
                             'index': 0, 'transactions': [{'sender': "Light",
                                                           'recipient': "Max",
                                                           'amount': 73}]}
    elif user_choice == 'q':
        pseudo_input = False
    else:
        print("invalid Input")
    if not verify_chain():
        print("The blockchain has been manipulated")
        print_blockchain()
        pseudo_input = False
    print("Balance of {}: {:6.2f}".format('Lumiere', get_balance("Lumiere")))
else:
    print("User exited.")
