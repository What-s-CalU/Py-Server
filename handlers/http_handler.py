'''
    Basic wrapper functions for serving http requests (and infering data from them).
'''

import http.server
import json_handler as json_h




# returns a GET http response from a website. 
def do_GET_from_url(url, port=80):
    client_connection = http.client.HTTPSConnection(host=url, port=port)
    client_connection.request("GET", url)
    client_connection_response = client_connection.getresponse()
    client_connection.close()
    return client_connection_response


# converts an http request object into a string (could probably write to an intermediate file instead for less ram usage)
def http_to_string(target):
    post_length = int(target.headers['Content-length'])
    return target.rfile.read(post_length)





# what the structure for incoming requests looks like. 
# this class has a controller for when a connection is to be closed, close_connection. 
# this class has storage for components of the request, including:
# - requestline (the request), requestversion (the version of http being used),
# - command (the request type),
# - path, the request's path. 

# rfile (optional input data from the client) (called using handle())
# wfile (output stream to write a response to the client)  (called using send_response() and send_header())

class ParsingHandler(http.server.BaseHTTPRequestHandler):
    # handles POST requests from clients. 
    # this doesn't seem to need to return anything, but ideally should be coupled with an object that's tied to main/the server. 
    def do_POST(self):

        # example from http read code
        data = json_h.json_load_string(http_to_string(self))

        data

        # example write code to send back to the client (ideally is json/other relevant information)
        self.wfile.write("serverside data")

        # send response to client
        self.send_response(200, "OK")
        self.end_headers()

