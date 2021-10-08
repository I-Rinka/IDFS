from requests.api import get
import client.config as conf

def getip():
    print(conf.my_ip)

conf.my_ip="nimabi"

getip()