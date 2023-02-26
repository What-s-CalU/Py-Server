'''
| ACSC/ACET - 492 - 001 - What's@Calu - Server Side Code (main.py)
| Edited on February 11th, 2023.
'''

import http.server
import json
import threading
import time
import sqlite3
import http.client


'''

class FakeClientThread(threading.Thread):
    def run(self):
        time.sleep(3)
        url = 'localhost'
        client_connection = http.client.HTTPSConnection(host=url, port=80)
        client_connection.request("POST", url, "{USERNAME:JohnDoe, PASSWORD:passWord1}")
        client_connection_response = client_connection.getresponse()
        client_connection.close()
        print(client_connection_response.msg)
'''


class ParsingHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        post_length = int(self.headers['Content-length'])

        # read into a string here? We could also read a character at a time here. 
        # print(self.rfile.read(post_length))
        data = json.loads(self.rfile.read(post_length))
        print(data['username'] + "; " + data['password'])
        self.send_response(200, "OK")
        self.end_headers()
        # parsing can be handled post read here. 
        self.wfile.write("serverside data")


SERVER_PORT_ADDRESS = 'localhost'
SERVER_PORT_NUMBER  = 80


# handler for the program.
def main():
    
    
    # what the structure for incoming requests looks like. 
    # this class has a controller for when a connection is to be closed, close_connection. 
    # this class has storage for components of the request, including:
    # - requestline (the request), requestversion (the version of http being used),
    # - command (the request type),
    # - path, the request's path. 

    # rfile (optional input data from the client) (called using handle())
    # wfile (output stream to write a response to the client)  (called using send_response() and send_header())

    # what the constructor for the server's http request socket looks like
    myServerSocketRequest = ParsingHandler
    with http.server.ThreadingHTTPServer((SERVER_PORT_ADDRESS, SERVER_PORT_NUMBER), myServerSocketRequest) as myServerSocket:
        print("serving PORT " + str(SERVER_PORT_NUMBER) + ":\n")
        myServerSocket.serve_forever()
    # ideally we never get here. Though the server crashes if interrupted, so it might be better to have a loop control/control for threads.
    return 0




# autoruns main. 
if __name__ == "__main__":
    main()

