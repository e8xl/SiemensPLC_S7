import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

import psutil
import snap7


def get_network_interfaces():
    """获取所有网卡接口及其IP地址"""
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # 只获取IPv4地址
                interfaces.append((interface, addr.address))
    return interfaces


def generate_ip_range(subnet):
    """生成子网IP地址列表"""
    ip_range = []
    base_ip = subnet.rsplit('.', 1)[0]  # 获取子网基地址
    for i in range(256):
        ip_range.append(f"{base_ip}.{i}")
    return ip_range


def connect_plc(ip, rack, slot):
    """连接到指定 IP 的 PLC，返回客户端对象和连接状态"""
    client = snap7.client.Client()
    try:
        client.connect(ip, rack, slot)
        return client, True, None
    except Exception as e:
        return None, False, str(e)


def disconnect_plc(client):
    """断开与 PLC 的连接"""
    if client is not None:
        try:
            client.disconnect()
        except Exception as e:
            print(f"断开连接时发生错误: {e}")


def get_cpu_info(ip, rack, slot):
    """获取指定IP的PLC的CPU信息"""
    client, connected, error_msg = connect_plc(ip, rack, slot)
    if not connected:
        print(f"无法连接到 {ip}: {error_msg}")
        return None, None

    try:
        info = client.get_cpu_info()
        model_name = info.ModuleTypeName.decode('utf-8')
        serial_number = info.SerialNumber.decode('utf-8')
        return model_name, serial_number
    except Exception as e:
        print(f"无法读取 {ip} 的 CPU 型号: {e}")
        return None, None
    finally:
        disconnect_plc(client)


def scan_network(ip_range, rack, slot):
    """使用线程池并发检查网络中的PLC连接状态"""
    success_count = 0
    failure_count = 0
    successful_ips = []
    unreachable_peers = []
    timeout_errors = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_ip = {executor.submit(connect_plc, ip, rack, slot): ip for ip in ip_range}

        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            client, connected, error_msg = future.result()

            if connected:
                successful_ips.append(ip)
                success_count += 1
                disconnect_plc(client)  # 连接成功后断开连接
            else:
                failure_count += 1
                if "Unreachable peer" in error_msg:
                    unreachable_peers.append(ip)
                elif "Connection timed out" in error_msg:
                    timeout_errors.append(ip)

    return {
        "success_count": success_count,
        "failure_count": failure_count,
        "successful_ips": successful_ips,
        "unreachable_peers": unreachable_peers,
        "timeout_errors": timeout_errors,
    }

def read_area_info(ip, rack, slot, area, db_number, start, size):
    """读取PLC的指定数据区域"""
    client, connected, error_msg = connect_plc(ip, rack, slot)
    if not connected:
        print(f"无法连接到 {ip}: {error_msg}")
        return None

    try:
        # 读取区域数据
        area_info = client.read_area(area, db_number, start, size)
        return area_info
    except Exception as e:
        print(f"无法读取 {ip} 设备的数据块信息: {e}")
        return None
    finally:
        disconnect_plc(client)
