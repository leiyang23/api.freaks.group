# 主机信息监控模块
作为`Django 3.0`的一个应用，可以方便的查看本机的基础信息（内存、磁盘、负载等）。   
自带可视化界面。   

## 依赖
依赖于django channels模块实现websocket。为了应对并发访问，引入了redis、apscheduler等库。       

## 配置   
1. settings.py 注册 `spy` 应用，并配置asgi 入口，详细可以参考 channels 的文档。  
2. settings.py 添加 redis 的连接信息，用来保存采集的信息。   
3. 在 asgi 的入口文件中添加`spy`应用的路由。    

## 访问地址
`/spy/index`