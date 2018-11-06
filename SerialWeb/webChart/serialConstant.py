import ctypes
import re

PORT_CHANEL_LIST = ['\x02\x23', '\x02\x23', '\x02\x23', \
                    '\x02\x23', '\x02\x23', '\x02\x23']
#PORT_CHANEL_LIST_X = [[0x01, 0x11], [0x01, 0x12], [0x01, 0x13], \
#                      [0x02, 0x21], [0x02, 0x22], [0x02, 0x03]]
CHANNEL_STRING = ['2_3', '2_3', '2_3', \
                  '2_3', '2_3', '2_3']
PORT_CHANNEL_STRING = ['2_3', '2_3', '2_3', \
                  '2_3', '2_3', '2_3']
END_MARK = '\x0D\x0A'
# END_MARK_X = [0x0D, 0x0A]

#BEGIN_0 = 0
#BEGIN_1 = 1
#DATA_1_1 = 2
#DATA_1_2 = 3
#DATA_2_1 = 4
#DATA_2_2 = 5
#DATA_2_3 = 6
#DATA_2_4 = 7
#DATA_3_1 = 8
#DATA_3_2 = 9
#DATA_3_3 = 10
#DATA_3_4 = 11
#END_0 = 12
#END_1 = 13

def readData(tmp):
    # TODO::
    data = re.match(r'^[0-9_]+[\s]+([0-9-.]+)[\s]+([0-9-.]+)[\s]+([0-9-.]+)', tmp)
    if not data:
        print("get error msg %s" % tmp)
        return None, None, None, None
    data1 = float(data.group(1))
    data2 = float(data.group(2))
    data3 = float(data.group(3))
    data4 = 3 * (int(tmp[0]) - 1) + int(tmp[2]) - 1
    return data1, data2, data3, data4


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