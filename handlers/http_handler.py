'''
    Basic wrapper functions for serving http requests (and infering data from them).
    List of HTTP Responses: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses
'''


import http.server
import handlers.json_handler      as json_h
import handlers.sql_handler       as sql_h
import global_values              as glob
import handlers.threading_handler as thread_h



# returns a GET http response from a website. 
def do_GET_from_url(url:str, port:int=80):
    client_connection: http.client.HTTPSConnection = http.client.HTTPSConnection(host=url, port=port)
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


    dopost_code:    int = 400
    dopost_message: str = "Bad Request"
    dopost_data:    str = "{\"INFO\":200}"



    # converts an http request object into a string (could probably write to an intermediate file instead for less ram usage)
    def http_body_to_string(self):
        post_length: int = int(self.headers['Content-length'])
        return self.rfile.read(post_length)

    # Sends a templated http response constructed in do_POST().
    def do_ANY_send_response(self, code: int, message: str, data: str):
        

        # manually converts our data into a blob of bytes for wfile.write(). 
        # *This method cannot accept a normal string that isn't a literal, for whatever reason. 
        self.send_response(code, message)
        # self.wfile.write(bytes(data, 'utf-8'))
        self.end_headers()



    # handles POST requests from clients. 
    # this doesn't seem to need to return anything, but ideally should be coupled with an object that's tied to main/the server. 
    def do_POST(self):
        self.dopost_code    = 400
        self.dopost_message = "Bad Request"
        self.dopost_data    = "{\"INFO\":200}"

        # example from http read code
        client_data: dict = json_h.json_load_string(self.http_body_to_string())
        
        if(glob.SERVER_IS_UP):

            if(client_data['request_type'] == "signin"):
                self.do_POST_signin(client_data)
            elif(client_data['request_type'] == "signup_start"):
                self.do_POST_signup_start(client_data)
        else:
            self.dopost_code    = 503
            self.dopost_message = "Service Unavailable"
            
        
        # construct the server's response to the client. 
        self.do_ANY_send_response(self.dopost_code, self.dopost_message, self.dopost_data)



    def do_POST_signin(self, client_data):

            # test query for correct username and password.
            client_query =  sql_h.sql_execute_search(
                "database/root.db",
                "SELECT NAME " +
                "FROM USERS "                +
                "WHERE NAME IS \"" + client_data["username"].upper() + "\" AND PASS IS \"" + client_data["password"]+"\"")
  

            # check to see if the query returned anything (IE, what we were looking for is int he database)
            if(client_query.fetchone() != None):
                self.dopost_code    = 200
                self.dopost_message = "OK"

    def do_POST_signup_start(self, client_data):

            # test query for correct username and password.
            client_query =  sql_h.sql_execute_search(
                "database/root.db",
                "SELECT NAME " +
                "FROM USERS "                +
                "WHERE NAME IS \"" + client_data["username"].upper() + "\" AND PASS IS \"" + client_data["password"]+"\"")
  

            # check to see if the query returned anything (IE, what we were looking for is int he database)
            if(client_query.fetchone() != None):
                self.dopost_code    = 200
                self.dopost_message = "OK"


    def do_GET(self):
        self.do_ANY_send_response(501, "Not Implemented", "")


    def do_HEAD(self):
        self.do_ANY_send_response(501, "Not Implemented", "")



