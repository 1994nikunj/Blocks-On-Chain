import hashlib
import time


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class Block:
    def __init__(self, previous_hash, transactions, timestamp, nonce=0):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = self.previous_hash + str(self.timestamp) + str(self.nonce) + str([t.__dict__ for t in self.transactions])
        sha = hashlib.sha256()
        sha.update(data.encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        start_time = time.time()
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        end_time = time.time()
        print(f"Block mined in {end_time - start_time:.2f} seconds")


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = difficulty

    @staticmethod
    def create_genesis_block():
        return Block("0", [], 0, 0)

    def add_block(self, block):
        self.chain.append(block)

    def mine_pending_transactions(self, miner_address):
        timestamp = int(time.time())
        block = Block(self.get_last_block().hash, self.pending_transactions, timestamp)
        block.mine_block(self.difficulty)
        print(f"Block mined: {block.hash}")
        self.add_block(block)
        self.pending_transactions = [Transaction(None, miner_address, 1)]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_last_block(self):
        return self.chain[-1]

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.receiver == address:
                    balance += transaction.amount
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print("Current block hash does not match")
                return False
            if previous_block.hash != current_block.previous_hash:
                print("Previous block hash does not match")
                return False
        return True


if __name__ == '__main__':
    blockchain = Blockchain()

    print("Mining block 1...")
    blockchain.add_transaction(Transaction("A", "B", 100))
    blockchain.mine_pending_transactions("miner1")

    print("Mining block 2...")
    blockchain.add_transaction(Transaction("C", "D", 10))
    blockchain.mine_pending_transactions("miner2")
