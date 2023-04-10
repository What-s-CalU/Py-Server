'''
    couples http handling with 'beautifulsoup' to simplify http parsing into structures for use by whats@calu
    to install soup on an instance, type `pip install beautifulsoup4`
    to install requests on an instance, type 'pip install requests'
    https://www.geeksforgeeks.org/python-web-scraping-tutorial/
'''
import threading
import handlers.http_handler      as http_h
import handlers.threading_handler as thread_h 
import global_values              as glob
from bs4 import BeautifulSoup
import requests


# we use datastructures from these modules: http, bs4, threading

# webscraper's tasks as a thread (which can be ran/released periodically via main)
class CALUWebScraperThread(threading.Thread):
    def run(self):
        while(True):
            if(glob.SCRAPER_UP):
                # constant URL for this webscraper. This is could be a constant, but is rather bare where it is. 
                url:    str = "http://calu.edu/news/announcements/"
                response = requests.get(url)

                # Check to see if the response is valid. 
                if(response.status_code == 200):
                    # parse response into chunks for analysis.
                    response_parsed = BeautifulSoup(str(response.text), 'html.parser')
                    events          = response_parsed.find('tr')


                    # find the event name and event(s) of each dropdown
                    for event in events:
                        i = 0
                        event_data = event.find('td')
                        
                        for data in event_data:
                            if(i == 0):
                                thread_h.s_print(data)
                                # copy the name
                            elif(i==1):
                                # resolve the description via another function
                                thread_h.s_print(data)
                            elif(i==2):
                                thread_h.s_print(data)
                            else:
                                thread_h.s_print("Unexpected Value.")
                                # copy the person who wrote it (or map them to an event category???
                            # increment for context. 
                            i+=1
                print("Scraped Successfully.")
                glob.SCRAPER_UP = False