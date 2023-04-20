
import global_values              as glob
import handlers.http_handler      as http_h
import handlers.json_handler      as json_h
import handlers.threading_handler as thread_h
import http.server
import threading


# The HTTP send<->recieve element of What's@Calu
class CALUServerhandlerThread(threading.Thread):
    def run(self):
        # what the constructor for the server's http request socket looks like
        myServerSocketRequest = http_h.ParsingHandler
        with http.server.ThreadingHTTPServer((glob.SERVER_PORT_ADDRESS, glob.SERVER_PORT_NUMBER), myServerSocketRequest) as myServerSocket:
            thread_h.s_print("[SERVER] <serving PORT {}>:\n".format(str(glob.SERVER_PORT_NUMBER)))
            myServerSocket.serve_forever()
