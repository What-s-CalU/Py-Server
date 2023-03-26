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
        code:    int = 400
        message: str = "Bad Request"
        data:    str = "{\"INFO\":200}"


        if(glob.SERVER_IS_UP):
            # example from http read code
            client_data: dict = json_h.json_load_string(self.http_body_to_string())

            # test query for correct username and password.
            client_query =  sql_h.sql_execute_search(
                "database/root.db",
                "SELECT NAME " +
                "FROM USERS "                +
                "WHERE NAME IS \"" + client_data["name"].upper() + "\" AND PASS IS \"" + client_data["password"]+"\"")
  

            # check to see if the query returned anything (IE, what we were looking for is int he database)
            if(client_query.fetchone() != None):
                code    = 200
                message = "OK"
        else:
            code    = 503
            message = "Service Unavailable"
            
        
        # construct the server's response to the client. 
        self.do_ANY_send_response(code, message, data)


    def do_GET(self):
        self.do_ANY_send_response(501, "Not Implemented", "")


    def do_HEAD(self):
        self.do_ANY_send_response(501, "Not Implemented", "")



        