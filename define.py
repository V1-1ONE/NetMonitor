from ping3 import ping, verbose_ping
from subprocess import Popen, PIPE, STDOUT
import re

def testPrint():
    print("~~~~~~~~~~~~всё заработало поздравляю~~~~~~~~~~~~")

def PingReq(INT):
    ip = INT
    response_time = ping(ip)

    if response_time is not None:
        print(f"Время отклика: {response_time * 1000:.2f} мс")
        return response_time * 1000
    else:
        print("Превышено время ожидания, устройство не доступно.")
        return 0

