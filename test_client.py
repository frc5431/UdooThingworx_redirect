import socket

BIND_ADDR = "127.0.0.1"
BIND_PORT = 5830

'''
LOADING HEADERS LEFT NAME
EACH HEADER HAS A UNIQUE UID
'''
PROP_PUT = "0x00"
PROP_GET = "0xA1"
HEADER_LEN = len(PROP_PUT)

'''
COMPOSER STRINGS
SEPARATIONS BETWEEN PROP_NAME AND JSON
'''
PROP_MULTI = "<DATA-TYPE>"
PROP_MULTI_EOF = "<EOF-TYPE>"

'''
SOCKET-UPDATE PACKETS
START AND STOP OF STREAMS
'''
EOF = "<STREAM:EOF>"
SOF = "<STREAM:SOF>"
ON_FAIL = "<STREAM:ERR>"

MESSAGE = SOF + PROP_PUT + "" + PROP_MULTI + "JSON" + PROP_MULTI_EOF + "{\"xangle\": \"15\"}" + EOF

print "UDP target IP:", BIND_ADDR
print "UDP target port:", BIND_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (BIND_ADDR, BIND_PORT))
print sock.recvfrom(1024)