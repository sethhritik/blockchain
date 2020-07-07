import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request



class MyBlockChain(object):
    def __init__(self):
        self.blockchain = []
        self.transactions = []
        self.create_new_block(previous_hash=1, proof=100)

    def create_new_block(self, proof, previous_hash=None):
        new_block = {
            'index': len(self.blockchain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.blockchain[-1]),
        }

        self.transactions = []

        self.blockchain.append(new_block)
        return new_block


    def create_new_transaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_sorted = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_sorted).hexdigest()

    @property
    def last_block(self):
        # This function returns the last block in the chain
        return self.blockchain[-1]

    def pow(self, last_proof):
        """
        Simple PoW Algorithm:
         - Find a number y, so that hash(xy) starts with 5 zeroes. x is the last y aka last_proof. y is then the new proof.
        :param last_proof: <int>
        :return: <int>
        """

        current_proof = 0
        while self.validate_proof(last_proof, current_proof) is False:
            current_proof += 1

        return current_proof

    @staticmethod
    def validate_proof(last_proof, current_proof):
        """
        Returns, whether the hash of the lastproof and the current_proof contains 5 leading zeroes.
        :param last_proof: <int> Previous Proof Number
        :param current_proof: <int> Current Proof Number
        :return: <bool>
        """

        possible_hash = hashlib.sha256(f'{last_proof}{current_proof}'.encode()).hexdigest()
        return possible_hash[:5] == "00000"

    app = Flask(__name__)
    node_identifier = str(uuid4()).replace('-', '')

    myblockchain = MyBlockChain()

    @app.route('/blockchain', methods=['GET'])
    def get_full_chain():
        output = {
            'chain': myblockchain.blockchain,
            'length': len(myblockchain.blockchain),
        }
        return jsonify(output), 200

    @app.route('/mining', methods=['GET'])
    def mining():
        pass

    @app.route('/transactions/add', methods=['POST'])
    def add_transaction():
        pass

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

    @app.route('/transactions/add', methods=['POST'])
    def add_transaction():
        values = request.get_json()

        # The POST request has to have the following required fields
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'There are values missing', 400

        # Adds a new transaction by utilizing our function
        index = myblockchain.create_new_transaction(values['sender'], values['recipient'], values['amount'])

        output = {
            'message': f'Your registered Transaction is going to be a part of the block with the index of {index}'}
        return jsonify(output), 201

    @app.route('/mining', methods=['GET'])
    def mining():
        # Calculate the new proof by using our PoW algorithm
        last_block = myblockchain.last_block
        last_proof = last_block['proof']
        proof = myblockchain.pow(last_proof)

        # For finding/mining the proof, the miner is granted a reward
        # The sender is nobody, as this coin is coming out of the void
        myblockchain.create_new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1,
        )

        # Add the new created block to the chain
        previous_hash = myblockchain.hash(last_block)
        newblock = myblockchain.create_new_block(proof, previous_hash)

        output = {
            'message': "A new block was mined",
            'index': newblock['index'],
            'transactions': newblock['transactions'],
            'proof': newblock['proof'],
            'previous_hash': newblock['previous_hash'],
        }
        return jsonify(output), 200

