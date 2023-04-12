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
        while True:
            if glob.SCRAPER_UP:
                url = "http://calu.edu/news/announcements/"
                response = requests.get(url)

                if response.status_code == 200:
                    response_parsed = BeautifulSoup(str(response.text), 'html.parser')
                    events = response_parsed.find_all('tr')

                    if events != None:
                        for event in events:
                            i = 0
                            event_data = event.find_all('td')

                            if event_data != None:
                                for data in event_data:
                                    if i == 0:
                                        thread_h.s_print(data)
                                    elif i == 1:
                                        thread_h.s_print(data)
                                    elif i == 2:
                                        thread_h.s_print(data)
                                    else:
                                        thread_h.s_print("Unexpected Value.")
                                    i += 1
                print("Scraped Successfully.")
                glob.SCRAPER_UP = False