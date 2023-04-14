'''
    couples http handling with 'beautifulsoup' to simplify http parsing into structures for use by whats@calu
    to install soup on an instance, type `pip install beautifulsoup4`
    to install requests on an instance, type 'pip install requests'
    https://www.geeksforgeeks.org/python-web-scraping-tutorial/
'''
import threading
from bs4 import BeautifulSoup
import requests
import datetime
import dateparser

import handlers.http_handler      as http_h
import handlers.threading_handler as thread_h 
import handlers.http_handler_util as http_util_h
import global_values              as glob



# we use datastructures from these modules: http, bs4, threading

# webscraper's tasks as a thread (which can be ran/released periodically via main)
class CALUWebScraperThread(threading.Thread):
    def run(self):
        event_name:  str = ""
        event_desc:  str = ""
        
        # time value fields 
        event_start: datetime.datetime
        event_end:   datetime.datetime

        event_time:  str = ""


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

                                    # time posted (fallback event time if desc has no dates)
                                    if i == 0:
                                        event_time  = data.get_text()
                                        print(event_time)
                                        event_start = datetime.datetime.fromisoformat(event_time)

                                    # description and time start parsing (time end is midnight for all events with a start time)
                                    elif i == 1:
                                        event_name = data.get_text()
                                        print(event_name)
                                        if(data) != None:
                                            event_desc = ""
                                            data_response        = requests.get("https://www.calu.edu" + data.find('a')['href'])
                                            data_response_parsed = BeautifulSoup(str(data_response.text), 'html.parser')
                                            data_anchor          = data_response_parsed.find('div', class_='b-band__inner')
                                            data_body            = data_anchor.get_text().split('\n')
                                            j = 0
                                            for data_line in data_body:
                                                if(j >= 5):
                                                        date_parsed = dateparser.parse(data_line)
                                                        # print(date_parsed)
                                                        event_desc = event_desc + data_line + "\n"
                                                else:
                                                    j+=1
                                            print(event_desc)
                                    # event sender (maps to categories via a dictionary)
                                    elif i == 2:
                                        event_sender = data.get_text()
                                        print(event_sender)
                                    
                                    # error handler.
                                    else:
                                        thread_h.s_print("Unexpected Value.")
                                    i += 1
                                
                                # add event via insert or ignore.
                                # http_util_h.insert_new_event(start_time, end_time, event_name, color, event_desc, category_id, False, None, 0)
                print("Scraped Successfully.")
                glob.SCRAPER_UP = False