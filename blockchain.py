import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset current list of transactions
        self.current_transactions = []

        # Add current block to the blockchain
        self.chain.append(block)
        return block

    def new_transaction(self, sender, receiver, amount):
        """
        Create a new transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Simple PoW algorithm:
        1. Find a number p' such that hash(pp') contains 4 leading zeroes,
        where p is last proof and p' is the new proof.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a Block
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validate proof: Does hash(last_proof, proof) contains 4 leading zeroes?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @property
    def last_block(self):
        return self.chain[-1]

# Initialize blockchain node
app = Flask(__name__)

# Generate global uuid for this node
node_identifier = str(uuid4()).replace('-', '')

# Initialize blockchain
blockchain = Blockchain()

# Route
@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block."

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction."

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }

    return jsonify(response), 200
