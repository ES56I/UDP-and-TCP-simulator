# Import socket module
from socket import * 
import random
import struct
import sys  # In order to terminate the program
import time

#Code by Evan Imtiaz

#-------------------------------------------------------UDP-------------------------------------------------------

# Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(('localhost', serverPort))

#Sets timeout to occur after 3 seconds from last response
serverSocket.settimeout(3)

#
while True:
    client_packet, clientAddress = serverSocket.recvfrom(1024)
    CHECK_VALUE = client_packet[3] 
    #print(client_packet[3])
    length = client_packet[3]
    client_packet_unpacked = struct.unpack(f'!IHH{length}s', client_packet)
    
    
    compared_message = client_packet_unpacked[3]
 
 
    #GENERATE VARIOUS ELEMENTS 
    client_packet_data = client_packet_unpacked[3].decode()
    print(f'receiving from the client: data_length: {client_packet_unpacked[0]} code: {client_packet_unpacked[1]} entity: {client_packet_unpacked[2]} data: {client_packet_data}')
    data_len = struct.calcsize('!IIHH')
    
    #VARIABLE DEFINITIONS
    pcode = 0
    entity = 2
    repeat = random.randint(5, 20)
    length = random.randint(50, 100)
    udp_port = random.randint(20000, 30000)
    codeA = random.randint(100, 400)
    
    #PACK ELEMENTS
    server_packet = struct.pack('!IHHIIHH', data_len, pcode, entity, repeat, udp_port, length, codeA)
    
    
    print('------------ Starting Stage A  ------------')
    print(f'sending to the client: data_length: {data_len} code: {pcode} entity: {entity} repeat: {repeat} udp_port: {udp_port} len: {length} codeA: {codeA}')
    print(f'SERVER: Server ready on the new UDP port: {udp_port}')
    print('SERVER:------------ End of Stage A  ------------')
    print('')
    
    # Send packet to client 
    serverSocket.sendto(server_packet, clientAddress)
    
    #Break used to exit the loop
    break


#Setting up new serverPort
serverPort = udp_port

#Closing connection
serverSocket.close()

#Opening connection
Serverside_Socket_The_Second = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
Serverside_Socket_The_Second.bind(('127.0.0.1', serverPort))

#PADDING
if length % 4 != 0:
    Rem = length % 4
    length = 4 - Rem + length

print('SERVER:------------ Starting Stage B  ------------')

#Variable definitions
repeat_counter = 0


#Generates random ack package and sends to client
while repeat_counter < repeat:
    rng_ack = random.randint(1, 100)
    
    #Sets up Sending and recieving to Client
    client_packet, clientAddress = Serverside_Socket_The_Second.recvfrom(2048)
    client_packet_unpacked = struct.unpack(f'!IHHI{length}s', client_packet)
    
    #Organizes elements to send to Client
    if rng_ack > 50 and client_packet_unpacked[3] == repeat_counter:
        entity = 2
        data_len = 4 
        pcode = client_packet_unpacked[1]
        
        #Packs elements to send
        server_packet = struct.pack('!IHHI', data_len, pcode, entity, repeat_counter)
        Serverside_Socket_The_Second.sendto(server_packet, clientAddress)
        repeat_counter+=1
        
        print(f'SERVER: received packet_id {client_packet_unpacked[3]} data_len {client_packet_unpacked[0]} pcode: {client_packet_unpacked[1]}')

#Generates Values to pack and send
data_len = struct.calcsize('!II')
tcp_port = random.randint(20000, 30000)
codeB = random.randint(100, 400)

#Packing Elements 
server_packet = struct.pack('!IHHII', data_len, pcode, entity, tcp_port, codeB)

#Sending Elements
Serverside_Socket_The_Second.sendto(server_packet, clientAddress)


print(f'------------- B2: sending tcp_port {tcp_port} codeB {codeB}')
print('------------ End of Stage B  ------------')

Serverside_Socket_The_Second.close()  # Terminate the program after sending the corresponding data

#----------------------------------TCP-------------------------------------
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

#Defining Port
serverPort = tcp_port

# Bind the socket to server address and server port
serverSocket.bind(('127.0.0.1', serverPort))

# listens for 5 seconds
serverSocket.listen(5)

print('')
print('------------ Stating Stage C ------------')
print(f'The server is ready to receive on tcp port: {tcp_port}')

# Definitions
pcode = codeB
entity = 2
repeat2 = random.randint(5, 20)
len2 = random.randint(50, 100)
codeC = random.randint(100, 400)
data = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ').encode()
data_len = len(data) + struct.calcsize('III')

#Listens for connections
while True:
    connectionSocket, addr = serverSocket.accept()
    server_packet = struct.pack('!IHHIIIs', data_len, pcode, entity, repeat2, len2, codeC, data)
    print(f'Server Sending to the client: data_length: {data_len} code: {pcode} entity: {entity} repeat2: {repeat2} len2: {len2} codeC: {codeC}')
    connectionSocket.send(server_packet)
    break

print('------------ End of Stage C    ------------')

time.sleep(3)
if len2 % 4 != 0:
    Rem = len2 % 4 
    len2 = 4 - Rem + len2

print('------------ Starting Stage D  ------------')
print('Starting to receive packets from client')

repeat_counter = 0


while repeat_counter < repeat2:
    try:
        server_packet = connectionSocket.recv(1024)
        server_packet_unpacked = struct.unpack(f'!IHH{len2}s', server_packet)
        data = server_packet_unpacked[3].decode()
        repeat_counter += 1 
        print(f'repeat_counter = {repeat_counter} data_len: {server_packet_unpacked[0]} pcode: {server_packet_unpacked[1]} entity: {server_packet_unpacked[2]} data: {data}')
    except: 
        break
    
#DEFINITIONS
data_len = struct.calcsize('I')
pcode = codeC
entity = 2
codeD = random.randint(100, 400)

#PACKING
server_packet = struct.pack('!IHHI', data_len, pcode, entity, codeD)

#Sending connections to the server
connectionSocket.send(server_packet)

#Close connections
connectionSocket.close()
serverSocket.close()  
sys.exit()  # Terminate the program after sending the corresponding data


