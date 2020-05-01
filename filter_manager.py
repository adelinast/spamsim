import sys
import logging

from spam_filter import FilterMessage
import utils

logz=logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

class FilterManager():
    
    def __init__(self, msg, data):
        self.msg=msg
        self.data=data
        self.score=0.0
        self.str_scan=""
        self.passed_tests=""
        
    def run(self):
        score=0
        filter=FilterMessage(self.msg, self.data)

        ret=self.msg.hasSubject()
        if ret==True:
            self.passed_tests=self.passed_tests+"Subject exists"+"\n"
        else:
            score=utils.getScore("SUBJECT_MISSING", self.data)
            self.str_scan=self.str_scan+"\tSUBJECT_MISSING"+"\trule score:"+str(score)+"\n"
            self.score=self.score+score

        ret=self.msg.hasFrom()
        if ret==True:
            self.passed_tests=self.passed_tests+"Subject exists"+"\n"
        else:
            score=utils.getScore("FROM_MISSING", self.data)
            self.str_scan=self.str_scan+"\tFROM_MISSING"+"\trule score:"+str(score)+"\n"
            self.score=self.score+score
        
        ret=filter.check_header('Message-Id')
        if ret==0:
            self.passed_tests=self.passed_tests+"Header Message-Id is valid"+"\n"
        else:
            score=utils.getScore("MESSAGEID_INVALID", self.data)
            self.str_scan=self.str_scan+"\tMESSAGEID_INVALID"+"\trule score:"+str(score)+"\n"
            self.score=self.score+score
            
        ret=filter.check_header('Date')
        if ret==0:
            self.passed_tests=self.passed_tests+"Header Date is valid"+"\n"
        else:
            score=utils.getScore("DATE_INVALID", self.data)
            self.str_scan=self.str_scan+"\tDATE_INVALID"+"\trule score:"+str(score)+"\n"
            if score is not None:
                self.score=self.score+float(score)
        
        ret=filter.check_header('From')
        if ret==0:
            self.passed_tests=self.passed_tests+"Header From is valid"+"\n"
        else:
            score=utils.getScore("FROM_INVALID", self.data)
            self.str_scan=self.str_scan+"\tFROM_INVALID"+"\trule score:"+str(score)+"\n"
            self.score=self.score+score
        
        ret=filter.check_forged_received_ip()
        if ret==0:
            self.passed_tests=self.passed_tests+"Not forged header"+"\n"
        else:
            score=utils.getScore("RECEIVED_FORGED", self.data)
            self.str_scan=self.str_scan+"\tRECEIVED_FORGED"+"\trule score:"+str(score)+"\n"
            self.score=self.score+score
        
        ret=filter.filter_source_ip()
        if ret is None:
            self.passed_tests=self.passed_tests+"Source IP is not Spam"+"\n"
        else:
            score=utils.getScore("DNSBL_ANSWER", self.data)
            self.str_scan=self.str_scan+"\tDNSBL_ANSWER"+"\trule score:"+str(score)+"\n"
            self.score=self.score+score
        
        self.printResult()
        ret=self.msg.mark_subject(self.getLevelSpam())
        if ret!=0:
            logz.info("Couldn't mark subject")
        
    def getLevelSpam(self):
        if self.score<5.0:
            level="No Spam"
        elif self.score>=5.0 and self.score<10.0:
            level="Spam:Low"
        elif self.score>=10.0 and self.score<15.0:
            level="Spam:Medium"
        elif self.score>=15.0 and self.score<20.0:
            level="Spam:High"
        elif self.score>=20.0:
            level="Spam:Very High"
        else:
            pass
        return level
    
    def printResult(self):
        print "----------------------------------------------------------"
        print "Failed Tests:"
        print self.str_scan
        print "Final Score:[%2.2f]" %self.score
        print "Result:%s" %self.getLevelSpam()
