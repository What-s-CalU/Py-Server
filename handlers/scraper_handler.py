'''
    couples http handling with 'beautifulsoup' to simplify http parsing into structures for use by whats@calu
    to install soup on an instance, type `pip install beautifulsoup4`
    https://www.geeksforgeeks.org/python-web-scraping-tutorial/
'''
import threading
import handlers.http_handler as http_h
import bs4                   as soup_h


# we use datastructures from these modules: http, bs4, threading

# webscraper's tasks as a thread (which can be ran/released periodically via main)
class CALUWebScraperThread(threading.Thread):
    def run(self):
        # constant URL for this webscraper. This is could be a constant, but is rather bare where it is. 
        url: str = "https://www.pennwest.edu/academics/academic-calendar"
        response = http_h.do_GET_from_url(url)

        # Check to see if the response is valid. 
        if(response.getcode() == 200):
            # parse response into chunks for analysis. 
            response_parsed = soup_h(str(response.msg), 'html.parser')
            events          = response_parsed.find('div', class_='accordion-item-w-dropdown')

            # find the event name and event(s) of each dropdown
            for event_category in events:
                event_category_name     = event_category.find('div', class_='text-block-174')
                event_category_contents = event_category.find('div', class_='w-richtext')
                for event in event_category_contents:
                    # from here, the contents in <strong> would become event category names (and be compared against the database),
                    # <p> are the day(s) of the events, in the format WEEKDAY, MONTH DAY 
                    # ^ delimiting <p> by only parsing what is after the "," would be ideal.
                    # the web formatting is also all over the place for these. see "Summer 2023" to get an idea of what I mean
                    # it may be better to manually add these events instead, giving it throught; since the website has changed a lot even
                    # just in the past year. 
                    print(event_category_name + ": " + event + "\n")