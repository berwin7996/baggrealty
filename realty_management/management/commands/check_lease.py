from django.core.management import BaseCommand, CommandError
from realty_management.models import Property, LivesIn
from datetime import datetime, timedelta
from django.core.mail import send_mail

class Command(BaseCommand):
    def handle(self, *args, **options):
        properties = Property.objects.all()
        foundcontract = False
        for p in properties:
            print('checking contracts for ' + p.address)
            todayplusthirty = datetime.now() + timedelta(days=30)
            contracts = LivesIn.objects.filter(unit_number__in=p.get_owned_units())
            for c in contracts:
                print('time right now + 30 days: ' + str(todayplusthirty.replace(tzinfo=None)))
                print('lease end time: ' + str(c.lease_end.replace(tzinfo=None)))
                if todayplusthirty.replace(tzinfo=None) > c.lease_end.replace(tzinfo=None):
                    #end email if date is 30 before end of lease
                    print(p.address, c.unit_number)
                    bodymsg = 'Your property at ' + str(p.address) + ' unit number ' + str(c.unit_number) + ' has a lease expiring on ' + str(c.lease_end.replace(tzinfo=None) + '\n')
        #only sends one email per day with summary of which properties are expiring
        if foundcontract:
            message = send_mail('LEASE EXPIRING SOON', bodymsg, 'baggrealty@gmail.com', ['baggrealty@gmail.com'], fail_silently=False)
            print('========================')
