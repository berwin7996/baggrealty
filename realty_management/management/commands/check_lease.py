from django.core.management import BaseCommand, CommandError
from realty_management.models import Property, LivesIn
from datetime import datetime, timedelta
from django.core.mail import send_mail

class Command(BaseCommand):
    def handle(self, *args, **options):
        properties = Property.objects.all()
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
                    message = send_mail('LEASE EXPIRING SOON', 'testing an email', 'baggrealty@gmail.com', ['baggrealty@gmail.com'], fail_silently=False)
            print('========================')
