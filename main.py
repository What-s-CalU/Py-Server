'''
| ACSC/ACET - 492 - 001 - What's@Calu - Server Side Code (main.py)
| Edited on February 26th, 2023.
'''




import global_values            as glob

import handlers.http_handler      as http_h
import handlers.http_handler_util as http_util_h

import handlers.json_handler     as json_h
import handlers.server_handler   as serv_h
import handlers.email_handler    as email_h
import handlers.sql_handler      as sql_h
import handlers.scraper_handler  as scrape_h

import handlers.hardware_handler as hardware_h

import http
import time


# handler for the program.
def main():
    # startup code here ...
    
    # Make threads
    serverRequestThread = serv_h.CALUServerhandlerThread()
    serverRequestThread.daemon = True
    
    webScrapingThread  = scrape_h.CALUWebScraperThread()
    webScrapingThread.daemon = True
    
    hardwareHandlerThread = hardware_h.CALUHardwareManagerThread()
    hardwareHandlerThread.daemon = True


    # Public facing HTTP control.
    #* this can be set to False to deny service while the server is updating. 
    glob.SERVER_IS_UP = True
    glob.SCRAPER_UP   = True

    # run threads
    serverRequestThread.start()
    webScrapingThread.start()
    hardwareHandlerThread.start()
    
    # Keeps main alive (no rogue threads on exit)
    try:
        while True:
            # loop through the databases for logged in users, reset passwords, etc. This function deletes expired entries. 
            # manage_timesheet("SELECT NAME AND TIME FROM SIGNUP","DELETE FROM SIGNUP WHERE NAME IS ? AND TIME IS ?")
            # manage_timesheet("SELECT NAME AND TIME FROM RESET","DELETE FROM RESET WHERE NAME IS ? AND TIME IS ?")

            time.sleep(1)
    except KeyboardInterrupt:
        return 0
    
def manage_timesheet(get_query:str, delete_query:str, timeout:int=240):
        userdata_query_signup =  sql_h.sql_execute_safe_search(
            "database/root.db",
            get_query,
            ())
        current = userdata_query_signup.fetchone()
        flipflop = False
        while(current != None):

            # grabs entries from the shared results. 
            name = current
            current = userdata_query_signup.fetchone()
            time = current

            # checks to see if the query would expire.
            if((int(time) + timeout) <= int(time.time())):
                sql_h.sql_execute_safe_insert(
                "database/root.db",
                delete_query,
                (name, time))
            current = userdata_query_signup.fetchone()

# autoruns main. 
if __name__ == "__main__":
    main()

