'''
    couples http handling with 'beautifulsoup' to simplify http parsing into structures for use by whats@calu
    https://www.geeksforgeeks.org/python-web-scraping-tutorial/
'''
import threading
import handlers.http_handler as http_h

# we use datastructures from this module. 
import http


# webscraper's tasks as a thread (which can be ran/released periodically via main)
class CALUWebScraperThread(threading.Thread):
    def run(self):
        url = 'localhost'
        response = http_h.do_GET_from_url(url)
        print(response.msg)