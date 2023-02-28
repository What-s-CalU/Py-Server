'''
    Basic wrapper functions for serving http requests (and infering data from them).
    List of HTTP Responses: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses
'''

import http.server
import handlers.json_handler as json_h
import handlers.sql_handler  as sql_h



# returns a GET http response from a website. 
def do_GET_from_url(url, port=80):
    client_connection = http.client.HTTPSConnection(host=url, port=port)
    client_connection.request("GET", url)
    client_connection_response = client_connection.getresponse()
    client_connection.close()
    return client_connection_response








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


    # converts an http request object into a string (could probably write to an intermediate file instead for less ram usage)
    def http_body_to_string(self):
        post_length = int(self.headers['Content-length'])
        return self.rfile.read(post_length)


    def do_POST_send_response(self, code, message, data):
        self.send_response(code, message)
        self.wfile.write(data)
        self.end_headers()


    def do_POST(self):
        code    = 200
        message = "OK"
        data    = "{'INFO':200}"


        # example from http read code
        client_data = json_h.json_load_string(self.http_body_to_string())

        # test query for correct username and password. 
        query_results = sql_h.sql_execute_search
        (
            "SELECT ID,NAME,PASSWORD " +
            "FROM USERS " +
            "WHERE NAME IS " + client_data['name'] + "AND PASS IS "+client_data['password']
        )
        
        # response if the query returned anything
        if(not(query_results)):
            code    = 400
            message = "Bad Request"

        # construct the server's response to the client. 
        self.do_POST_send_response(code, message, data)




        