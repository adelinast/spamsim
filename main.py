#!/usr/bin/python
import os
import sys
import logging

from testmailBox import MyMailBox
import extract_data
from extract_data import Data
import parse_mail
from filter_manager import FilterManager

logz=logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

SRC=""
CONF="conf"
RULES=os.path.join(SRC, CONF, 'rules.conf')
REGEXES=os.path.join(SRC, CONF, 'header_regexes.conf')
DNSBL_LIST=os.path.join(SRC, CONF, 'dnsbl_list.conf')
DNSBL_ANSWERS=os.path.join(SRC, CONF, 'dnsbl_answers.conf')

LEVEL_LIST = {'Very High': ['20', 'INF'],
            'High': ['15', '20'],
            'Medium': ['10', '15'],
            'Low': ['5', '10'],
    }

def usage():
    print "Usage: python %s --mbox=out.mbox |--mail=mail.eml" %sys.argv[0]
    sys.exit(1)
    
if __name__ == "__main__":
    if len(sys.argv)<2 or len(sys.argv)>3:
        usage()
    
    #extract params
    mbox=None
    mboxFilename=None
    if len(sys.argv)>=2:
        mboxFilename=sys.argv[1][(len("--mbox")+1):]
        #logz.debug("mboxFilename %s", mboxFilename)
        
    mailFilename=None
    if len(sys.argv)==3:
        mailFilename=sys.argv[2][(len("--mail")+1):]
        #logz.debug("mail %s", mailFilename)

    #extract data from conf files
    data=Data()
    
    extract_data.loadRulesFile(RULES, data)
    extract_data.loadRegexFile(REGEXES, data)
    extract_data.loadDnsblListFile(DNSBL_LIST, data)
    extract_data.loadDnsblAnswerFile(DNSBL_ANSWERS, data)
        
    #test mail box
    print "\nTesting mailbox %s\n" %mboxFilename
    mailBox=MyMailBox(mboxFilename, data)
    mailBox.testMessages()

    #test a mail
    print "\nTesting mail %s\n" %mailFilename
    parse=parse_mail.ParseMail(mailFilename)
    message=parse.getMessage()
    if message is not None:
        msg=parse_mail.ParsedMessage(message)
    else:
        sys.exit(1)
    
    msg.parseReceivedFrom()
    
    list= msg.getReceivedFrom()
    
    for l in list:
        logz.debug("received by [%s]", l.received_by)
        logz.debug("received from [%s]", l.received_from_ip)
    
    filter_manager=FilterManager(msg, data)
    filter_manager.run()
    """
    dns="dnsbl.sorbs.net"
    #hostname, aliaslist, ipaddrlist = socket.gethostbyname(dns)
    ipaddr=socket.gethostbyname(dns)
    #print ipaddr
    
    #ip="77.238.189.89"
    ip="91.205.40.0"
    """