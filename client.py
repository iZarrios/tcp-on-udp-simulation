import socket
import pickle
from dotenv import load_dotenv
import os
from tcp_packet import TCPPacket




load_dotenv()
port = int(os.getenv("PORT",8080))
address= os.getenv("ADDRESS","localhost")
timeout = int(os.getenv("TIMEOUT",1))

ADDR=(address,port)



# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

udp_socket.settimeout(timeout)

while True:
    try:

        pkt = TCPPacket()
        # send a message to the server
        message = "hahahahhahahahahaa"

        pkt.data = message
        pkt_pk= pickle.dumps(pkt)
        udp_socket.sendto(pkt_pk,ADDR)

        # receive a response from the server
        data, server_address = udp_socket.recvfrom(1024)
        print('Received message:', data.decode())
        print('From server:', server_address)
    except socket.timeout:
        pass

# close the socket
udp_socket.close()