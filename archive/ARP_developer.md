# SiemensPLC_Project1

### Requirements（需求） 

设计一个程序，能够搜索子网内的西门子PLC设备，并把搜索到的设备在列表中显示出来。

### Analysis（分析）

1. Siemens PLC 子网设备使用TCP/IP方式连接

2. 使用Python模块搜索子网设备

3. 发送ARP广播获取指定网卡设备内的子网设备

4. 分析设备地址（未确定是否合理）

5. 根据SiemensPLC的S7协议进行设备连接判断

6. 安装博图软件创建虚拟PLC进行测试

---
### Implementation（实现）

##### 通过Scapy模块发送ARP包获取指定网卡设备的IP和MAC地址

1. 获取当前设备的网卡设备
   1. 使用psutil模块的net_if_addrs().items()方法  
      [example](../module/获取当前设备网卡设备及其IP地址.py)  
      使用到的方法 文档地址:  
      [pstuil.net_if_addrs().items](https://hellowac.github.io/psutil-doc-zh/system/network/net_if_addrs.html)  
      [socket.AF_INET](https://docs.python.org/3/library/socket.html#socket.AF_INET)  
      限定IPV4方法：因为AF_INET是IPV4的协议族  
      限定IPV4的原因是ARP是基于IPV4的协议。且Siemens PLC设备也是基于IPV4的协议。

2. 扫描指定网卡设备的IP段（CIDR 表示法）

   ```
   scan_network 函数
   ip_range:
   要扫描的 IP 地址范围，通常是一个 CIDR 表示法，如 192.168.1.0/24。
   指定要扫描的网络段，以便确定哪些设备在线。
   arp_request:
   类型: ARP 实例。
   生成一个 ARP 请求，用于查询 IP 地址对应的 MAC 地址。
   ARP 协议用于在同一局域网中解析 IP 地址到 MAC 地址，获取设备信息。
   ether:
   类型: Ether 实例。
   创建一个以太网帧，目标地址为广播地址 ff:ff:ff:ff:ff:ff。
   发送广播帧以确保网络中的所有设备都能接收到 ARP 请求。
   packet:
   类型: 组合的以太网帧和 ARP 请求。
   封装后的数据包，包含了以太网和 ARP 请求的信息。
   将 ARP 请求和以太网帧组合在一起以进行发送。
   result:
   类型: ARP 响应的列表。
   srp 函数的返回值，其中包含发送和接收的包。
   获取响应以确定哪些设备在线。
   devices:
   类型: 列表。
   存储在线设备的字典，包含 IP 和 MAC 地址。
   收集并返回扫描到的设备信息。
   display_devices 函数
   devices:
   列表。
   包含在线设备的字典列表，通常来自 scan_network 的返回值。
   传递已扫描到的设备以便打印输出。
   ```

   文档地址

   [Arp](https://scapy.readthedocs.io/en/latest/usage.html#arp)  [Ether](https://scapy.readthedocs.io/en/latest/usage.html#ether)  [Srp](https://scapy.readthedocs.io/en/latest/usage.html#srp)



---

### 遇到的问题

1. Scapy的import方式
   [stackoverflow_解决方式](https://stackoverflow.com/questions/63645535/arp-in-scapy-not-working-and-getting-an-error-cannot-find-reference-arp-in-a)
2. Scapy需要Wincap支持
   [Wincap下载地址](https://www.winpcap.org/install/default.htm)

---

### 参考文档

1. [西门子S7系列中间人攻击：流量劫持和转发（一）](https://www.freebuf.com/articles/ics-articles/231701.html)
2. [手摸手教你撕碎西门子S7通讯协议01--S7协议介绍](https://blog.csdn.net/hqwest/article/details/139346989)
3. [西门子——博图V16与PLCSIM Advanced仿真通讯配置（1500系列）](https://blog.csdn.net/qq_42504097/article/details/125394487)

