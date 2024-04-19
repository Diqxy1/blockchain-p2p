import socket
import datetime as date
import threading
import json
from src.blockchain import Blockchain, Block

class Node:
    def __init__(self, blockchain: Blockchain, port):
        self.blockchain = blockchain
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', port))
        self.server_socket.listen(5)
        print(f"P2P Server listening on port {port}")

    def handle_connection(self, client_socket, address):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            payload = data.decode()
            
            decode_payload = self._decode_json_recv(payload)       
            
            if decode_payload.strip():
                try:
                    json_obj = json.loads(decode_payload)
                    
                    latest_block = self.blockchain._chain[-1] 
                    new_index = latest_block._index + 1
                    new_block = Block(new_index, date.datetime.now(), json_obj, latest_block._hash)
                    self.blockchain.add_block(new_block)
                    
                    print(f"Added new block from {address}")
                    print(self._print(self.blockchain._chain))
                    
                    response = "HTTP/1.1 200 OK\n\nBlock added successfully"
                    client_socket.sendall(response.encode())
                    
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
             
        client_socket.close()

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection established with {address}")
            threading.Thread(target=self.handle_connection, args=(client_socket, address)).start()
    
    def _decode_json_recv(self, data):
        lines = data.split('\n')
            
        # finds the blank line that separates the headers from the message body, if present
        blank_line_index = next((i for i, line in enumerate(lines) if line.strip() == ''), None)
            
        # if there is no blank line, we assume that the entire message is the request body
        if blank_line_index is None:
            json_str = data
            return json_str
        else:
            # Extracts the JSON message body (after the blank line)
            json_str = '\n'.join(lines[blank_line_index+1:])
            return json_str

    def _print(self, chain):
        for block in chain:
            print(f'Block: {block._index}')
            print(f'Timestamp: {block._timestamp}')
            print(f'Payload: {block._payload}')
            print(f'Hash: {block._hash}')
            print(f'Hash Anterior: {block._previous_hash}')
            print(20*'---')