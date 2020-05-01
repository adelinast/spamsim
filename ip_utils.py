import re

class IP:
    a=0
    b=0
    c=0
    d=0
    
def parseIP(ip):
    matchObj = re.match(r"""^(\d{,3}) \.(\d{,3})\.(\d{,3})\.(\d{,3})$""", ip, re.VERBOSE)
    if matchObj:
        ip=IP()
        ip.a=int(matchObj.group(1))
        ip.b=int(matchObj.group(2))
        ip.c=int(matchObj.group(3))
        ip.d=int(matchObj.group(4))
        return ip
    return None

def getFirstFromIP(ip):
    ip=parseIP(ip)
    if ip is not None:
        return ip.a
    return None

