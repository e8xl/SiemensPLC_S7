import socket
import psutil
from scapy.layers.l2 import ARP, Ether, srp

def get_network_interfaces():
    """获取所有网卡接口及其IP地址"""
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # 只获取IPv4地址
                interfaces.append((interface, addr.address))
    return interfaces

def scan_network(ip_range):
    """扫描指定的IP范围，查找在线设备"""
    print(f"开始扫描 {ip_range} ...")
    arp_request = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")  # 广播地址
    packet = ether / arp_request
    result = srp(packet, timeout=5, verbose=False)[0]

    devices = []
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def display_devices(devices):
    """打印扫描到的设备列表并保存到文件"""
    if not devices:
        print("没有扫描到设备")
        return
    else:
        print("扫描到的设备：")
        with open('ip.txt', 'w') as f:
            for device in devices:
                line = f"IP: {device['ip']}, MAC: {device['mac']}\n"
                print(line.strip())
                f.write(line)

def main():
    # 提供用户界面 选择网卡
    interfaces = get_network_interfaces()
    for index, (name, ip) in enumerate(interfaces):
        print(f"{index}: 网卡名称: {name}, 网卡IP地址: {ip}")

    # 用户选择网卡
    choice = int(input("请选择网卡索引: "))
    selected_interface = interfaces[choice][1]  # 存储用户选择的网卡IP地址

    # 计算用户所选网卡的IP地址子网范围（假设为/24）
    subnet = '.'.join(selected_interface.split('.')[:-1]) + '.0/24'

    # 将处理好的CIDR格式IP地址传递给扫描函数
    devices = scan_network(subnet)

    # 显示扫描结果
    display_devices(devices)

if __name__ == "__main__":
    main()
