from django.core.management import BaseCommand, CommandError
from realty_management.models import Unit


import requests
import lxml
from lxml import html, etree
from lxml.cssselect import CSSSelector
import time, datetime

apartment_details = []
# scrape_url = 'http://chambana.craigslist.org/search/apa'
scrape_url = 'http://chambana.craigslist.org/'
class Command(BaseCommand):
    help = 'Scrapes the sites for new dockets'
    def handle(self, *args, **options):
        self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))
        print 'scraping site: ' + scrape_url + 'search/apa'
        r = requests.get(scrape_url + 'search/apa')
        # build the DOM Tree
        tree = lxml.html.fromstring(r.text)
        # construct a CSS Selector
        sel = CSSSelector('p.row a')
        # Apply the selector to the DOM tree.
        results = sel(tree)
        print results
        # get the text out of all the results
        data = [str(result.get('href')) for result in results]
        data = [str(scrape_url + result) for result in data if result != 'None']
        print data
        print '='*20

        for index, link in enumerate(list(set(data))):
    
            # debugging
            if index > 3:
                break
    
            print 'scraping ' + link
            r = requests.get(link)
            tree = lxml.html.fromstring(r.text)
            sel = CSSSelector('p.attrgroup span')
            results = sel(tree)
            '''
            match = results[1]
            sqft = gettext(lxml.html.tostring(match))

    
            sel = CSSSelector('span.price')
            results = sel(tree)
            match = results[0]
            price = lxml.html.tostring(match)[21:-8]
            # print 'price', price
    
            if price.isdigit() and sqft > 0:
                #print {'sqft':sqft, 'cost':int(price)}
                apartment_details.append({'sqft':sqft, 'cost':int(price)})
            else:
                print 'not a digit...'
            print '='*20
            '''

 
now = time.gmtime(time.time())
 
def convertTime(t):
   """Converts times in format HH:MMPM into seconds from epoch (but in CST)"""
   convertedTime = time.strptime(t + ' ' + str(now.tm_mon) + ' ' + str(now.tm_mday) + ' ' + str(now.tm_year), "%I:%M%p %m %d %Y")
   return time.mktime(convertedTime)
   # This used to add 5 * 60 * 60 to compensate for CST



