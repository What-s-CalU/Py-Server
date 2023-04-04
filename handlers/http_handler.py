'''
    Basic wrapper functions for serving http requests (and infering data from them).
    List of HTTP Responses: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses
'''


import http.server
import handlers.json_handler      as     json_h
import handlers.sql_handler       as     sql_h
import global_values              as     glob
from   handlers.email_handler     import send_email
import time
import random, string

#
# Utility functions used by the parse handler that are -technically- agnostic of the handler.
#

# Simple function taken from sth on stackoverflow.
# https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python
def generate_checksum(length:int):
    result: str = ""
    choice_pool = string.ascii_uppercase

    # actually generates the checksum.
    result = result.join(random.choice(choice_pool) for i in range(length))
    return result


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


    # hackmey object-namespace variables we use for decoupled functions/as an impromptu data structure.
    # technically not a part of structured programming, but they make passing values between functions easier notationally. 
    dopost_code:    int = 400
    dopost_message: str = "Bad Request"
    dopost_data:    str = "{\"INFO\":200}"


#
# Utility functions used by the parse handler. 
#
    def set_response_header(self, code, message):
        self.dopost_code    = code
        self.dopost_message = message

    # converts an http request object into a string (could probably write to an intermediate file instead for less ram usage)
    def http_body_to_string(self):
        post_length: int = int(self.headers['Content-length'])
        return self.rfile.read(post_length)


    # Sends a templated http response constructed in do_POST().
    def do_ANY_send_response(self, code: int, message: str, data: str):
        self.send_response(code, message)
        self.end_headers()
        self.wfile.write(data.encode())


