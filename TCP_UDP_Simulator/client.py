# Import socket module
from socket import * 
import sys # In order to terminate the program
import struct
import random
import time

#Code by Evan Imtiaz 
#-------------------------------------------------------UDP-------------------------------------------------------

#PORT DEFINITION 

serverName = 'localhost'

# serverName = '127.0.0.1'

# -----------------------FUNCTION DEFINITIONS ------------------
def check_server_response(response):
    data_len, pcode, entity = struct.unpack_from('!IHH', response)
    if pcode==555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return   


#----------------------------------------------------------------

# Assign a port number
serverPort = 12000

# Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)

# TIME OUT SET TO 5 SECONDS
clientSocket.settimeout(5)

# PACKET CREATION
data = 'Hello World!!!'

# Padding data
if len(data) % 4 != 0:
    Original = len(data)
    Rem = Original % 4
    Final = 4 - Rem + Original
    data = data.ljust(Final, '\0')
    
#Defining variables needed for packing    
data_len = len(data)
pcode = 0
entity = 1

#Packing elements requires to be split into two components, header and data.
Client_packet_1 = struct.pack('!IHH', data_len, pcode, entity)
Client_Packet_2 = data.encode()
Client_packet = Client_packet_1 + Client_Packet_2

# Send packet to server
clientSocket. sendto(Client_packet, (serverName, serverPort))

# Receive packet from server
Server_Packet, serverAddress = clientSocket.recvfrom(2048)

#VALIDATE THE SERVER PACKET WE RECIEVED
check_server_response(Server_Packet)

# UNPACK
Server_Packet_Recieved = struct.unpack('!IHHIIHH', Server_Packet)

print('------------ Starting Stage A  ------------')
print(f'Recieved packed from server: data_len: {Server_Packet_Recieved[0]} pcode: {Server_Packet_Recieved[1]} entity: {Server_Packet_Recieved[2]} repeat: {Server_Packet_Recieved[3]} udp port: {Server_Packet_Recieved[4]} len: {Server_Packet_Recieved[5]} codeA: {Server_Packet_Recieved[6]}')
print('------------ End of Stage A  ------------')

#-------------------RE-BINDING PORT--------------------

newport = Server_Packet_Recieved[4]
serverPort = newport

print('------------ Starting Stage B  ------------')

# PACKET CREATION

Client_padding = 0
Client_Length = Server_Packet_Recieved[5]
repeat = Server_Packet_Recieved[3]

#PADDING

if Client_Length % 4 != 0:
    Rem = Client_Length % 4
    Client_padding = 4 - Rem
    
pcode = Server_Packet_Recieved[6]
entity = 1


if Client_padding != 0:
    Len_Data = Client_Length + Client_padding
    data = bytearray(Len_Data * '0'.encode()) 
else:
    data = bytearray(Client_Length * '0'.encode())
    
data_len = len(data) + 4

Client_Length = len(data)
repeat_value = 0


#INCRIMENT THE REPEAT VALUE UNTIL IT EXCEEDS REPEAT

while repeat_value < repeat:
    
    Client_packet_1 = struct.pack('!IHHI', data_len, pcode, entity, repeat_value)
    
    Client_packet = Client_packet_1 + data
    
    # Send packet to server
    clientSocket.sendto(Client_packet, (serverName, serverPort))
    
    # Receive and unpack packet from server
    received = False
    
    #Try Loop will try to recieve but if it fails it will then sleep for 3 seconds and try again
    while True:
        #print("entered the loop")
        try:
            Server_Packet, serverAddress = clientSocket.recvfrom(2048)
            break
        except:
            time.sleep(1)
            clientSocket.sendto(Client_packet, (serverName, serverPort))
    
    #print("exited the loop")
    repeat_value += 1
    check_server_response(Server_Packet)
    Server_Packet_Recieved = struct.unpack('!IHHI', Server_Packet)
    
    #Print recieved data
    
    print(f'Received acknowledgement packet from server: data_len: {Server_Packet_Recieved[0]} pcode: {Server_Packet_Recieved[1]} entity: {Server_Packet_Recieved[2]} acknumber: {Server_Packet_Recieved[3]}')

# Final Packet is recieved and printed to console

Server_Packet, serverAddress = clientSocket.recvfrom(2048)
Server_Packet_Recieved = struct.unpack('!IHHII', Server_Packet)

tcp_port = Server_Packet_Recieved[3]

print(f'Received final packet: data_len: {Server_Packet_Recieved[0]} pcode: {Server_Packet_Recieved[1]} entity: {Server_Packet_Recieved[2]} tcp_port: {Server_Packet_Recieved[3]} codeB: {Server_Packet_Recieved[4]}')
print('------------ End of Stage B  ------------')

#----------------------------------TCP---------------------------------------

# Assign a port number
serverPort = tcp_port

# Bind the socket to server address and server port
time.sleep(4)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print('')
print('------------ Starting Stage C  ------------')
print(f'connecting to server at TCP port {tcp_port}')

#RECIEVE PACKETS FROM SERVER

Server_Packet = clientSocket.recv(1024)

Server_Packet_Recieved = struct.unpack('!IHHIIIs', Server_Packet)

decoded_data = Server_Packet_Recieved[6].decode()

print(f'Received packet from server: data_len: {Server_Packet_Recieved[0]}  pcode: {Server_Packet_Recieved[1]} entity: {Server_Packet_Recieved[2]} repeat2: {Server_Packet_Recieved[3]} len2: {Server_Packet_Recieved[4]} codeC: {Server_Packet_Recieved[5]} char: {decoded_data}')
print('------------ End of Stage C  ------------')

#Sleep timer in place to ensure packages are recieved properly

time.sleep(1)
repeat2 = Server_Packet_Recieved[3] 
data_len = Server_Packet_Recieved[4]  

if data_len % 4 != 0:
    Rem = Server_Packet_Recieved[4] % 4
    data_len = 4 - Rem + data_len
    
data = decoded_data * data_len
data_encoded = data.encode()

print()
print('------------ Starting Stage D  ------------')
print(f'sending {data} to server for {repeat2} times')

entity = 1
pcode = Server_Packet_Recieved[5]
repeat_value = 0



# The while loop recieves a package with each iteration

while repeat_value < repeat2:
    # print("line 218")
    Client_packet_1 = struct.pack('!I H H', data_len, pcode, entity)
    Client_packet = Client_packet_1 + data_encoded
    #print(Client_Packet)
    clientSocket.send(Client_packet)
    repeat_value = repeat_value + 1
    time.sleep(1)
    
#RECIEVE FINAL PACKET
    
Server_Packet = clientSocket.recv(1024)
Server_Packet_Recieved = struct.unpack(f'!IHHI', Server_Packet)
print(f'Received from server: data_len: {Server_Packet_Recieved[0]} pcode: {Server_Packet_Recieved[1]} entity: {Server_Packet_Recieved[2]} codeD: {Server_Packet_Recieved[3]}')

print()
print("TESTING SUCCESFUL")

#END CONNECTION 

clientSocket.close() 



