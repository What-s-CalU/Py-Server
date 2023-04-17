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
# import dateparser

import handlers.http_handler      as http_h
import handlers.threading_handler as thread_h 
import handlers.http_handler_util as http_util_h
import global_values              as glob



# we use datastructures from these modules: http, bs4, threading

# webscraper's tasks as a thread (which can be ran/released periodically via main)
class CALUWebScraperThread(threading.Thread):
    def run(self):
        skipped_first: bool = False
        event_name:  str = None
        event_desc:  str = None
        category_id: str = None
        
        # time value fields 
        event_start: datetime.datetime = None
        event_end:   datetime.datetime = None

        event_time:  str = None

        print(glob.SCRAPER_CATEGORY_FIELDS)

        # Runs while the scraper is up.
        # The thread is always running, which allows us to start glob.SCRAPER_UP up arbitrarily. 
        while True:
            if glob.SCRAPER_UP:
                skipped_first = False
                url = "http://calu.edu/news/announcements/"
                response = requests.get(url)

                if response.status_code == 200:
                    response_parsed = BeautifulSoup(str(response.text), 'html.parser')
                    events = response_parsed.find_all('tr')

                    if events != None:
                        for event in events:
                            if(skipped_first):
                                i = 0
                                event_data = event.find_all('td')

                                if event_data != None:
                                    for data in event_data:

                                        # time posted (fallback event time if desc has no dates)
                                        if i == 0:
                                            event_time  = data.get_text()
                                            # print(event_time)

                                            # fallback date. 
                                            event_start = datetime.datetime.fromisoformat(event_time)
                                            event_start = datetime.datetime(event_start.year, event_start.month, event_start.day, hour=0,minute=0,second=0)

                                            event_end   = datetime.datetime.fromisoformat(event_time)
                                            event_end   = datetime.datetime(event_start.year, event_start.month, event_start.day, hour=23,minute=59,second=0)
                                            

                                        # description and time start parsing (time end is midnight for all events with a start time)
                                        elif i == 1:
                                            event_name  = data.get_text().strip()
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
                                                            # date_parsed = dateparser.parse(data_line)
                                                            # print(date_parsed)
                                                            event_desc = event_desc + data_line + "\n"
                                                    else:
                                                        j+=1
                                                # print(event_desc)
                                        # event sender (maps to categories via a dictionary)
                                        elif i == 2:
                                            event_sender = data.get_text().strip()
                                            category_id = ""
                                            try:
                                                category_id = glob.SCRAPER_CATEGORY_FIELDS[event_sender]
                                            except KeyError:
                                                category_id = 18
                                        
                                        # error handler.
                                        else:
                                            thread_h.s_print("Unexpected Value.")
                                        i += 1
                                
                                    http_util_h.insert_new_calu_event(str(event_start.isoformat()), str(event_end.isoformat()), event_name, event_desc, category_id, False, None, 0)
                                    # send an http update??? The client could just do this via a refresh button and automatic refreshing; I'm not sure if http allows us to just 
                                    # send data like that without a thread constantly listening like this server does on every client.
                            else:
                                skipped_first = True
                print("Scraped Successfully.")
                glob.SCRAPER_UP = False