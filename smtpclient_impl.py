#!/usr/bin/python
import sys
import logging
import os
import socket

import utils
import extract_data
from extract_data import Data
from sender import Sender

ADDRESS_LIST = {'default': ['recipient1@localhost.ro', 'recipient2@localhost.ro', 'test@localhost.com'],
	}
MAXIMUM_NUMBER_OF_ATTEMPTS=2
A_COUPLE_OF_SECONDS=2

SRC=""
CONF="conf"
DATE=os.path.join(SRC, CONF, 'dates.conf')
FIELDS=os.path.join(SRC, CONF, 'fields.conf')

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def usage():
	print "Usage: python %s --host=hostname --port=port" %sys.argv[0]
	sys.exit(1)

if __name__ == "__main__":
	
	if len(sys.argv)<2 or len(sys.argv)>3:
		usage()
	
	hostname="localhost"
	if len(sys.argv)>=2:
		ip_address=sys.argv[1][(len("--host")+1):]
		#(hostname, aliaslist, ipaddrlist)=socket.gethostbyaddr(ip_address)
		hostname=socket.getfqdn(ip_address)
		print hostname

	port=1025
	if len(sys.argv)==3:
		port=sys.argv[2][(len("--port")+1):]

	mbox=None
	data=Data()

	#smtpMailsink = SmtpMailsink(host=hostname, mailboxFile=mbox)
	#smtpMailsink.start()

	extract_data.loadConfFile(DATE, data)
	extract_data.loadFieldsConfFile(FIELDS, data)
	
	randomDate=utils.get_random(data.date)
	randomFrom=utils.get_random(data.from_list)
	randomRcptList=utils.get_random(data.rcpt_list)
	randomSubject=utils.get_random(data.subject_list)
	hasText=True
	bodyPlainText=utils.get_random(data.plainTexts)
	bodyHtmlText=""
	hasHtml=False
	
	sender=Sender(hostname, port, randomFrom.mailFrom, randomRcptList.rcpt, randomSubject.subject, 
				randomDate, hasHtml, hasText, bodyPlainText.plainText, bodyHtmlText)
	sender.run()

