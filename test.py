from urllib.request import Request, urlopen
import re


def getIP():
    d = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

ip = getIP()
ip = str(ip)

print(ip)