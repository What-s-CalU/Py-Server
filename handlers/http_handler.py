'''
    Basic wrapper functions for serving http requests (and infering data from them).
    List of HTTP Responses: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses
'''


import http.server
import handlers.json_handler      as     json_h
import handlers.sql_handler       as     sql_h
import handlers.http_handler_util as     util_h
import global_values              as     glob
from   handlers.email_handler     import send_email
import handlers.threading_handler as thread_h
import time
import random, string
#
# Utility functions used by the parse handler that are -technically- agnostic of the handler.
#

# Simple function taken from sth on stackoverflow.
# https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python
def generate_checksum(length:int=10):
    result: str = ""
    choice_pool = string.ascii_uppercase

    # actually generates the checksum.
    result = result.join(random.choice(choice_pool) for i in range(length))
    return result


def check_checksum(client_data):
    # rectify username. 
    client_data["username"] = client_data["username"].upper()

    value: bool = False
    # wrapped in a try loop (realistically we'll never call this without the right client_data)
    try:
        # look for a logged in user.
        client_query =  sql_h.sql_execute_safe_search(
        "database/root.db",
        "SELECT NAME FROM LOGIN WHERE NAME IS ? AND CHECKSUM IS ?",
        (client_data["username"], client_data["checksum"]))
        
        # update the time the user was last active in the login table, if so.
        if(client_query.fetchone() != None):
            value = True
            # assign these new user values to the database.
            client_time:     str = str(time.time())
            sql_h.sql_execute_safe_insert(
            "database/root.db",
            "UPDATE LOGIN SET NAME=?, TIME=? WHERE NAME=?",
            (client_data["username"], client_time, client_data["username"]))

    # return false for invalid data or a false check. 
    except KeyError:
        value = False
    return value


