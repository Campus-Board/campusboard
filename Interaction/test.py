#from yowsup.demos.echoclient.stack import YowsupEchoStack
from collector_stack import YowsupEchoStack

#5519987185426:VknCLpa74rWBhsDaPhKKx8Z704A=
login = '5519987185426'
pw = 'VknCLpa74rWBhsDaPhKKx8Z704A='
credentials = (login, pw)
stack = YowsupEchoStack(credentials)
stack.start()