#!/usr/bin/python

import sys
import threading
import asyncore
import socket
import mailbox
import logging
import StringIO

from smtpserver import SmtpMailServer

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class SmtpMailsink(threading.Thread):
    TIME_TO_WAIT_BETWEEN_CHECKS_TO_STOP_SERVING = 0.001

    def __init__(self, host='localhost', port=1025, mailboxFile=None, threadName=None):   
        self.throwExceptionIfAddressIsInUse(host, port)
        self.initializeThread(threadName)
        self.initializeSmtpMailServer(host, port, mailboxFile)

    def throwExceptionIfAddressIsInUse(self, host, port):
        testSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        testSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                               testSocket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
        testSocket.bind((host, port))
        testSocket.close()

    def initializeThread(self, threadName):
        self._stopevent = threading.Event()
        self.threadName = threadName
        if self.threadName is None:
            self.threadName = SmtpMailsink.__class__
        threading.Thread.__init__(self, name = self.threadName )
        
    def initializeSmtpMailServer(self, host, port, mailboxFile):
        self.smtpMailServer = SmtpMailServer((host, port), None)
        self.resetMailbox(mailboxFile)
                
    def resetMailbox(self, mailboxFile=None):
        self.mailboxFile = mailboxFile
        if self.mailboxFile is None:
            self.mailboxFile = StringIO.StringIO()
        self.smtpMailServer.setMailboxFile(self.mailboxFile)

    def getMailboxContents(self):
        return self.mailboxFile.getvalue()
    
    def getMailboxFile(self):
        return self.mailboxFile
    
    def run(self):
        while not self._stopevent.isSet():
            asyncore.loop(timeout = SmtpMailsink.TIME_TO_WAIT_BETWEEN_CHECKS_TO_STOP_SERVING, count=1)

    def stop(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        self.smtpMailServer.close()

def usage():
    print "Usage: python %s ---mbox=out.mbox --port=port" %sys.argv[0]
    sys.exit(1)

if __name__ == "__main__":
    
    if len(sys.argv)<2 or len(sys.argv)>3:
        usage()
    
    mbox=None
    if len(sys.argv)>=2:
        mboxFilename=sys.argv[1][(len("--mbox")+1):]
        if mboxFilename!='':
            mboxFile = open(mboxFilename, "w+")
            mbox = mailbox.mbox(mboxFilename)
    
    port=1025
    if len(sys.argv)==3:
        port=int(sys.argv[2][(len("--port")+1):])

    ip="0.0.0.0"
    (hostname, aliaslist, ipaddrlist)=socket.gethostbyaddr(ip)
    logz.info("hostname %s", hostname)
    logz.info("aliaslist %s", aliaslist)
    
    smtpMailsink=SmtpMailsink(host=hostname, port=port, mailboxFile=mbox)
    smtpMailsink.start()

    #smtpMailsink.stop(10)
    mboxFile.close()
    