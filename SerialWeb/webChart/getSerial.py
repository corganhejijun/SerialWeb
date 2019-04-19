# -*- coding: UTF-8 -*-
import serial
import time
import serial.tools.list_ports as list_ports
from . import serialConstant as const
from . import Port
from . import models
import datetime
import os

class SerialPort:
    port_list = None
    portOpened = []

    def __init__(self):
        return

    def create(self, portName, baud=const.BAUD_RATE):
        for p in self.portOpened:
            if p.getName() == portName:
                print("already opened")
                return
        port = serial.Serial(portName, baud, write_timeout=0)
        port.timeout = 2
        if not port.isOpen():
            port.open()
            print('open ' + portName + ' success')
        else:
            port.close()
            port.open()
            print(portName + ' is already opened')
        portObj = Port.Port(port)
        portObj.start()
        self.portOpened.append(portObj)

    def ready2Open(self, name):
        try:
            for port in self.port_list:
                if name == port[0]:
                    portObj = serial.Serial(name, const.BAUD_RATE)
                    return portObj.isOpen()
        except:
            pass
        return False
    
    def getOpenList(self):
        result = {'open': [], 'occupy': []}
        for port in self.port_list:
            if not self.ready2Open(port[0]):
                found = False
                for item in self.portOpened:
                    if item.getName() == port[0]:
                        result['open'].append(item.getName())
                        found = True
                        break
                if not found:
                    result['occupy'].append(port[0])
        return result
                    
    
    def openByMe(self, name):
        for port in self.portOpened:
            if port.getName() == name:
                return True 
        return False

    def port_close(self, name):
        for item in self.portOpened:
            if name == item.getName():
                item.stop()
                item.port.close()
                self.portOpened.remove(item)
                print("port " + name + " closed")
                return

    def read_data(self, nameList):
        message = []
        for name in nameList:
            for port in self.portOpened:
                if port.getName() == name:
                    if len(port.data) == 0:
                        continue
                    text = name + ":"
                    for line in port.data:
                        text += line + "\r\n"
                    port.data = []
                    message.append(text)
        return message

    def getPortList(self):
        self.port_list = list(list_ports.comports())
        return self.port_list

    def dataDown(self, time, count):
        portData = models.PortData.objects.all().order_by('-id')[:count]
        result = []
        for data in portData:
            result.append({'name': data.name, 'value': data.strValue, 'time': data.time})
        filePath = os.path.join(const.ROOT_PATH, "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".txt")
        with open(filePath, 'w') as file:
            file.write('T1,T2,T3,T4,T5,T6,RH1,RH2,RH3,RH4,RH5,RH6,V11,V12,V13,V21,V22,V23,V1,V2,V11,V12,date\r\n')
            for item in reversed(result):
                if item['name'] ==  '1_1':
                    try:
                        value = item['value'].split(',')
                        line = ',,,,,,,,,,,,' + value[0] + ',' + value[1] + ',' + value[2] + ',,,,' + value[3] + ',,,,' + item['time']
                        file.write(line + '\r\n')
                    except:
                        pass
                if item['name'] == '2_1':
                    try:
                        value = item['value'].split(',')
                        line = ',,,,,,,,,,,,,,,' + value[0] + ',' + value[1] + ',' + value[2] + ',,' + value[3] + ',,,' + item['time']
                        file.write(line + '\r\n')
                    except:
                        pass
                if item['name'] == '1_2':
                    try:
                        value = item['value'].split(',')
                        line = (value[0] + ',' + value[2] + ',' + value[4] + ',,,,' 
                            + value[1] + ',' + value[3] + ',' + value[5] + ',,,,,,,,,,,,,,' + item['time'])
                        file.write(line + '\r\n')
                    except:
                        pass
                if item['name'] == '2_2':
                    try:
                        value = item['value'].split(',')
                        line = (',,,' + value[0] + ',' + value[2] + ',' + value[4] + ',,,,' 
                            + value[1] + ',' + value[3] + ',' + value[5] + ',,,,,,,,,,,' + item['time'])
                        file.write(line + '\r\n')
                    except:
                        pass
        return filePath
