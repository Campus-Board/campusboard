__author__ = 'mac'

import smtplib
to = 'jmendozais@gmail.com'
gmail_user = 'mail.campusboard@gmail.com'
gmail_pwd = 'Campusboard1'
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
print header
msg = header + '\n this is test msg from mkyong.com \n\n'
smtpserver.sendmail(gmail_user, to, msg)
print 'done!'
smtpserver.close()