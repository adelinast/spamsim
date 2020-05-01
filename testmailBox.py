#!/usr/bin/python
import mailbox
import logging
import sys

import parse_mail
from filter_manager import FilterManager

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class MyMailBox():
    
    def __init__(self, filename, data):
        self.filename=filename
        if filename is not None:
            self.mbox=mailbox.UnixMailbox(file(filename,"r"))
        else:
            logz.error("filename of the out.mbox is empty")
            self.mbox=None
        self.data=data
        
    def testMessages(self):
        if self.mbox is None:
            logz.error("no mailbox")
            return
        #test if self.mbox has messages
        for message in self.mbox:
            msg=parse_mail.ParsedMessage(message)
            
            filter_manager=FilterManager(msg, self.data)
            filter_manager.run()
