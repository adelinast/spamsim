#!/usr/bin/python
import sys
import logging
import re

from dnsbl import Dnsbl
import ip_utils

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class FilterMessage():

    def __init__(self, message, data):
        self.messsage=message
        self.data=data
    
    def check_header(self, header_name):
        header_content=self.messsage.getHeader(header_name)
        if header_content is None:
            return
        logz.info("Check %s %s", header_name, header_content)
        #loop through regex list to check if the header has the correct form    
        for header_regex in self.data.header_regex:
            logz.debug("header %s regex %s", header_regex.header, header_regex.regex)
            if header_regex.header==header_name:
                logz.debug("Found regex for %s", header_name)
                matchObj = re.match(header_regex.regex, header_content, re.VERBOSE)
                if matchObj:
                    logz.debug("Header %s is valid", header_name)
                    return 0
                else:
                    logz.debug("Header %s NOT valid", header_name)
                    return 1
        logz.debug("Header %s not found in regex", header_name)
        return -1

    def check_existent_headers(self):
        headers_list=self.messsage.getHeaderNames()
        for header_name in headers_list:
            ret=self.verify_header(header_name)
            if ret==0:
                logz.info("Header [%s] is valid", header_name)
            elif ret==-1:
                logz.info("Header [%s] not found in regex", header_name)
            else:
                logz.info("Header [%s] NOT valid", header_name)
        return ret
    
        
    def check_forged_received_ip(self):
        ip_utils.getFirstFromIP(str(self.messsage.getLastIpAddress()))
        return 0
        
    def filter_source_ip(self):
        #check source ip with dnsbl
        result=""
        ip_address=self.messsage.getSourceIpAddress()
        if ip_address is None:
            return
        print ip_address
        ips=[]
        if self.data.dnsbl is None:
            return
        for host in self.data.dnsbl:
            dnsbl=Dnsbl()
            ips=dnsbl.resolve_query(ip_address, host)
            description=dnsbl.process_answer(ip_address, host, ips, self.data.dnsbl_answer)
            logz.info("dnsbl answer %s",description)
            if description!="NXDOMAIN":
                result=result+str(description)
        if result!="":
            return result
        return None
        
    