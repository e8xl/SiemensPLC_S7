import snap7
from S7API import read_area_info
from snap7 import util
plc = snap7.client.Client()
a = read_area_info('192.168.0.1', 0, 1, snap7.client.Area.DB, 1, 0, 4)
print(a)
bool1 = util.get_bool(a, 2, 0)
bool2 = util.get_bool(a, 2, 1)
print(bool1)
print(bool2)
int1 = util.get_int(a, 0)
print(int1)