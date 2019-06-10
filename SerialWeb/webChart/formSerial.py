# -*- coding: UTF-8 -*-
import requests
import json
from . import serialConstant as const
import datetime
from . import models

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

    def process_data(self, recv, namelist):
        lines = recv.split('\r\n')
        portName = ""
        result = []
        for line in lines:
            if len(line) == 0:
                continue
            data = ''
            if ":" in line:
                [portName, data] = line.split(':', 1)
            else:
                data = line
            if len(portName) > 0 and len(data) > 0:
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                if portName in namelist:
                    result.append(portName + ":" + data + '[' + time + ']')
                # portData = models.PortData(name=portName, time=time, strValue=data)
                # portData.save()
                
        return result

    def read_data(self, nameList):
        data = "get:data"
        url = "http://127.0.0.1:8880/"
        r = requests.post(url, data=data)
        recv = r.text[len('{"result":true, "data":{"data": "'):-len('"}}')]
        print("receive data: " + recv)
        return self.process_data(recv, nameList)

    def getOpenList(self):
        data = "get:openList"
        recv = self.sendPost(data)
        return recv['data']

    def dataDown(self, time, count):
        pass