#
# Query handling code for the python server backend. 
#

    # handles POST requests from clients; IE, the only requests the application makes. 
    # task-specific code that touches the datapase are all prefixed with do_POST, and outlined below this. 
    def do_POST(self):
        self.set_response_header(400, "Bad Request")
        self.dopost_data    = "{\"INFO\":200}"

        # example from http read code
        client_data: dict = json_h.json_load_string(self.http_body_to_string())
        
        if(glob.SERVER_IS_UP):

            # switch statement for event mapping.

            # signin
            if(client_data['request_type']   == "signin"):
                self.do_POST_signin(client_data)

            # account creation block
            elif(client_data['request_type'] == "signup_start"):
                self.do_POST_signup_start(client_data)
            elif(client_data['request_type'] == "signup_continue"):
                self.do_POST_signup_continue(client_data)
            elif(client_data['request_type'] == "signup_end"):
                self.do_POST_signup_end(client_data)
            
            # password reset block
            elif(client_data['request_type'] == "reset_start"):
                self.do_POST_reset_start(client_data)
            elif(client_data['request_type'] == "reset_continue"):
                self.do_POST_reset_continue(client_data)
            elif(client_data['request_type'] == "reset_end"):
                self.do_POST_reset_end(client_data)
            
            # catchall
            else:
                self.set_response_header(506, "Not Acceptable")
        # catchall for no service. 
        else:
            self.set_response_header(503, "Service Unavailable")
            
        
        # construct the server's response to the client. 
        self.do_ANY_send_response(self.dopost_code, self.dopost_message, self.dopost_data)



    # Handles requests for a user to sign into the application.
    # Expects username (email handle) and password fields. 
    def do_POST_signin(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()
            # password is case sensitive, and thus is ignored. 
            
            
            # test query for correct username and password.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT NAME FROM USERS WHERE NAME IS ? AND PASS IS ?",
                (client_data["username"], client_data["password"]))
  

            # check to see if the query returned anything (IE, what we were looking for is int he database)
            if(client_query.fetchone() != None):
                self.set_response_header(200, "OK")
            # incorrect password or username; no access is granted. 
            else:
                self.set_response_header(401, "Unauthorized")



    def do_POST_signup_start(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()
            
            # test query for any present users already signed up.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT NAME FROM USERS WHERE NAME IS ?",
                (client_data["username"],))

            # check to see if the query returned anything (none = no user)
            if(client_query.fetchone() == None):

                # test query for any present users waiting to sign up.
                client_query =  sql_h.sql_execute_safe_search(
                    "database/root.db",
                    "SELECT NAME FROM SIGNUP WHERE NAME IS ?",
                    (client_data["username"],))
                
                if(client_query.fetchone() == None):
                    # prepare information to be inserted into the database. 
                    client_checksum: str = generate_checksum(10)

                    # seconds since epoch, easy to parse. 
                    client_time:     int = time.time()
                    
                    # actually insert the time. 
                    # format taken from https://www.sqlitetutorial.net/sqlite-python/insert/
                    sql_h.sql_execute_safe_insert(
                        "database/root.db",
                        "INSERT INTO SIGNUP(NAME, CHECKSUM, TIME) VALUES(?, ?, ?)",
                        (client_data["username"], client_checksum, client_time))

                    # For console logs; printed alongside email query.
                    print(client_data['username']+"@pennwest.edu" + " registered with checksum: " + client_checksum + ".\n")
                    send_email(
                            client_data['username']+"@pennwest.edu",
                            "Your What's@Calu Verification Code",
                            "Your What's@Calu Verification Code is:\n\""+ client_checksum+"\",\nDo not share this code with anyone. What's@Calu will never ask you to generate this code for use outside of the What's@Calu Planner app.")
                    
                    # request is OK, return to client. 
                    self.set_response_header(200, "OK")

                # this client already is signed up or queued to sign up; cannot begin the signin process again. 
                else:
                    self.set_response_header(401, "Unauthorized")
            
            # this client already is signed up or queued to sign up; cannot begin the signin process again. 
            else:
                self.set_response_header(401, "Unauthorized")


    def do_POST_signup_continue(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()

            # test query for correct username and password.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT NAME FROM SIGNUP WHERE NAME IS ? AND CHECKSUM IS ?",
               (client_data["username"], client_data["checksum"])) 
  

            # check to see if the query returned anything (IE, what we were looking for is in the database)
            if(client_query.fetchone() != None):
                self.set_response_header(200, "OK")
            # incorrect checksum (user cannot edit their username by this point).
            else:
                self.set_response_header(401, "Unauthorized")


    def do_POST_signup_end(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()

            # repeat the checks for continuing. 
            self.do_POST_signup_continue(client_data)
            if(self.dopost_code == 200):
                # assign these new user values to the database. 
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    "INSERT INTO USERS(NAME, PASS) VALUES(?, ?)",
                    (client_data["username"], client_data["password"])) 
            
                # delete the temporary signup value. User is now signed up.
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    "DELETE FROM SIGNUP WHERE NAME IS ? AND CHECKSUM IS ?",
                    (client_data["username"], client_data["checksum"]))
            
            # Otherwise, the user is not valid (we reuse the checksum to -try- to prevent a man in the middle attack/mass signups).
            else:
                self.set_response_header(401, "Unauthorized")



    def do_POST_reset_start(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()
            
            # test query for any present users already signed up.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT NAME FROM USERS WHERE NAME IS ?",
                (client_data["username"],))

            # check to see if the query returned anything (none = no user)
            if(client_query.fetchone() != None):

                # test query for any present users waiting to sign up.
                client_query =  sql_h.sql_execute_safe_search(
                    "database/root.db",
                    "SELECT NAME FROM RESET WHERE NAME IS ?",
                    (client_data["username"],))
                
                if(client_query.fetchone() == None):
                    # prepare information to be inserted into the database. 
                    client_checksum: str = generate_checksum(10)

                    # seconds since epoch, easy to parse. 
                    client_time:     int = time.time()
                    
                    # actually insert the time. 
                    # format taken from https://www.sqlitetutorial.net/sqlite-python/insert/
                    sql_h.sql_execute_safe_insert(
                        "database/root.db",
                        "INSERT INTO RESET(NAME, CHECKSUM, TIME) VALUES(?, ?, ?)",
                        (client_data["username"], client_checksum, client_time))

                    # For console logs; printed alongside email query.
                    print(client_data['username']+"@pennwest.edu" + " registered with checksum: " + client_checksum + ".\n")
                    send_email(
                            client_data['username']+"@pennwest.edu",
                            "Your What's@Calu Password Reset Code",
                            "Your What's@Calu Password Reset Code is:\n\""+ client_checksum+"\",\nDo not share this code with anyone. What's@Calu will never ask you to generate this code for use outside of the What's@Calu Planner app.")
                    
                    # request is OK, return to client. 
                    self.set_response_header(200, "OK")

                # this client already is signed up or queued to sign up; cannot begin the signin process again. 
                else:
                    self.set_response_header(401, "Unauthorized")
            
            # this client already is signed up or queued to sign up; cannot begin the signin process again. 
            else:
                self.set_response_header(401, "Unauthorized")


    def do_POST_reset_continue(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()

            # test query for correct username and password.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT NAME FROM RESET WHERE NAME IS ? AND CHECKSUM IS ?",
               (client_data["username"], client_data["checksum"])) 
  

            # check to see if the query returned anything (IE, what we were looking for is in the database)
            if(client_query.fetchone() != None):
                self.set_response_header(200, "OK")
            # incorrect checksum (user cannot edit their username by this point).
            else:
                self.set_response_header(401, "Unauthorized")


    def do_POST_reset_end(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()

            # repeat the checks for continuing. 
            self.do_POST_reset_continue(client_data)
            if(self.dopost_code == 200):
                # assign these new user values to the database. 
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    "UPDATE USERS SET NAME=?, PASS=? WHERE NAME=?",
                    (client_data["username"], client_data["password"], client_data["username"])) 
            
                # delete the temporary signup value. User is now signed up.
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    "DELETE FROM RESET WHERE NAME IS ? AND CHECKSUM IS ?",
                    (client_data["username"], client_data["checksum"]))
            
            # Otherwise, the user is not valid (we reuse the checksum to -try- to prevent a man in the middle attack/mass signups).
            else:
                self.set_response_header(401, "Unauthorized")




    # we do not implement proper HTTP protocol, so it's unimplemented here. 
    def do_GET(self):
        self.do_ANY_send_response(501, "Not Implemented", "")

    def do_HEAD(self):
        self.do_ANY_send_response(501, "Not Implemented", "")


