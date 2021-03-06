# -*- coding: UTF-8 -*-
import os
import datetime
from . import models

BAUD_RATE = 9600
ROOT_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..')
SEND_INTERVAL = 2 # second

SEND_LIST = [b'\x01\x11', b'\x01\x12', b'\x02\x11', b'\x02\x12']
SEND_END = b'\x0D\x0A'
CHANNEL_NAME = ['1_1', '2_1', '1_2', '2_2']

def readData(tmp):
    # TODO::数据格式：1_1 T1 V1 V2 ...
    strList = tmp.split(' ')
    dataList = []
    for i, _ in enumerate(strList):
        if i == 0:
            channelName = strList[i]
        else:
            d = None
            try:
                d = float(strList[i])
            except:
                d = None
            dataList.append(d)
    return channelName, dataList

def processLine(line):
    channelName, dataList = readData(line)
    data = channelName + ' '
    dataStr = ''
    if len(dataList) == 0:
        # 单通道的情况
        data = channelName
        channelName = ''
    for i, item in enumerate(dataList):
        dataStr += str(item)
        if i < len(dataList) - 1:
            dataStr += ','
    data += dataStr
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data += "[" + time + "]"
    portData = models.PortData(name=channelName, time=time, strValue=dataStr)
    portData.save()
    return data, channelName
    

def dataDown(time, count):
    portData = models.PortData.objects.all().order_by('-id')[:count]
    result = []
    for data in portData:
        result.append({'name': data.name, 'value': data.strValue, 'time': data.time})
    fileName = "dataResult.csv"
    filePathOld = os.path.join(ROOT_PATH, "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv")
    filePath = os.path.join(ROOT_PATH, fileName)
    if os.path.exists(filePath):
        os.rename(filePath, filePathOld)
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


## deprecated
#def hex2Double(s):
#    cp = ctypes.pointer(ctypes.c_longlong(s))
#    fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_double))
#    return fp.contents.value
#
#def double2hex(s):
#    fp = ctypes.pointer(ctypes.c_double(s))
#    cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_longlong))
#    return hex(cp.contents.value)
#
#def readData1(data):
#    data1 = (data[DATA_1_1] << 8) + data[DATA_1_2]
#    data1 = data1 << (32 + 16)
#    return data1
#
#def readData2(data):
#    data2 = (data[DATA_2_1] << 24) + (data[DATA_2_2] << 16) + (data[DATA_2_3] << 8) + data[DATA_2_4]
#    data2 = data2 << 32
#    return data2
#
#def readData3(data):
#    data3 = (data[DATA_3_1] << 24) + (data[DATA_3_2] << 16) + (data[DATA_3_3] << 8) + data[DATA_3_4]
#    data3 = data3 << 32
#    return data3