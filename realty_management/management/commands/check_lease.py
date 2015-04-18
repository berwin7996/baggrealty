from django.core.management import BaseCommand, CommandError
from realty_management.models import Property, LivesIn
from datetime import datetime, timedelta

class Command(BaseCommand):
	def handle(self, *args, **options):
		properties = Property.objects.all()
		for p in properties:
			todayplusthirty = datetime.now() + timedelta(days=30)
	        contracts = LivesIn.objects.filter(unit_number__in=p.get_owned_units())
	        for c in contracts:
	            if todayplusthirty > c.lease_end:
	                #end email if date is 30 before end of lease
	                message = send_mail('LEASE EXPIRING SOON', '', 'baggrealty@gmail.com', ['baggrealty@gmail.com'], fail_silently=False)
