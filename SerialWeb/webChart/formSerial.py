# -*- coding: UTF-8 -*-
import requests
import json
from . import serialConstant as const

class SerialPort:
    def __init__(self):
        return

    def sendPost(self, data):
        url = "http://127.0.0.1:8880/"
        r = requests.post(url, data=data)
        print("requests return " + str(r.status_code) + " for " + r.reason)
        data = json.loads(r.text)
        return data

    def getOpenStatus(self, name):
        data = "get:port:" + name
        recv = self.sendPost(data)
        result = recv['data']
        return result

    def getPortList(self):
        data = "get:list"
        recv = self.sendPost(data)
        return recv['data']['port']
        
    def ready2Open(self, name):
        status = self.getOpenStatus(name)
        if len(status) == 0:
            return False
        return not status['opened'] and not status['occupy']

    def openByMe(self, name):
        status = self.getOpenStatus(name)
        if len(status) == 0:
            return False
        return status['opened']

    def create(self, portName, baud=const.BAUD_RATE):
        data = "get:open:" + portName + ":" + str(baud)
        recv = self.sendPost(data)
        print("open port " + portName + " result " + recv['data']['data'])
        
    def port_close(self, name):
        data = "get:close:" + name
        recv = self.sendPost(data)
        print("close port " + name + " result " + recv['data']['data'])

    def read_data(self, nameList):
        pass

    def getOpenList(self):
        data = "get:openList"
        recv = self.sendPost(data)
        return recv['data']

    def dataDown(self, time, count):
        pass