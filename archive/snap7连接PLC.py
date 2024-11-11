import snap7

def check_plc(ip):
    """尝试连接到指定 IP 的 PLC，并返回连接状态"""
    client = snap7.client.Client()
    try:
        client.connect(ip, 0, 1)  # 通常为 PLC 的机架和插槽
        print(f"成功连接到 PLC: {ip}")
        return True
    except Exception as e:
        print(f"{ip} 连接失败: {e}")
        return False
    finally:
        client.disconnect()

def read_ip_list(file_path):
    """从文件中读取 IP 地址并返回列表"""
    ip_list = []
    with open(file_path, 'r') as file:
        for line in file:
            # 去除空行和换行符
            line = line.strip()
            if line and line.startswith("IP:"):
                ip = line.split(",")[0].split(":")[1].strip()
                ip_list.append(ip)
    return ip_list

def main():
    ip_file_path = 'ip.txt'  # 文件路径
    ip_list = read_ip_list(ip_file_path)  # 从文件读取 IP 地址

    for ip in ip_list:
        check_plc(ip)

if __name__ == "__main__":
    main()
