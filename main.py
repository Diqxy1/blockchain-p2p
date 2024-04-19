from src.blockchain import Blockchain
from src.node import Node
import threading

my_blockchain = Blockchain()

p2p_server = Node(my_blockchain, port=3333)
server_thread = threading.Thread(target=p2p_server.start)
server_thread.start()