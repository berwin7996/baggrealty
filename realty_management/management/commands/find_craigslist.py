from django.core.management import BaseCommand, CommandError
from realty_management.models import Unit

import requests
import lxml
from lxml import html

apartments = {}

class Command(BaseCommand):
     help = 'Scrapes the sites for new dockets'
     def handle(self, *args, **options):
         self.stdout.write('\nScraping started at %s\n' % str(datetime.datetime.now()))
         craigslist = {'chambana': 'http://chambana.craigslist.org/search/apa'}
         for list, url in craigslist.iteritems():
             self.stdout.write('Scraping url: %s\n' % url)
             r = requests.get(url)
             root = lxml.html.fromstring(r.content)
             # 
             for row in root.cssselect('p[class="row"] a'):
             	print row

 
 now = time.gmtime(time.time())
 
 def convertTime(t):
     """Converts times in format HH:MMPM into seconds from epoch (but in CST)"""
     convertedTime = time.strptime(t + ' ' + str(now.tm_mon) + ' ' + str(now.tm_mday) + ' ' + str(now.tm_year), "%I:%M%p %m %d %Y")
     return time.mktime(convertedTime)
     # This used to add 5 * 60 * 60 to compensate for CST
 