from django.core.management import BaseCommand, CommandError
from realty_management.models import Property, LivesIn
from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC5152ba3e4bd9ec69b732ecb2f840de26" 
AUTH_TOKEN = "e72ea0df11834ac6fe678d8debb4bb26" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 

class Command(BaseCommand):
    def handle(self, *args, **options):
        properties = Property.objects.all()
        foundcontract = False
        bodymsg = ''
        for p in properties:
            print('checking contracts for ' + p.address)
            todayplustwenty = date.today() + timedelta(days=25)
            todayplusforty = date.today() + timedelta(days=35)
            contracts = LivesIn.objects.filter(unit_number__in=p.get_owned_units())
            for c in contracts:
                print('time right now + 25 days: ' + str(todayplustwenty))
                print('lease end time: ' + str(c.lease_end.date()))
                print('time right now + 35 days: ' + str(todayplusforty))
                if todayplustwenty < c.lease_end.date() and c.lease_end.date() < todayplusforty:
                    #end email if date is 30 before end of lease
                    foundcontract = True
                    print(p.address, c.unit_number)
                    bodymsg += 'Your property at ' + str(p.address) + ' ' + str(c.unit_number) + ' has a lease expiring on ' + str(c.lease_end.date()) + ' for tenant named: ' + ''.join([i for i in str(c.main_tenant) if not i.isdigit()]) + '\n\n\n'
                    print('----------')
        #only sends one email per day with summary of which properties are expiring
        if foundcontract:
            message = send_mail('LEASE EXPIRING SOON', bodymsg, 'baggrealty@gmail.com', ['baggrealty@gmail.com'], fail_silently=False)
            client.messages.create(
                to="2245580568", 
                from_="+16302837104", 
                body=bodymsg,  
            )

            print('========================')
