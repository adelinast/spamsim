#!/usr/bin/python

import smtplib
import logging
import sys

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class SmtpMailClient():
	def __init__(self, serverName, port):
		self.serverName=serverName
		self.port=port
		
	def send(self, sender, recipients, msg):
		logz.info("Sending Message")
		#sock=smtplib.socket.create_connection(('127.0.0.1', 1025,), timeout, ('',0))
		client=smtplib.SMTP(self.serverName, self.port)
		client.set_debuglevel(True) # show communication with the server
		try:
			client.sendmail(sender, recipients, msg.as_string())
			logz.debug("Success sending message")
		except:
			logz.error("Error sending message")
		finally:
			client.quit()
			logz.debug("Client quit")
