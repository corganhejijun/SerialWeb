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
DATA_1_3 = 4
DATA_1_4 = 5
DATA_2_1 = 6
DATA_2_2 = 7
DATA_2_3 = 8
DATA_2_4 = 9
DATA_2_5 = 10
DATA_2_6 = 11
DATA_2_7 = 12
DATA_2_8 = 13
DATA_3_1 = 14
DATA_3_2 = 15
DATA_3_3 = 16
DATA_3_4 = 17
DATA_3_5 = 18
DATA_3_6 = 19
DATA_3_7 = 20
DATA_3_8 = 21
END_0 = 22
END_1 = 23


def hex2Double(s):
    cp = ctypes.pointer(ctypes.c_longlong(s))
    fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_double))
    return fp.contents.value

def double2hx(s):
    fp = ctypes.pointer(ctypes.c_double(s))
    cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_longlong))
    return hex(cp.contents.value)