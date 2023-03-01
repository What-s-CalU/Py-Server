'''
| ACSC/ACET - 492 - 001 - What's@Calu - Server Side Code (main.py)
| Edited on February 26th, 2023.
'''




import global_values         as glob
import handlers.http_handler as http_h
import handlers.json_handler as json_h
import http


# handler for the program.
def main():

    
    # what the constructor for the server's http request socket looks like
    myServerSocketRequest = http_h.ParsingHandler
    with http.server.ThreadingHTTPServer((glob.SERVER_PORT_ADDRESS, glob.SERVER_PORT_NUMBER), myServerSocketRequest) as myServerSocket:
        print("serving PORT " + str(glob.SERVER_PORT_NUMBER) + ":\n")
        myServerSocket.serve_forever()
    # ideally we never get here. Though the server crashes if interrupted, so it might be better to have a loop control/control for threads.
    return 0



# autoruns main. 
if __name__ == "__main__":
    main()

