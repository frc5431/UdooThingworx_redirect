from SocketServer import UDPServer, BaseRequestHandler
from datetime import datetime
from ThingWorx import ThingWorx
from json import loads, dumps

BIND_ADDR = ""
BIND_PORT = 5830
worx = ThingWorx()
worx_thing = "RobotData"

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

print "Starting Udoo side of robotics server"
print "Default header length %d" % HEADER_LEN


def data_handle(raw):
    try:
        raw = str(raw)
        striped = raw[raw.index(SOF) + len(SOF):raw.index(EOF)]
        inner = striped[HEADER_LEN:striped.index(PROP_MULTI)]
        type = striped[striped.index(PROP_MULTI) + len(PROP_MULTI):striped.index(PROP_MULTI_EOF)]
        content = striped[striped.index(PROP_MULTI_EOF) + len(PROP_MULTI_EOF):]
        time_stamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        if PROP_PUT in striped:
            print "Got PUT header"
            if "JSON" in type.upper():
                to_load = loads(content)
                to_load['timestamp'] = time_stamp
                print "Formulated timestamp"
            else:
                to_load = {inner: content, 'timestamp': time_stamp}
                print "Arced timestamp"
            print "Loaded json %s" % dumps(to_load)
            response_code = worx.put_property(to_load)
            print "Put response code %d" % response_code
            toret = "OK" if response_code == 200 else "ERR_RESPONSE"
            print "Sending response %s" % toret
            return toret
        elif PROP_GET in striped:
            print "Got GET header"
            if len(inner) > 0:
                return worx.get_property(inner)
            else:
                return worx.get_property()
        else:
            print "Not a valid request!"
    except (IOError, TypeError, OSError, ValueError, IndexError), err:
        print "Error parsing request data: %s" % err
        return "ERR"


class UDPHandle(BaseRequestHandler):
    def handle(self):
        addr = self.client_address
        sock = self.request[1]
        resp = ""
        try:
            raw_data = str(self.request[0]).strip().replace('\n', '')
            if EOF not in raw_data or SOF not in raw_data:
                print "Failed to pull entire stream..."
                sock.sendto(ON_FAIL, addr)
                return
            print "From (%s): %s" % (str(addr), raw_data)
            resp = data_handle(raw_data)
            sock.sendto(SOF + resp + EOF, addr)
        except (OSError, ValueError, TypeError, IOError), err:
            print "UDP handle error: %s" % err
            sock.sendto(SOF + resp + EOF, addr)


if __name__ == "__main__":
    worx.set_thing(worx_thing)
    server = UDPServer((BIND_ADDR, BIND_PORT), UDPHandle)
    server.allow_reuse_address = True
    print "Starting server...\nwaiting for data..."
    server.serve_forever()
