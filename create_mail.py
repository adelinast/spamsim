#!/usr/bin/python

import os
import re
import sys
import datetime

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils
import mimetypes

import logging
from logging import raiseExceptions

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class Mail():
    def __init__(self):
        self.textBody = None
        self.htmlBody = None
        self.subject = ""
        self.reEmail = re.compile("^([\\w \\._]+\\<[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\>|[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)$")
        self.clearRecipients()
        self.clearAttachments()

    def create(self):
        if self.textBody is None and self.htmlBody is None:
            raiseExceptions("Error - must specify at least one body type")
        if len(self.to)==0:
            raiseExceptions("Error - must specify at least one recipient")
        if self.textBody is not None and self.htmlBody is None:
            msg=MIMEText(self.textBody, "plain")
        elif self.textBody is None and self.htmlBody is not None:
            msg=MIMEText(self.htmlBody, "html")
        else:
            msg=MIMEMultipart("alternative")
            msg.attach(self.textBody, "plain")
            msg.attach(self.htmlBody, "html")
            if len(self.attach) != 0:
                tmpmsg = msg
                msg = MIMEMultipart()
                msg.attach(tmpmsg)
            for fname,attachname in self.attach:
                if not os.path.exists(fname):
                    print "File '%s' does not exist.  Not attaching to email." % fname
                    continue
                if not os.path.isfile(fname):
                    print "Attachment '%s' is not a file.  Not attaching to email." % fname
                    continue
            # Guess at encoding type
            ctype, encoding = mimetypes.guess_type(fname)
            if ctype is None or encoding is not None:
                # No guess could be made so use a binary type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(fname)
                attach = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(fname, 'rb')
                attach = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(fname, 'rb')
                attach = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(fname, 'rb')
                attach = MIMEBase(maintype, subtype)
                attach.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(attach)

            # Set the filename parameter
            if attachname is None:
                filename = os.path.basename(fname)
            else:
                filename = attachname
            
            attach.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attach)
        if self.subject is not None:
            msg['Subject']=self.subject
        if self.mailfrom is not None:
            msg['From']=self.mailfrom
        if self.to is not None:
            msg['To']=", ".join(self.to)
        if self.messageID is not None:
            msg['Message-ID']=self.messageID
        if self.date is not None:
            msg['Date']=self.date
        msg.preamble = "You need a MIME enabled mail reader to see this message"
        return msg
    
    def setMessageID(self):
        self.messageID = email.utils.make_msgid()
    
    def setDate(self, date):
        self.date=datetime.date(date.year, date.month, date.day).strftime( "%d/%m/%Y %H:%M")
    
    def setFrom(self, address):
        """
        Set the email sender.
        """
        if not self.validateEmailAddress(address):
            raise Exception("Invalid email address '%s'" % address)
        self.mailfrom = address
    
    def setSubject(self, subject):
        """
        Set the subject of the email message.
        """
        self.subject = subject

    def setTextBody(self, body):
        """
        Set the plain text body of the email message.
        """
        self.textBody = body

    def clearRecipients(self):
        """
        Remove all currently defined recipients for
        the email message.
        """
        self.to = []
    
    def addRecipient(self, address):
        """
        Add a new recipient to the email message.
        """
        if not self.validateEmailAddress(address):
            raise Exception("Invalid email address '%s'" % address)
        self.to.append(address)

    def clearAttachments(self):
        """
        Remove all file attachments.
        """
        self.attach = []

    def validateEmailAddress(self, address):
        """
        Validate the specified email address.
        
        @return: True if valid, False otherwise
        @rtype: Boolean
        """
        if self.reEmail.search(address) is None:
            return False
        return True
    
    def setHtmlBody(self, body):
        """
        Set the HTML portion of the email message.
        """
        self.htmlBody = body

    def addAttachment(self, fname, attachname=None):
        """
        Add a file attachment to this email message.
        @param fname: The full path and file name of the file
                      to attach.
        @type fname: String
        @param attachname: This will be the name of the file in
                           the email message if set.  If not set
                           then the filename will be taken from
                           the fname parameter above.
        @type attachname: String
        """
        if fname is None:
            return
        self.attach.append( (fname, attachname) )
