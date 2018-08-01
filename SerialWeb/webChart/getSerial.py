import serial
import time
import serial.tools.list_ports
import threading
import datetime
import os

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
        while self.alive:
            time.sleep(0.1)
            n = self.port.inWaiting()
            data = ''
            if n:
                tmp = self.port.read(n)
                data += "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]" + tmp.decode('utf-8')
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

    def create(self, port, buand=9600):
        port = serial.Serial(port, buand)
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
                    portObj = serial.Serial(name, 9600)
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
