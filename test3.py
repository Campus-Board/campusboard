__author__ = 'mac'

import django
django.setup()
"""
from Interaction.collector_stack import YowsupEchoStack
login = '5519987185426'
pw = 'VknCLpa74rWBhsDaPhKKx8Z704A='
credentials = (login, pw)
stack = YowsupEchoStack(credentials)
stack.start()
"""
from Data.message import Message
msgs = Message.objects.all()
for msg in msgs:
    print msg

from Data.models import User

def show_users():
    for user in User.objects.all():
        print user.alias
        print user.bluetooth_id
        print user.phone_number
        print "================="