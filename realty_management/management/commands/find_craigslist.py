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
        r = requests.get(scrape_url + 'search/apa')
        # build the DOM Tree
        tree = lxml.html.fromstring(r.text)
        # construct a CSS Selector
        sel = CSSSelector('p.row a')
        # Apply the selector to the DOM tree.
        results = sel(tree)
        #print results
        # get the text out of all the results
        data = [str(result.get('href')) for result in results]
        data = [str(scrape_url + result) for result in data if result != 'None']
        
        populate_details(data)

        # average price of all the apartments
        prices = [float(apt['cost']) for apt in apartment_details]
        avg_price = sum(prices)/(len(prices)+0.01)
        print avg_price

        avgs = Unit.objects.raw('SELECT "realty_management_unit"."num_bed", "realty_management_unit"."num_baths", AVG("realty_management_unit"."rent") AS avg FROM "realty_management_unit"')
        print avgs[0]

 
now = time.gmtime(time.time())
 
def convertTime(t):
   """Converts times in format HH:MMPM into seconds from epoch (but in CST)"""
   convertedTime = time.strptime(t + ' ' + str(now.tm_mon) + ' ' + str(now.tm_mday) + ' ' + str(now.tm_year), "%I:%M%p %m %d %Y")
   return time.mktime(convertedTime)
   # This used to add 5 * 60 * 60 to compensate for CST

def populate_details(data):
	# go through links to get info
    for index, link in enumerate(list(set(data))):

        # debugging
        if index > 10:
            break

        print 'scraping ' + link
        r = requests.get(link)
        tree = lxml.html.fromstring(r.text)
        #print lxml.html.tostring(tree)
        sel = CSSSelector('p.attrgroup span')
        results = sel(tree)

        match = results[0]
        #print lxml.html.tostring(match)
        br, ba = gettext(lxml.html.tostring(match))
        #print 'br', br, 'ba', ba
        #break

        sel = CSSSelector('span.price')
        results = sel(tree)
        match = results[0]
        price = lxml.html.tostring(match)[21:-8]
        print 'price', price
        if price.isdigit():
        	apartment_details.append({'br':br, 'ba':ba, 'cost':price})
        else:
        	print 'not a digit...'

# for br ba
def gettext(source):
    '''
    <span><b>1</b>BR / <b>1</b>Ba</span> 
    '''
    # print type(source)
    source = etree.fromstring(source)
    # print etree.tostring(source)
    etree.strip_tags(source, 'b', 'span')
    newstr = etree.tostring(source)
    br = newstr.split('/')[0].split('>')[1]
    ba = newstr.split('/')[1].split('<')[0]

    br = br[:-2] # remove Br
    ba = ba[:-2] # remove Ba

    try:
        br = int(br)
    except:
        br = 1
    try:
        ba = int(ba)
    except:
        ba = 1

    return br, ba
