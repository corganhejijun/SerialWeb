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
        path = os.path.join(os.getcwd(), "_" + self.port.name[-4:] + ".txt")
        print('write file to ' + path)
        if (os.path.exists(path)):
            self.file = open(path, "a")
        else:
            self.file = open(path, 'w')

    def Reader(self):
        while self.alive:
            time.sleep(0.1)
            n = self.port.inWaiting()
            data = ''
            if n:
                tmp = self.port.read(n)
                tmp = tmp.decode('utf-8')
                data1_T1, data7_V1, data8_V2 = const.readData(tmp)
                if not data1_T1:
                    continue
                data += const.CHANNEL_STRING[0] + "   " 
                data += str(data1_T1) + ',' + str(data7_V1) + ',' + str(data8_V2) 
                data += "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
                self.port.flushInput()
            if len(data) > 0:
                self.data.append(data)
                self.file.write(data + "\r\n")

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
