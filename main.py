'''
| ACSC/ACET - 492 - 001 - What's@Calu - Server Side Code (main.py)
| Edited on April 23nd, 2023.
'''




import global_values            as glob
import handlers.server_handler   as serv_h
import handlers.sql_handler      as sql_h
import handlers.scraper_handler  as scrape_h
import datetime
import handlers.hardware_handler as hardware_h

import time


# handler for the program.
def main():
    glob.SCRAPER_UP   = True

    # Hardware Threads
    hardwareHandlerThread = hardware_h.CALUHardwareManagerThread()
    hardwareHandlerThread.daemon = True
    hardwareHandlerThread.start()

    # Server Threads
    serverRequestThread = serv_h.CALUServerhandlerThread()
    serverRequestThread.daemon = True
    serverRequestThread.start()
    
    # Scraper Threads
    webScrapingThread  = scrape_h.CALUWebScraperThread()
    webScrapingThread.daemon = True
    webScrapingThread.start() 

    
    # Keeps main alive (no rogue threads on exit)
    try:
        while True:
            # loop through the databases for logged in users, reset passwords, etc. This function deletes expired entries.
            manage_tokens()
            time.sleep(1)
    except KeyboardInterrupt:
        return 0
    
    return 0


# probably should aquire a lock specific to the sql database. 
def manage_tokens():
        manage_timesheet(
            """SELECT
                SIGNUP.NAME as name,
                SIGNUP.TIME as time,
                SIGNUP.ID   as id
                FROM SIGNUP""",
            "DELETE FROM SIGNUP WHERE NAME IS ? AND TIME IS ? AND ID IS ?")
        manage_timesheet(
            """SELECT
                RESET.NAME as name,
                RESET.TIME as time,
                RESET.ID   as id
                FROM RESET""",
            "DELETE FROM RESET WHERE NAME IS ? AND TIME IS ? AND ID IS ?")
        manage_timesheet(
            """SELECT
                LOGIN.NAME as name,
                LOGIN.TIME as time,
                LOGIN.ID   as id
                FROM LOGIN""",
            "DELETE FROM LOGIN WHERE NAME IS ? AND TIME IS ? AND ID IS ?", 80)


def manage_timesheet(get_query:str, delete_query:str, timeout:int=240):
        userdata_query_signup =  sql_h.sql_execute_safe_search(
            "database/root.db",
            get_query,
            ())
        # iterates through the entire list of entries for their current times and names. 

        userdata_return = userdata_query_signup.fetchall()
        for current in userdata_return:
            if(current[0] != None):
                # grabs entries from the shared results. 
                table_name = current[0]
                table_time = current[1]
                table_id   = current[2]

                # checks to see if the query would expire.
                if((float(table_time) + timeout) <= float(time.time())):
                    print("[MAIN] <Invalidating token for \"{}\".>".format(table_name))
                    sql_h.sql_execute_safe_insert(
                    "database/root.db",
                    delete_query,
                    (table_name, table_time, table_id))
                current = userdata_query_signup.fetchone()



# autoruns main. 
if __name__ == "__main__":
    main()

