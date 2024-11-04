import psutil
import socket


def get_network_interfaces():
    """获取所有网卡接口及其IP地址"""
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # 使用socket.AF_INET来获取IPv4地址（限制为IPV4）
                interfaces.append((interface, addr.address))
    return interfaces

print(get_network_interfaces())