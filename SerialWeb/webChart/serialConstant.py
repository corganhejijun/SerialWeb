import ctypes
import re

PORT_CHANEL_LIST = ['\x01\x10', '\x02\x20']
#PORT_CHANEL_LIST_X = [[0x01, 0x11], [0x01, 0x12], [0x01, 0x13], \
#                      [0x02, 0x21], [0x02, 0x22], [0x02, 0x03]]
CHANNEL_STRING = ['1_1', '2_1']
PORT_CHANNEL_STRING = ['1_1', '2_1']
END_MARK = '\x0D\x0A'

def readData(tmp):
    # TODO::
    patternStr = r'^[0-9_]+[\s]+'
    patternStr += r'([0-9-.]+)[\s]+([0-9-.]+)[\s]+([0-9-.]+)[\s]+'
    patternStr += r'([0-9-.]+)[\s]+([0-9-.]+)[\s]+([0-9-.]+)[\s]+'
    patternStr += r'([0-9-.]+)[\s]+([0-9-.]+)[\s]+([0-9-.]+)[\s]+([0-9-.]+)'
    pattern = re.compile(patternStr)
    data = pattern.match(tmp)
    if not data:
        print("get error msg %s" % tmp)
        return None, None, None, None, None, None, None, None, None, None
    # T1,RH1,T2,RH2,T2,RH2
    data1_T1 = float(data.group(1))
    data2_RH1 = float(data.group(2))
    data3_T2 = float(data.group(3))
    data4_RH2 = float(data.group(4))
    data5_T3 = float(data.group(5))
    data6_RH3 = float(data.group(6))
	
	# V1,V2,V3
    data7_V1 = float(data.group(7))
    data8_V2 = float(data.group(8))
    data9_V3 = float(data.group(9))
	
	# VR
    data10_VR = float(data.group(10))
	
    #data4 = 3 * (int(tmp[0]) - 1) + int(tmp[2]) - 1
	#data4 = float(data.group(4))
    return data1_T1, data2_RH1, data3_T2, data4_RH2, data5_T3, data6_RH3, data7_V1, data8_V2, data9_V3, data10_VR

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