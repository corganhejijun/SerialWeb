import serial
import time
import serial.tools.list_ports
import threading
import datetime

class Port:
    def __init__(self, port):
        self.alive = False
        self.waitEnd = None
        self.port = port
        self.data = []
        self.thread = None
    
    def start(self):
        self.alive = True
        self.waitEnd = threading.Event()
        self.thread = None
        self.thread = threading.Thread(target=self.Reader)
        self.thread.setDaemon(1)
        self.thread.start()

    def Reader(self):
        while self.alive:
            time.sleep(0.1)
            n = self.port.inWaiting()
            data = ''
            if n:
                tmp = self.port.read(n)
                data += "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]" + tmp.decode('utf-8')
            self.data.append(data)
            self.port.flushInput()

    def stop(self):
        self.alive = False
        self.thread.join()

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
                message = ''
                for line in port.data:
                    message += line + "\r\n"
                return message
        return ''

    def getPortList(self):
	    self.port_list = list(serial.tools.list_ports.comports())
	    return self.port_list;
