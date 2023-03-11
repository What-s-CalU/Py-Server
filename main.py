'''
| ACSC/ACET - 492 - 001 - What's@Calu - Server Side Code (main.py)
| Edited on February 26th, 2023.
'''




import global_values           as glob
import handlers.http_handler   as http_h
import handlers.json_handler   as json_h
import handlers.server_handler as serv_h
import http
import time


# handler for the program.
def main():
    # startup code here ...
    
    # Make threads
    serverRequestThread = serv_h.CALUServerhandlerThread()


    # Public facing HTTP control.
    #* this can be set to False to deny service while the server is updating. 
    glob.SERVER_IS_UP = True

    # run threads
    serverRequestThread.start()
    
    return 0



# autoruns main. 
if __name__ == "__main__":
    main()

