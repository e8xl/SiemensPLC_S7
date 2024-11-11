# SiemensPLC_Project1

### Requirements（需求） 

设计一个程序，能够搜索子网内的西门子PLC设备，并把搜索到的设备在列表中显示出来。

### Analysis（分析）

1. Siemens PLC 子网设备使用TCP/IP方式连接

2. 使用snap7模块对指定网卡进行依次连接

3. 使用多线程优化连接速度

---
### Implementation（实现）

##### 通过snap7对相应网卡子网段进行依次连接

1. 获取当前设备的网卡设备
   1. 使用psutil模块的net_if_addrs().items()方法  
      [example](./module/获取当前设备网卡设备及其IP地址.py)  
      使用到的方法 文档地址:  
      [pstuil.net_if_addrs().items](https://hellowac.github.io/psutil-doc-zh/system/network/net_if_addrs.html)  
      [socket.AF_INET](https://docs.python.org/3/library/socket.html#socket.AF_INET)  
      限定IPV4方法：因为AF_INET是IPV4的协议族  
      限定IPV4的原因是ARP是基于IPV4的协议。且Siemens PLC设备也是基于IPV4的协议。

2. 使用snap7对网卡设备子网段进行依次连接
    1. 使用snap7.client.Client()方法连接  
        [example](./module/snap7连接PLC.py)  
        使用到的方法 文档地址:  
        [snap7.client.Client](https://python-snap7.readthedocs.io/en/latest/snap7.client.html#snap7.client.Client)

3. 使用concurrent.futures进行多线程优化
    1. 使用concurrent.futures.ThreadPoolExecutor()方法
        使用到的方法 文档地址:  
        [concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)  
        [concurrent.futures.as_completed](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.as_completed)  
        [concurrent.futures.Future](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future)  
        [concurrent.futures.Executor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor)  
        [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
---

### 遇到的问题

1. [CLI: function refused by CPU(Unknown error)](https://blog.csdn.net/u013551122/article/details/118384698)
2. [S7-PLCSIM Advanced V4.0 SP1](https://www.bilibili.com/video/BV1PY411o7jg/)


---

### 参考文档

1. [西门子S7系列中间人攻击：流量劫持和转发（一）](https://www.freebuf.com/articles/ics-articles/231701.html)
2. [手摸手教你撕碎西门子S7通讯协议01--S7协议介绍](https://blog.csdn.net/hqwest/article/details/139346989)
3. [西门子——博图V16与PLCSIM Advanced仿真通讯配置（1500系列）](https://blog.csdn.net/qq_42504097/article/details/125394487)
4. [snap7-python](https://python-snap7.readthedocs.io/en/latest/)
5. [基于snap7模块 使用pycharm 实现plc通讯读写数据块数据](https://www.bilibili.com/video/BV13N411j7yz/)