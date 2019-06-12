# -*- coding: UTF-8 -*-
import threading
from . import serialConstant as const
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
        path = os.path.join(const.ROOT_PATH, "_" + self.port.name[-4:] + ".txt")
        print('write file to ' + path)
        if (os.path.exists(path)):
            self.file = open(path, "a")
        else:
            self.file = open(path, 'w')

        self.alive = True
        self.thread = None
        self.thread = threading.Thread(target=self.Reader)
        self.thread.setDaemon(1)
        self.thread.start()

    def Reader(self):
        lasttime = datetime.datetime.now()
        fileData = ''
        oldStr = ''
        currentChannel = 0
        sendTime = None
        while self.alive:
            if sendTime is None:
                sendTime = datetime.datetime.now()
                self.port.write(const.SEND_LIST[currentChannel] + const.SEND_END)
            else:
                if (datetime.datetime.now() - sendTime).total_seconds() > const.SEND_INTERVAL:
                    sendTime = None
                    currentChannel = (currentChannel + 1) % len(const.SEND_LIST)
            n = self.port.inWaiting()
            if n:
                try:
                    tmp = self.port.read(n)
                    tmp = tmp.decode('utf-8')
                except:
                    continue
                if len(tmp) == 0:
                    continue
                oldStr = oldStr + tmp
                strList = oldStr.split('\r\n')
                if len(strList) == 0:
                    continue
                oldStr = strList.pop()
                for item in strList:
                    if (len(item) == 0):
                        continue
                    data, channelName = const.processLine(item)
                    if channelName == const.CHANNEL_NAME[currentChannel]:
                        sendTime = None
                        currentChannel = (currentChannel + 1) % len(const.SEND_LIST)
                    fileData += data + "\r\n"
                    if len(data) > 0:
                        self.data.append(data)
                self.port.flushInput()
            if not n and (datetime.datetime.now() - lasttime).total_seconds() > 1:
                if len(fileData) > 0:
                    try:
                        self.file.write(fileData + "\r\n")
                    except:
                        continue
                    fileData = ""
                lasttime = datetime.datetime.now()

    def stop(self):
        self.alive = False
        self.thread.join()
        self.file.close()

    def getName(self):
        return self.port.name