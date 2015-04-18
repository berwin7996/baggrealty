from django.core.management.core import BaseCommand, CommandError
from realty_management.models import Property, LivesIn

class Command(BaseCommand):
	def handle(self, *args, **options):
		properties = Property.objects.get()
		for p in property:
			c.check_expire()