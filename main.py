import snap7
from snap7 import util

import S7API


def main():
    ip_list = []  # IP列表

    def display_ip_list():
        if ip_list:
            print("当前可连接的PLC IP列表:")
            for ip in ip_list:
                print(f" - {ip}")
        else:
            print("当前没有可连接的PLC IP")

    while True:
        try:
            # Main menu
            print("\n主菜单:")
            print("1. 选择网卡并连接到PLC")
            print("2. 查询CPU信息")
            print("3. 查询数据库")
            print("4. 清空IP列表")
            print("0. 退出程序")
            display_ip_list()

            choice = input("请选择功能 (输入数字): ")

            if choice == "1":
                # 选择网卡并连接到PLC
                interfaces = S7API.get_network_interfaces()
                for index, (name, ip) in enumerate(interfaces):
                    print(f"{index}: 网卡名称: {name}, 网卡IP地址: {ip}")

                print("请选择SiemensPLC所在网卡/网段")
                choice = int(input("请选择网卡索引: "))
                selected_interface = interfaces[choice][1]

                # 计算子网
                subnet = '.'.join(selected_interface.split('.')[:-1]) + '.0'
                print(f"扫描的子网为: {subnet}.0-255")

                ip_range = S7API.generate_ip_range(subnet)
                rack_input = input("请输入PLC所在机架号（默认值为0）：")
                slot_input = input("请输入CPU插槽号（默认值为1）：")

                rack = int(rack_input) if rack_input.strip() else 0
                slot = int(slot_input) if slot_input.strip() else 1

                result = S7API.scan_network(ip_range, rack, slot)

                print(f"在IP段 {subnet}.0-255 中扫描到的PLC连接结果如下：")
                print(f"\n连接成功: {result['success_count']} 台, 连接失败: {result['failure_count']} 台")

                # 添加成功连接的IP到列表
                for ip in result["successful_ips"]:
                    if ip not in ip_list:
                        ip_list.append(ip)

                if result["unreachable_peers"]:
                    print(f"无法访问的设备: {', '.join(result['unreachable_peers'])}")

                if result["timeout_errors"]:
                    print(f"连接超时的设备: {', '.join(result['timeout_errors'])}")

            elif choice == "2":
                # 查询CPU信息
                if not ip_list:
                    ip_input = input("IP列表为空，请输入PLC的IP地址或IP段 (xxx.xxx.xx.xx 或 xxx.xxx.xx.xx/24): ")

                    # 检测如果用户输入了单个IP或IP范围
                    if '/24' in ip_input:
                        subnet = ip_input.split('/')[0]
                        ip_range = S7API.generate_ip_range(subnet)
                    else:
                        ip_range = [ip_input]  # Treat it as a single IP

                    result = S7API.scan_network(ip_range, 0, 1)
                    for ip in result["successful_ips"]:
                        if ip not in ip_list:
                            ip_list.append(ip)

                for ip in ip_list:
                    model, serial = S7API.get_cpu_info(ip, 0, 1)
                    if model:
                        print(f"连接成功设备IP: {ip}, CPU型号: {model}, 序列号: {serial}")
                    else:
                        print(f"无法获取设备 {ip} 的CPU信息")

            elif choice == "3":
                # 查询数据库
                if not ip_list:
                    ip_input = input("IP列表为空，请输入PLC的IP地址或IP段 (xxx.xxx.xx.xx 或 xxx.xxx.xx.xx/24): ")

                    # 如果用户输入了单个IP或IP范围
                    if '/24' in ip_input:
                        subnet = ip_input.split('/')[0]
                        ip_range = S7API.generate_ip_range(subnet)
                    else:
                        ip_range = [ip_input]  # Treat it as a single IP

                    result = S7API.scan_network(ip_range, 0, 1)
                    for ip in result["successful_ips"]:
                        if ip not in ip_list:
                            ip_list.append(ip)

                for ip in ip_list:
                    print("\n请输入以下信息以读取PLC的数据块：")
                    area_input = input("请输入区域 (DB=数据块, PE=输入, PA=输出, MK=标志, TM=计时器, CT=计数器): ")
                    db_number = int(input("请输入数据块号 (如果不是DB区域可填0): "))
                    start = int(input("请输入起始字节位置: "))
                    size = int(input("请输入读取的字节数: "))

                    area_map = {
                        "DB": snap7.client.Area.DB,
                        "PE": snap7.client.Area.PE,
                        "PA": snap7.client.Area.PA,
                        "MK": snap7.client.Area.MK,
                        "TM": snap7.client.Area.TM,
                        "CT": snap7.client.Area.CT,
                    }
                    area = area_map.get(area_input.upper())
                    if area is None:
                        print("无效的区域名称，请重试。")
                        continue

                    # 读取Data Block信息
                    area_info = S7API.read_area_info(ip, 0, 1, area, db_number, start, size)
                    if area_info:
                        print(f"从 {ip} 读取的数据块信息: {area_info}")

                        # 读取数据块中的数据
                        data_type = input("请选择要读取的数据类型 (bool/int): ").strip().lower()
                        byte_offset = int(input("请输入字节偏移量: "))

                        if data_type == "bool":
                            bit_offset = int(input("请输入位偏移量 (0-7): "))
                            bool_value = util.get_bool(area_info, byte_offset, bit_offset)
                            print(f"读取到的布尔值: {bool_value}")
                        elif data_type == "int":
                            # 只读取一个整数值
                            int_value = util.get_int(area_info, byte_offset)
                            print(f"读取到的整数值: {int_value}")
                        else:
                            print("无效的数据类型，请选择 'bool' 或 'int'。")

            elif choice == "4":
                # 清空IP列表
                ip_list.clear()
                print("IP列表已清空。")

            elif choice == "0":
                print("程序退出。")
                break

            else:
                print("无效的选项，请重试。")

        except KeyboardInterrupt:
            print("\n程序被用户终止，正常结束。")
            break
        except Exception as e:
            print(f"发生错误: {e}")


if __name__ == "__main__":
    main()