# returns a GET http response from a website.
def do_GET_from_url(url:str, port:int):
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
        # Try to update the display with the latest http serve message. 
        thread_h.update_notifications("Served HTTP Response: \"{}\", Code: {}.".format(message, code), code, True)

        # Write the server response. 
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
        has_requested = False
        # example from http read code
        client_data: dict = json_h.json_load_string(self.http_body_to_string())
        
        if(glob.SERVER_IS_UP):
            has_requested = False
            # switch statement for event mapping.

            # signin
            if(client_data['request_type']   == "signin"):
                has_requested = True
                self.do_POST_signin(client_data)

            # account creation block
            elif(client_data['request_type'] == "signup_start"):
                has_requested = True
                self.do_POST_signup_start(client_data)
            elif(client_data['request_type'] == "signup_continue"):
                has_requested = True
                self.do_POST_signup_continue(client_data)
            elif(client_data['request_type'] == "signup_end"):
                has_requested = True
                self.do_POST_signup_end(client_data)
            
            # password reset block
            elif(client_data['request_type'] == "reset_start"):
                has_requested = True
                self.do_POST_reset_start(client_data)
            elif(client_data['request_type'] == "reset_continue"):
                has_requested = True
                self.do_POST_reset_continue(client_data)
            elif(client_data['request_type'] == "reset_end"):
                has_requested = True
                self.do_POST_reset_end(client_data)

            # block for logged in userevents. 
            # only a user that passes through signin/signup_end/reset_end can get here. 
            if(check_checksum(client_data)):
                # make custom events
                # add event
                if(client_data['request_type'] == "add_custom_event"):
                    self.do_POST_add_custom_event(client_data)
                # get events
                # send user events to the client.
                elif(client_data['request_type'] == "get_user_subscribed_events"):
                    self.do_POST_get_user_subscribed_events(client_data)
                # send category names and subscribe status
                elif(client_data['request_type'] == "get_calu_category_names"):
                    self.do_POST_get_calu_category_names(client_data)
                elif(client_data['request_type'] == "edit_custom_event"):
                    self.do_POST_edit_custom_event(client_data)
                elif (client_data['request_type'] == "delete_event"):
                    self.do_POST_delete_user_event(client_data)


                # get calu events
                #update category subscription
                elif(client_data['request_type'] == "update_calu_category_subscription"):
                    self.do_POST_update_calu_category_subscription(client_data)   
                # get events for calu category
                elif (client_data['request_type'] == "get_calu_category_events"):
                    self.do_POST_get_calu_category_events(client_data)
                # catchall

                #categories
                elif(client_data['request_type'] == "get_user_subscribed_categories"):
                    self.do_POST_get_user_subscribed_categories(client_data) 
                elif(client_data['request_type'] == "add_category"):
                    self.do_POST_insert_category(client_data) 
                #delete category
                elif(client_data['request_type'] == "delete_category"):
                    self.do_POST_delete_category_and_associated_data(client_data)

                elif(client_data['request_type'] == "signout"):
                    self.do_POST_signout(client_data)

                #edit event
                elif client_data['request_type'] == "edit_event":
                    self.do_POST_edit_event(client_data)

                    
                    
            else:
                if(has_requested == False):
                    self.set_response_header(506, "Not Acceptable")
        # catchall for no service. 
        else:
            self.set_response_header(503, "Service Unavailable")
            
        
        # construct the server's response to the client. 
        self.do_ANY_send_response(self.dopost_code, self.dopost_message, self.dopost_data)

    
    def do_POST_delete_category_and_associated_data(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Get category_id from client_data
        category_id = client_data["category_id"]

        # Call the delete_category_and_associated_data function
        util_h.delete_category_and_associated_data(user_id, category_id)

        # Set response header and message
        self.set_response_header(200, "OK")


    def do_POST_edit_event(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Edit the event in the EVENTS table
        updated_event = util_h.edit_event(
            client_data['start_time'],
            client_data['end_time'],
            client_data['title'],
            client_data['description'],
            client_data['category_id'],
            client_data['is_custom'],
            user_id,
            None,
            client_data['event_id']
        )

        self.dopost_data = json_h.json_dump_string(updated_event)
        self.set_response_header(200, "OK")

    def do_POST_insert_category(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Insert the new category into the CATEGORIES table
        category_id = util_h.insert_new_category(
            user_id,
            client_data['color'],
            client_data['category_name']
        )
        
        util_h.insert_new_user_category_subscription(
            user_id,
            category_id
        )

        self.dopost_data = json_h.json_dump_string({"category_id": category_id})
        self.set_response_header(200, "OK")

    def do_POST_get_user_subscribed_categories(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Get user-subscribed categories
        user_subscribed_categories = util_h.get_user_subscribed_categories(user_id)
        self.dopost_data = json_h.json_dump_string(user_subscribed_categories)
        print(self.dopost_data)
        self.set_response_header(200, "OK")



    def do_POST_delete_user_event(self, client_data):
        util_h.delete_user_event(
            client_data['event_id']
        )

        self.set_response_header(200, "OK")

    
    def do_POST_get_calu_category_events(self, client_data):
        category_events = util_h.get_calu_category_events(client_data["category_id"])
        self.dopost_data = json_h.json_dump_string(category_events)
        print(self.dopost_data)
        self.set_response_header(200, "OK")


    def do_POST_update_calu_category_subscription(self, client_data):
        client_data["username"] = client_data["username"].upper()
        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return
        
        category_id = client_data["category_id"]

        if(client_data["is_subscribed"] == 1):
        # Insert new user category subscription
            util_h.insert_new_user_category_subscription(user_id, category_id)
        if(client_data["is_subscribed"] == 0):
            util_h.delete_user_category_subscription(user_id, category_id)

        self.set_response_header(200, "OK")

    def do_POST_get_calu_category_names(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Get the list of categories with null user_id
        categories_data = util_h.get_categories_with_subscription_status(user_id)

        # Convert the list of categories to a JSON string and put it in post data
        self.dopost_data = json_h.json_dump_string(categories_data)

        self.set_response_header(200, "OK")


    # Handles requests for all events users a subscribe to
    def do_POST_get_user_subscribed_events(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Get the list of events the user is subscribed to
        user_subscribed_events = util_h.get_user_subscribed_events(user_id)

        # Convert the list of events to a JSON string and put it in post data
        self.dopost_data = json_h.json_dump_string(user_subscribed_events)
        print(self.dopost_data)
        self.set_response_header(200, "OK")



    
    # Handles requests to add a user created event
    def do_POST_add_custom_event(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Get category_id from CATEGORIES table
        category_id = client_data["categoryID"]

        if category_id is None:
            self.set_response_header(400, 'Category ID not provided')
            return

        # Insert the custom event into the EVENTS table
        event_id = util_h.insert_new_event(
            client_data['start_time'],
            client_data['end_time'],
            client_data['title'],
            client_data['description'],
            category_id,
            client_data['isCustom'],
            user_id,
            None
        )
        self.dopost_data = json_h.json_dump_string(event_id)
        self.set_response_header(200, "OK")



    # Handles requests to add a user created event
    def do_POST_edit_custom_event(self, client_data):
        client_data["username"] = client_data["username"].upper()

        # Get user_id from USERS table
        user_id = util_h.get_user_id(client_data["username"])
        if user_id is None:
            self.set_response_header(400, 'User not found')
            return

        # Get category_id from CATEGORIES table
        category_id = client_data["categoryID"]

        if category_id is None:
            self.set_response_header(400, 'Category ID not provided')
            return

        # Insert the custom event into the EVENTS table
        event_id = util_h.edit_event(
            client_data['start_time'],
            client_data['end_time'],
            client_data['title'],
            client_data['description'],
            category_id,
            client_data['isCustom'],
            user_id,
            None,
            client_data['event_id']
        )
        self.dopost_data = json_h.json_dump_string(event_id)
        self.set_response_header(200, "OK")




    # Handles requests for a user to sign into the application.
    # Expects username (email handle) and password fields. 
    def do_POST_signin(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()
            # password is case sensitive, and thus is ignored. 
            
            
            # test query for correct username and password.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT ID FROM USERS WHERE NAME IS ? AND PASS IS ?",
                (client_data["username"], client_data["password"]))
  
            id = client_query.fetchone()
            # check to see if the query returned anything (IE, what we were looking for is in the database)
            if(id != None):
                checksum = generate_checksum()
                self.dopost_data = "{\"id\": " + str(id[0]) + ", \"checksum\":\"" + checksum + "\"}"
                print(self.dopost_data)
                self.set_response_header(200, "OK")

                # seconds since epoch, easy to parse. 
                client_time:     str = str(time.time())
                
                # actually insert the time. 
                # format taken from https://www.sqlitetutorial.net/sqlite-python/insert/
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    "INSERT INTO LOGIN(NAME, CHECKSUM, TIME) VALUES(?, ?, ?)",
                    (client_data["username"], checksum, client_time))



            # incorrect password or username; no access is granted. 
            else:
                self.set_response_header(401, "Unauthorized")



    # Handles requests for a user to log out of the application.
    def do_POST_signout(self, client_data):
            # rectify username. 
            client_data["username"] = client_data["username"].upper()
            
            
            # test query for correct username and password.
            client_query =  sql_h.sql_execute_safe_search(
                "database/root.db",
                "SELECT NAME FROM LOGIN WHERE NAME IS ? AND CHECKSUM IS ?",
                (client_data["username"], client_data["checksum"]))
  
            id = client_query.fetchone()
            # check to see if the query returned anything (IE, what we were looking for is in the database)
            if(id != None):
                # delete the temporary login value. User is now logged out.
                sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    "DELETE FROM LOGIN WHERE NAME IS ? AND CHECKSUM IS ?",
                    (client_data["username"], client_data["checksum"]))
                self.set_response_header(200, "OK")
                
            # invalid user; access not granted. 
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
                    client_time:     str = str(time.time())
                    
                    # actually insert the time. 
                    # format taken from https://www.sqlitetutorial.net/sqlite-python/insert/
                    sql_h.sql_execute_safe_insert(
                        "database/root.db",
                        "INSERT INTO SIGNUP(NAME, CHECKSUM, TIME) VALUES(?, ?, ?)",
                        (client_data["username"], client_checksum, client_time))

                    # For console logs; printed alongside email query.
                    print(client_data['username'] + " registered with checksum: " + client_checksum + ".\n")
                    send_email(
                            client_data['username'],
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
                    client_time:     str = str(time.time())
                    
                    # actually insert the time. 
                    # format taken from https://www.sqlitetutorial.net/sqlite-python/insert/
                    sql_h.sql_execute_safe_insert(
                        "database/root.db",
                        "INSERT INTO RESET(NAME, CHECKSUM, TIME) VALUES(?, ?, ?)",
                        (client_data["username"], client_checksum, client_time))

                    # For console logs; printed alongside email query.
                    print(client_data['username'] + " reset with checksum: " + client_checksum + ".\n")
                    send_email(
                            client_data['username'],
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


