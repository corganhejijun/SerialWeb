import serial
import time
import serial.tools.list_ports
import threading
import datetime
import os
from . import serialConstant as const

WAIT_FOR_RECEIVE = 1  #seconds
PHASE_BEFORE_SEND = 0
PHASE_AFTER_SEND = 1
PHASE_RECEIVED = 2
BAUD_RATE = 256000
#ROOT_PATH = '/home/admin1/SerialWeb'
ROOT_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')

class Port:
    def __init__(self, port):
        self.alive = False
        self.waitEnd = None
        self.port = port
        self.data = []
        self.thread = None
        self.file = None
    
    def start(self):
        self.alive = True
        self.waitEnd = threading.Event()
        self.thread = None
        self.thread = threading.Thread(target=self.Reader)
        self.thread.setDaemon(1)
        self.thread.start()
        path = os.path.join(ROOT_PATH, "_" + self.port.name[-4:] + ".txt")
        print('write file to ' + path)
        if (os.path.exists(path)):
            self.file = open(path, "a")
        else:
            self.file = open(path, 'w')

    def Reader(self):
        lasttime = datetime.datetime.now()
        fileData = ''
        oldStr = ''
        count = 0
        while self.alive:
            n = self.port.inWaiting()
            data = ''
            if n:
                tmp = self.port.read(n)
                try:
                    tmp = tmp.decode('utf-8')
                except:
                    continue
                if len(tmp) == 0:
                    continue
                oldStr = oldStr + tmp
                count += 1
                self.port.flushInput()
            if not n or count > 20:
                count = 0
                strList = oldStr.split('\r\n')
                if len(strList) == 0:
                    continue
                oldStr = strList.pop()
                for item in strList:
                    if (len(item) == 0):
                        continue
                    data1_T1, data7_V1, data8_V2 = const.readData(item)
                    if not data7_V1:
                        data += const.CHANNEL_STRING[0] + "   "
                        data += str(data1_T1)
                    else:
                        data += const.CHANNEL_STRING[0] + "   " 
                        data += str(data1_T1) + ',' + str(data7_V1) + ',' + str(data8_V2) 
                    data += "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + "]"
                    fileData += data + "\r\n"
                if len(data) > 0:
                    self.data.append(data)
                if (datetime.datetime.now() - lasttime).total_seconds() > 1:
                    self.file.write(fileData + "\r\n")
                    lasttime = datetime.datetime.now()
                    fileData = ""

    def stop(self):
        self.alive = False
        self.thread.join()
        self.file.close()

    def getName(self):
        return self.port.name


class SerialPort:
    port_list = None
    portOpened = []

    def __init__(self):
        return

    def create(self, portName, baud=BAUD_RATE):
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
            print(portName + ' is already opened')
        portObj = Port(port)
        portObj.start()
        self.portOpened.append(portObj)

    def ready2Open(self, name):
        try:
            for port in self.port_list:
                if name == port[0]:
                    portObj = serial.Serial(name, BAUD_RATE)
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
        self.port_list = list(serial.tools.list_ports.comports())
        return self.port_list
