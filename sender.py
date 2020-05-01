import errno
import time

from smtpclient import SmtpMailClient
from create_mail import Mail

MAXIMUM_NUMBER_OF_ATTEMPTS=2
A_COUPLE_OF_SECONDS=2

class Sender():
    
    def __init__(self, hostname, port, randomFrom, recipientList, randomSubject, randomDate, hasHtml, hasText, bodyPlainText, bodyHtmlText):
        self.hostname=hostname
        self.port=port
        self.randomFrom=randomFrom
        self.recipientList=recipientList
        self.randomSubject=randomSubject
        self.hasText=hasText
        self.hasHtml=hasHtml
        self.bodyPlainText=bodyPlainText
        self.bodyHtmlText=bodyHtmlText
        self.randomDate=randomDate
        
    def run(self):
        #create message
        m=Mail()
        m.setFrom(self.randomFrom)
        m.addRecipient(self.recipientList)
        m.setSubject(self.randomSubject)
        if self.hasText:
            m.setTextBody(self.bodyPlainText)
        else:
            m.setHtmlBody(self.bodyHtmlText)
        m.setMessageID()
        m.setDate(self.randomDate)
        msg=m.create()
    
        smtpclient=SmtpMailClient(self.hostname, self.port)
        #send message
        for attempt in range(MAXIMUM_NUMBER_OF_ATTEMPTS):
            try:
                smtpclient.send(m.mailfrom, m.to, msg)
            except EnvironmentError as exc:
                if exc.errno == errno.ECONNREFUSED:
                    time.sleep(A_COUPLE_OF_SECONDS)
                else:
                    raise
            else:
                break
        else:
            raise RuntimeError("maximum number of unsuccessful attempts reached")
    
        #smtpMailsink.stop()
