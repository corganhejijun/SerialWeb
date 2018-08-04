import ctypes

PORT_CHANEL_LIST = ['\x01\x11', '\x01\x12', '\x01\x13', \
                    '\x02\x21', '\x02\x22', '\x02\x23']
PORT_CHANEL_LIST_X = [[0x01, 0x11], [0x01, 0x12], [0x01, 0x13], \
                      [0x02, 0x21], [0x02, 0x22], [0x02, 0x03]]
CHANNEL_STRING = ['1__1', '1__2', '1__3', \
                  '2__1', '2__2', '2__3']
END_MARK = '\x0A\x0D'
END_MARK_X = [0x0A, 0x0D]

BEGIN_0 = 0
BEGIN_1 = 1
DATA_1_1 = 2
DATA_1_2 = 3
DATA_2_1 = 4
DATA_2_2 = 5
DATA_2_3 = 6
DATA_2_4 = 7
DATA_3_1 = 8
DATA_3_2 = 9
DATA_3_3 = 10
DATA_3_4 = 11
END_0 = 12
END_1 = 13


def hex2Double(s):
    cp = ctypes.pointer(ctypes.c_longlong(s))
    fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_double))
    return fp.contents.value

def double2hex(s):
    fp = ctypes.pointer(ctypes.c_double(s))
    cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_longlong))
    return hex(cp.contents.value)

def readData1(data):
    data1 = (data[DATA_1_1] << 8) + data[DATA_1_2]
    data1 = data1 << (32 + 16)
    return data1

def readData2(data):
    data2 = (data[DATA_2_1] << 24) + (data[DATA_2_2] << 16) + (data[DATA_2_3] << 8) + data[DATA_2_4]
    data2 = data2 << 32
    return data2

def readData3(data):
    data3 = (data[DATA_3_1] << 24) + (data[DATA_3_2] << 16) + (data[DATA_3_3] << 8) + data[DATA_3_4]
    data3 = data3 << 32
    return data3