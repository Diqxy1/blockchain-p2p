import hashlib
import datetime as date

import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, payload, previous_hash):
        self._index = index
        self._timestamp = timestamp
        self._payload = payload
        self._previous_hash = previous_hash
        self._hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self._index).encode() +
            str(self._timestamp).encode() +
            str(self._payload).encode() +
            str(self._previous_hash).encode()
        )
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self._chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), 'Genesis Block', 0)

    def add_block(self, new_block: Block):
        new_block.previous_hash = self._chain[-1]._hash
        new_block.hash = new_block.calculate_hash()
        self._chain.append(new_block)

    def is_valid(self):
        chain_length = len(self._chain)
        for i in range(1, chain_length):
            current_block = self._chain[i]
            previous_block = self._chain[i - 1]

            current_hash = current_block._hash
            prev_hash = previous_block._hash

            if previous_block._index != 0:
                if current_hash != current_block.calculate_hash() or current_hash != prev_hash:
                    return False
        return True