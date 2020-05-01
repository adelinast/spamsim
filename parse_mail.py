#!/usr/bin/python

import sys
import logging
import email.Parser
import email.Message
import re

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class ParseMail():
    
    def __init__(self, mailFileName):
        self.mailFileName=mailFileName
    
    def getMessage(self):
        if self.mailFileName is None:
            logz.info("mail filename is empty")
            return
        #open the mail
        try:
            mailFile = open(self.mailFileName)
        except IOError:
            logz.info("file %s cannot be opened", self.mailFileName)
            return
        
        parser=email.Parser.Parser()
        try:
            msg=parser.parse(mailFile)
            mailFile.close()
        except email.Errors.HeaderParseError:
            logz.info("Corrupt message!")
            sys.exit(1)
        return  msg

class ReceivedFrom:
    received_from_ip=None
    received_by=None
    
class ParsedMessage():
    
    received_from=None
    
    def __init__(self, msg):
        self.msg=msg
        self.received_from=[]
    
    def getHeaders(self):
        logz.debug("all headers %s", self.msg.items())
        #get headers
        return self.msg.items()
    
    def getHeader(self, headerName):
        if self.msg.has_key(headerName):
            header = self.msg.get(headerName,'')
            #logz.debug("header content %s", header)
            return header
        else:
            return None
        
    def getParts(self):
        #separate parts
        partCounter=1
        for part in self.msg.walk():
            if part.get_content_maintype()=="multipart":
                continue
            name=part.get_param("name")
            if name==None:
                name="part-%i" % partCounter
            partCounter+=1
            f=open(name,"wb")
            f.write(part.get_payload(decode=1))
            f.close()
    
    def getMessageID(self):
        msgId=self.getHeader('Message-ID')
        return msgId

    def getFrom(self):
        return self.getHeader('From')
    
    def getHeaderNames(self):
        fields=self.msg.keys()
        #for field in fields:
            #logz.debug("Field %s exist", field)
        return fields
    
    def getReceivedFrom(self):
        #get received from list
        if self.received_from is not None:
            return self.received_from
        else:
            return None
    
    def parseReceivedFrom(self):
        #makes a list with received from ip and received and store in self.received_from
        received_list=self.msg.get_all('received')
        if received_list is None:
            return
        for received in received_list:
            matchObj = re.match(r"""^from \s* \[ (\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}) \] (?:.*?) by (.*?\..*?) with|via (?:.*?) $""", received, re.VERBOSE)
            if matchObj:
                #logz.debug("matchObj.group() : %s" % matchObj.group())
                #logz.debug("matchObj.group(1) : %s" % matchObj.group(1))
                #logz.debug("matchObj.group(2) : %s" % matchObj.group(2))
                received_from=ReceivedFrom()
                received_from.received_from_ip=matchObj.group(1).strip()
                received_from.received_by=matchObj.group(2).strip()
                self.received_from.append(received_from)
    
    def getSourceIpAddress(self):
        if self.received_from is not None:
            received = self.received_from
            return received[0].received_from_ip if received else None
    
    def getLastIpAddress(self):
        if self.received_from is not None and len(self.received_from)>=1:
            return self.received_from[len(self.received_from)-1].received_from_ip
    
    def getPreviousLastIpAddress(self):
        if self.received_from is not None and len(self.received_from)>=2:
            return self.received_from[len(self.received_from)-2].received_from_ip
    
    def getLastReceivedBy(self):
        if self.received_from is not None and len(self.received_from)>=1:
            return self.received_from[len(self.received_from)-1].received_by
    
    def getPreviousLastReceivedBy(self):
        if self.received_from is not None and len(self.received_from)>=2:
            return self.received_from[len(self.received_from)-2].received_by
    
    def mark_subject(self, level):
        subject=self.getHeader('Subject')
        if subject is None:
            return
        if level is not None:
            subject="[Spam"+":"+level+"] "+subject[0:]
        else:
            #subject="[Spam"+"] "+subject[0:]
            return 1
        return 0
    
    def hasSubject(self):
        if self.getHeader('Subject') is None:
            return False
        return True
    
    def hasFrom(self):
        if self.getHeader('From') is None:
            return False
        return True
    