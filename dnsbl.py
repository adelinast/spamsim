#!/usr/bin/python
import sys
import logging
import dns.resolver
import time

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class Dnsbl():
    def __init__(self):
        self._dnsTimeoutBlacklist = None
        
    def dnsTimeoutBlacklistHas(self, key):
        if self._dnsTimeoutBlacklist.has_key(key):
            expire = self._dnsTimeoutBlacklist[key]
            if time.time() < expire:
                return True
            return False
        
    def resolve_query(self, ip, dnsbl):
        ips_dnsbl = []
        #to do check ip v4
        iprev = ip.split('.')
        iprev.reverse()
        iprev = '.'.join(iprev)
        check_name = "%s.%s" % (iprev, dnsbl)
        print check_name
        resolver=dns.resolver.Resolver()
        resolver.lifetime = 3
        resolver.timeout = 2
        
        try:
            answers = resolver.query(check_name, 'A')
            for rdata in answers:
                logz.debug("dnsbl: %s ip: %s", dnsbl, rdata.address)
                ips_dnsbl.append(rdata.address)
        except dns.exception.Timeout:
            logz.error("dns exception: No answers could be found in the specified lifetime. %s", dnsbl)
            pass
        except dns.exception.DNSException:
            logz.error("dns exception:  %s", dnsbl)
            pass
        
        if len(ips_dnsbl)>0:
            return ips_dnsbl

    def process_answer(self, ip_current, dnsbl, ip_list, dnsbl_answers):
        if ip_list is None:
            return "NXDOMAIN"
        if len(dnsbl_answers)==0:
            logz.error("dnsbl empty")
            return "dnsbl empty"
        for answer in dnsbl_answers:
            for ip in ip_list:
                if dnsbl==answer.dnsbl and ip==answer.answer:
                    logz.debug("answer description %s", i.description)
                    return answer.description
