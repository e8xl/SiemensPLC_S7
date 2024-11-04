import socket
import psutil
import snap7
from concurrent.futures import ThreadPoolExecutor, as_completed


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


def check_plc(ip, rack, slot):
    """尝试连接到指定 IP 的 PLC，并返回连接状态"""
    client = snap7.client.Client()
    # noinspection PyBroadException
    try:
        client.connect(ip, rack, slot)  # 使用用户指定的机架和插槽
        return ip, True
    except Exception:
        return ip, False
    finally:
        client.disconnect()


def main():
    try:
        # 提供用户界面选择网卡
        interfaces = get_network_interfaces()
        for index, (name, ip) in enumerate(interfaces):
            print(f"{index}: 网卡名称: {name}, 网卡IP地址: {ip}")

        # 用户选择网卡
        choice = int(input("请选择网卡索引: "))
        selected_interface = interfaces[choice][1]  # 存储用户选择的网卡IP地址

        # 计算用户所选网卡的IP地址子网范围（假设为/24）
        subnet = '.'.join(selected_interface.split('.')[:-1]) + '.0'
        print(f"扫描的子网为: {subnet}.0-255")

        # 生成子网IP地址列表
        ip_range = generate_ip_range(subnet)

        # 获取机架号和插槽号，允许用户输入
        rack_input = input("请输入机架号（默认值为0）：")
        slot_input = input("请输入插槽号（默认值为1）：")

        # 设置默认值
        rack = int(rack_input) if rack_input.strip() else 0
        slot = int(slot_input) if slot_input.strip() else 1

        # 用于统计连接结果
        success_count = 0
        failure_count = 0
        successful_ips = []

        # 使用线程池并发检查PLC连接
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_ip = {executor.submit(check_plc, ip, rack, slot): ip for ip in ip_range}
            for future in as_completed(future_to_ip):
                ip, success = future.result()
                if success:
                    successful_ips.append(ip)
                    success_count += 1
                else:
                    failure_count += 1

        # 输出连接结果
        print(f"\n连接成功: {success_count} 台, 连接失败: {failure_count} 台")
        for ip in successful_ips:
            print(f"连接成功设备IP: {ip}")

    except KeyboardInterrupt:
        print("\n程序被用户终止，正常结束。")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
