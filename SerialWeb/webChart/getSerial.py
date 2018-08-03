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
        beginTime = 0
        currentChannel = 0
        phase = PHASE_BEFORE_SEND
        while self.alive:
            currentChannel = currentChannel%len(const.PORT_CHANEL_LIST)
            time.sleep(0.1)
            if phase == PHASE_BEFORE_SEND:
                self.port.write((const.PORT_CHANEL_LIST[currentChannel] + const.END_MARK).encode('utf-8'))
                beginTime = datetime.datetime.now()
                phase = PHASE_AFTER_SEND
                continue
            n = self.port.inWaiting()
            data = ''
            if n:
                tmp = self.port.read(n)
                if tmp[const.BEGIN_0] == const.PORT_CHANEL_LIST_X[currentChannel][0] \
                    and tmp[const.BEGIN_1] == const.PORT_CHANEL_LIST_X[currentChannel][1] \
                    and tmp[const.END_0] == const.END_MARK_X[0] and tmp[const.END_1] == const.END_MARK_X[1]:
                    data1 = (tmp[const.DATA_1_1] << 24) + (tmp[const.DATA_1_2] << 16) + (tmp[const.DATA_1_3] << 8) + tmp[const.DATA_1_4]
                    data1 = data1 << 32
                    data1 = const.hex2Double(data1)
                    data2 = (tmp[const.DATA_2_1] << 56) + (tmp[const.DATA_2_2] << 48) + (tmp[const.DATA_2_3] << 40) + (tmp[const.DATA_2_4] << 32) \
                            + (tmp[const.DATA_2_5] << 24) + (tmp[const.DATA_2_6] << 16) + (tmp[const.DATA_2_7] << 8) + tmp[const.DATA_2_8]
                    data2 = const.hex2Double(data2)
                    data3 = (tmp[const.DATA_3_1] << 56) + (tmp[const.DATA_3_2] << 48) + (tmp[const.DATA_3_3] << 40) + (tmp[const.DATA_3_4] << 32) \
                            + (tmp[const.DATA_3_5] << 24) + (tmp[const.DATA_3_6] << 16) + (tmp[const.DATA_3_7] << 8) + tmp[const.DATA_3_8]
                    data3 = const.hex2Double(data3)
                    data += const.CHANNEL_STRING[currentChannel] + "   " + str(data1) + ',' + str(data2) + ',' + str(data3) + "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
                    # data += tmp.decode('utf-8') + "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
                    self.port.flushInput()
            received = False
            if len(data) > 0:
                received = True
                self.data.append(data)
                self.file.write(data + "\r\n")
                phase = PHASE_BEFORE_SEND
                currentChannel += 1
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
        self.portOpened.append(portObj);

    def isOpen(self, name):
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
            if not self.isOpen(port[0]):
                found = False
                for item in self.portOpened:
                    if item.getName() == port[0]:
                        result['open'].append(item.getName())
                        found = True
                        break
                if not found:
                    result['occupy'].append(port[0])
        return result
                    
    
    def openByOther(self, name):
        for port in self.portOpened:
            if port.getName() == name:
                return False
        return True

    def port_close(self, name):
        for item in self.portOpened:
            if name == item.getName():
                item.stop()
                item.port.close()
                self.portOpened.remove(item)
                return

    def read_data(self, name):
        for port in self.portOpened:
            if port.getName() == name:
                if len(port.data) == 0:
                    continue
                message = ''
                for line in port.data:
                    message += line + "\r\n"
                port.data = [];
                return message
        return ''

    def getPortList(self):
	    self.port_list = list(serial.tools.list_ports.comports())
	    return self.port_list;
