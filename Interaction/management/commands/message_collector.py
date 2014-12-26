from django.core.management.base import BaseCommand, CommandError
from Interaction.collector_stack import YowsupEchoStack
import time
class Command(BaseCommand):
    help = 'wassap collector deamon'

    def handle(self, *args, **options):
        login = '5519987185426'
        pw = 'VknCLpa74rWBhsDaPhKKx8Z704A='
        credentials = (login, pw)
        stack = YowsupEchoStack(credentials)
        stack.start()
        self.stdout.write('There are {} things!'.format(MyModel.objects.count()))