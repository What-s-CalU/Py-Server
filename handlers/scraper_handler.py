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
import time
# import dateparser

import handlers.http_handler      as http_h
import handlers.threading_handler as thread_h 
import handlers.http_handler_util as http_util_h
import global_values              as glob



# we use datastructures from these modules: http, bs4, threading

# webscraper's tasks as a thread (which can be ran/released periodically via main)
class CALUWebScraperThread(threading.Thread):
    def run(self):

        # Lie to the connections we make about what the info is for,
        # this is the only way to prevent an abort when scraping. 
        headers = {
            "User-Agent":                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language":           "en-US,en;q=0.5",
            "Accept-Encoding":           "gzip, deflate, br",
            "Connection":                "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest":            "document",
            "Sec-Fetch-Mode":            "navigate",
            "Sec-Fetch-Site":            "cross-site"
        }
        skipped_first: bool = False
        event_name:    str = None
        event_desc:    str = ""
        category_id:   str = None
        
        # time value fields 
        event_start: datetime.datetime = None
        event_end:   datetime.datetime = None

        event_time:  str = None

        scrapee: requests.Session = requests.Session()

        finished_init: bool = False
        scrape_done: bool   = False
        do_not_fill: bool   = False
        was_updated: bool   = False
        data_anchor = None
        last_scraped: float = time.time()

        events_updated = []
        thread_h.s_print("[SCRAPER] <Current Webscraping Nametable>:")
        for value in glob.SCRAPER_CATEGORY_FIELDS:
            thread_h.s_print(("[SCRAPER] <{}>".format(value)))

        # Runs while the scraper is up.
        # The thread is always running, which allows us to start glob.SCRAPER_UP up arbitrarily. 
        while True:
            if glob.SCRAPER_UP:
                scrape_done = False
                # Fetch events from the database
                skipped_first = False
                url = "http://calu.edu/news/announcements/"
                while(not(finished_init)): 
                    try:
                        # Prevents against connection aborts from the host.
                        time.sleep(0.10)
                        response = scrapee.get(url, headers=headers, timeout=4.35)
                        finished_init   = True
                    except requests.exceptions.ReadTimeout:
                        thread_h.s_print("[SCRAPER] [ERROR] <Connection timed out; attempting reconnection.>")
                        continue



                if response.status_code == 200:


                    response_parsed = BeautifulSoup(str(response.text), 'html.parser')
                    events = response_parsed.find_all('tr')


                    # hardcoded checks for whether or not events equals none.
                    if events != None:
                        for event in events:
                            if(skipped_first and not(scrape_done)):
                                i = 0
                                event_data = event.find_all('td')

                                if event_data != None:
                                    for data in event_data:
                                        # time posted (fallback event time if desc has no dates)
                                        if i == 0:
                                            event_time  = data.get_text().encode('ascii',errors='ignore').decode('ascii')
                                            # print(event_time)

                                            # fallback date. 
                                            event_start = datetime.datetime.fromisoformat(event_time)
                                            event_start = datetime.datetime(event_start.year, event_start.month, event_start.day, hour=0,minute=0,second=0)

                                            event_end   = datetime.datetime.fromisoformat(event_time)
                                            event_end   = datetime.datetime(event_start.year, event_start.month, event_start.day, hour=23,minute=59,second=0)
                                            

                                        # description and time start parsing (time end is midnight for all events with a start time)
                                        elif i == 1:
                                            was_updated = False
                                            event_name  = data.get_text().strip().encode('ascii',errors='ignore').decode('ascii')
                                            thread_h.s_print("[SCRAPER] [EVENT] <Viewing \"{}\".>".format(event_name))

                                            for event_title in events_updated:
                                                if(str(event_title) == event_name):
                                                    was_updated = True

                                            # Don't try to sent an http request for an event we already updated. 
                                            if(not(was_updated)):

                                                # Don't try to evaluate a regex we know is null
                                                if(data) != None:
                                                        
                                                        # Setup loop controls for the description grabber. 
                                                        finished_body = False
                                                        do_not_fill = False
                                                        data_anchor = None

                                                        # Loop so long as we've not gotten a description.
                                                        while(not(finished_body)):
                                                            event_desc = ""
                                                            url_body   = "https://www.calu.edu" + data.find('a')['href']
                                                            try:
                                                                time.sleep(6.00)
                                                                data_response        = scrapee.get(url_body, headers=headers, timeout=4.35)
                                                                data_response_parsed = BeautifulSoup(str(data_response.text), 'html.parser')
                                                                data_anchor          = data_response_parsed.find('div', class_='b-band__inner')
                                                            
                                                            # Bail whenever the connection times out to keep the announcements page happy
                                                            except requests.exceptions.ReadTimeout:
                                                                thread_h.s_print("[SCRAPER] [ERROR] <Connection timed out; skipping description.>")
                                                                finished_body = True
                                                                do_not_fill = True
                                                            
                                                            # Loop if we didn't run into the data_anchor and the server would be fine with reconnection.
                                                            if(data_anchor == None and not(do_not_fill)):
                                                                finished_body = False
                                                            
                                                            # Evaluate the description. 
                                                            else:
                                                                data_body            = data_anchor.get_text().split('\n')
                                                                j = 0
                                                                for data_line in data_body:
                                                                    if(j >= 5):
                                                                            # date_parsed = dateparser.parse(data_line)
                                                                            # print(date_parsed)
                                                                            event_desc = event_desc + data_line.encode('ascii',errors='ignore').decode('ascii') + "\n"
                                                                    else:
                                                                        j+=1
                                                                finished_body = True

                                            # Dummy out the description, as we don't need it. 
                                            else:
                                                event_desc = ""
                                                

                                        # event sender (maps to categories via a dictionary)
                                        elif i == 2:
                                            event_sender = data.get_text().strip().encode('ascii',errors='ignore').decode('ascii')
                                            category_id = ""
                                            try:
                                                category_id = glob.SCRAPER_CATEGORY_FIELDS[event_sender]
                                            except KeyError:
                                                category_id = 18
                                        
                                        # error handler.
                                        else:
                                            thread_h.s_print("[SCRAPER] [ERROR] <Unexpected values in <tr> body.>")
                                        i += 1
                                
                                    scrape_done = http_util_h.insert_new_calu_event(str(event_start.isoformat()) + ".000", str(event_end.isoformat()) + ".000", event_name, event_desc, category_id, False, None, 0, events_updated, do_not_fill)
                                    # send an http update??? The client could just do this via a refresh button and automatic refreshing; I'm not sure if http allows us to just 
                                    # send data like that without a thread constantly listening like this server does on every client.
                            else:
                                skipped_first = True
                thread_h.s_print("[SCRAPER] <Scraped Successfully. Next scrape scheduled in 24 hours.>")
                glob.SCRAPER_UP   = False
                glob.SERVER_IS_UP = True
                
            # waits until the server can scrape again. 
            else:
                if((float(last_scraped) + 86400) < time.time()):
                    last_scraped = time.time()
                    glob.SCRAPER_UP   = True
                    glob.SERVER_IS_UP = False
                time.sleep(1)
                   