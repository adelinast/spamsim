#!/usr/bin/python

import smtpd
import mailbox
import email.Parser

class SmtpMailServer(smtpd.SMTPServer):
	def __init__(self, *args, **kwargs):
		smtpd.SMTPServer.__init__(self, *args, **kwargs)
		self.mailboxFile = None

	def setMailboxFile(self, mailboxFile):
		self.mailboxFile = mailboxFile

	def process_message(self, peer, mailfrom, rcpttos, data):
		if self.mailboxFile is not None:
			#print "-----------"+peer
			inheaders = 1
			lines = data.split('\n')
			print '---------- MESSAGE FOLLOWS ----------'
			for line in lines:
				# headers first
				if inheaders and not line:
					print 'X-Peer:', peer[0]
				inheaders = 0
			print line
			print '------------ END MESSAGE ------------'
			mbox=self.mailboxFile
			parser = email.Parser.Parser()
			#parse data and complete fields
			msg = parser.parsestr(data)
			id = msg.get('Message-ID','')
			date = msg.get('Date','')
			subject = msg.get('Subject','')
			payload = msg.get_payload(decode=1)
			charset = msg.get_charset()
			content_type=msg.get_content_type()
			print payload
			mbox.lock()
			try:
				msg = mailbox.mboxMessage()				
				msg['From'] = mailfrom
				msg['To'] = rcpttos
				msg['Subject']=subject				
				msg['Message-ID']=id
				msg['Date']=date
				msg.set_charset(charset)
				msg.set_payload(payload)
				msg.set_type(content_type)
				mbox.add(msg)
				mbox.flush()
			finally:
				mbox.unlock()			
				