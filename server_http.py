import socket
from dotenv import load_dotenv
import os
import pickle as pkl
from ParserHttp import *

# from tcp_packet import TCPPacket
from udp_tcp_socket import TCPOverUDPSocket, print_packet

load_dotenv()
port = int(os.getenv("PORT",8080))
address= os.getenv("ADDRESS","localhost")
timeout = int(os.getenv("TIMEOUT",1))

req1="""GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
Accept-Language: en-US,en;q=0.5\r\n
Accept-Encoding: gzip, deflate\r\n
Connection: keep-alive\r\n
\r\n"""



req2="""POST /users HTTP/1.1\r\n
Host: example.com\r\n
Content-Type: application/json\r\n
Content-Length: 56\r\n
Authorization: Bearer xxxxxxxx\r\n
\r\n"""



req3="""GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n
Accept-Language: en-US,en;q=0.5\r\n
Accept-Encoding: gzip, deflate\r\n
Connection: keep-alive\r\n
\r\n"""

req4 = """POST /users HTTP/1.1\r\n\
Host: example.com\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Content-Length: 27\r\n\
Authorization: Bearer xxxxxxxx\r\n\
\r\n\
first_name=john&last_name=doe"""

response1="""
HTTP/1.1 200 OK\r\n
Content-Type: application/json; charset=UTF-8\r\n
Date: Fri, 30 Apr 2023 10:00:00 GMT\r\n
Expires: Fri, 30 Apr 2023 11:00:00 GMT\r\n
Cache-Control: public, max-age=3600\r\n
\r\n"""

response2="""
HTTP/1.1 200 OK\r\n
Date: Sun, 26 Sep 2010 20:09:20 GMT\r\n
Server: Apache/2.0.52 (CentOS)\r\n
Last-Modified: Tue, 30 Oct 2007 17:00:02 GMT\r\n
ETag: "17dc6-a5c-bf716880"\r\n
Accept-Ranges: bytes\r\n
Content-Length: 2652\r\n
Keep-Alive: timeout=10, max=100\r\n
Connection: Keep-Alive\r\n
Content-Type: text/html; charset=ISO-8859-1\r\n
\r\n
data data data data data """

response3="""
HTTP/1.1 200 OK\r\n
Content-Length: 55\r\n
Content-Type: text/html\r\n
Last-Modified: Wed, 12 Aug 1998 15:03:50 GMT\r\n
Accept-Ranges: bytes\r\n
ETag: “04f97692cbd1:377”\r\n
Date: Thu, 19 Jun 2008 19:29:07 GMT\r\n
\r\n"""

ADDR=(address,port)

udp_socket = TCPOverUDPSocket()

# bind the socket to a specific address and port
udp_socket.bind(ADDR)
udp_socket.settimeout(timeout)

udp_socket.listen()

print('Server is listening on', ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        if conn.status == 1:
            print("Connection closed")
            break
        # recieve message from client
        try:
            data = conn.rcv()
            if not data:
                continue
            if data.data == "FIN":
                continue
            # packet_type = packet.packet_type()
            # print_packet(data)
            print("DATA START")
            print(data.data)
            print("DATA END")
            print("-----------------------")
            print("RESPONSE START")
            response = HttpRequest(data.data)
            print(response)
            print("RESPONSE END")
        except socket.timeout:
            print("Timeout")
            conn.close()
            break

while True:
    addr, _= udp_socket.accept()
    handle_client(udp_socket, addr)
