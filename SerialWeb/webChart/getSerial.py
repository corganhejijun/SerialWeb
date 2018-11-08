import serial
import time
import serial.tools.list_ports
import threading
import datetime
import os
from . import serialConstant as const

WAIT_FOR_RECEIVE = 2  #seconds
PHASE_BEFORE_SEND = 0
PHASE_AFTER_SEND = 1
PHASE_RECEIVED = 2
BAUD_RATE = 9600

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
        path = os.path.join(os.getcwd(), "_" + self.port.name + ".txt")
        if (os.path.exists(path)):
            self.file = open(path, "a")
        else:
            self.file = open(path, 'w')

    def Reader(self):
        beginTime = datetime.datetime(1970,1,1)
        currentChannel = 0
        phase = PHASE_BEFORE_SEND
        received = False
        while self.alive:
            currentChannel = currentChannel%len(const.PORT_CHANEL_LIST)
            time.sleep(0.1)
            if phase == PHASE_BEFORE_SEND:
                self.port.write((const.PORT_CHANEL_LIST[currentChannel] + const.END_MARK).encode('utf-8'))
                print("write data to port %s" % const.CHANNEL_STRING[currentChannel])
                if received:
                    beginTime = datetime.datetime.now()
                phase = PHASE_AFTER_SEND
                continue
            n = self.port.inWaiting()
            data = ''
            if n:
                phase = PHASE_BEFORE_SEND
                tmp = self.port.read(n)
                tmp = tmp.decode('utf-8')
                print("get string %s" % tmp)
                if tmp.startswith(const.PORT_CHANNEL_STRING[currentChannel]):
                    # TODO::
                    data1_T1, data2_RH1, data3_T2, data4_RH2, data5_T3, data6_RH3, data7_V1, data8_V2, data9_V3, data10_VR = const.readData(tmp)
                    if not data1_T1:
                        continue
                    # TODO::
                    data += const.CHANNEL_STRING[currentChannel] + "   " + str(data1_T1) + ',' + str(data2_RH1) + ',' + str(data3_T2) + ',' + str(data4_RH2) + ',' + str(data5_T3)+ ',' + str(data6_RH3)+ ',' + str(data7_V1)+ ',' + str(data8_V2)+ ',' + str(data9_V3)+ ',' + str(data10_VR)+ "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
                    # data += tmp.decode('utf-8') + "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
                    self.port.flushInput()
            if len(data) > 0:
                received = True
                self.data.append(data)
                self.file.write(data + "\r\n")
                currentChannel += 1
            else:
                received = False
            if not received:
                if (datetime.datetime.now() - beginTime) > datetime.timedelta(seconds=WAIT_FOR_RECEIVE):
                    phase = PHASE_BEFORE_SEND
                    currentChannel += 1

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

    def create(self, port, baud=BAUD_RATE):
        port = serial.Serial(port, baud, write_timeout=0)
        port.timeout = 2
        if not port.isOpen():
            port.open()
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
