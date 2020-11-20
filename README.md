# 卫星链路拥塞控制
## 文件及目录说明
+ single.py: Mininet脚本，包括拓扑定义（h1与h2
节点）、链路动态调整线程
+ client.py: h2节点调用的TCP连接客户端
+ server.py: h1节点调用的TCP连接服务器
+ log: 每次实验中，记录链路状态变化和实际传输速率变化的日志
+ mymodule: 可编译为Linux内核模块的代码