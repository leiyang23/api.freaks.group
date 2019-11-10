### 部署
#### nginx   
nginx 的管理使用 宝塔面板。

#### django 服务器   
1. 安装 supervisor   
supervisor 是一个 python 的进程管理库。
Centos 下直接 `yum install supervisor`，其配置文件 /etc/supervisord.conf 文件中，在此文件中我们可以指定自己的 program 的配置地址。  
常用命令：`supervisorctl start/stop/restart/status [program]`。   

2. 安装 uWSGT 和 daphne   
`pip3 install uwsgi` `pip3 install daphne`。   
安装后的启动命令在 /usr/local/python3/bin/ 目录下。 

3. 配置
程序的配置在 supervisor 的配置文件中以 includes 的形式导入，因此只需将程序的配置文件地址注册到 supervisor的配置文件中就可以了。  

#### celery  
1. 注册服务  
从celery仓库里复制celery/extra/generic-init.d/中的两个文件到Centos系统的 /etc/rc.d/init.d/ 目录下，完成服务注册。   
`celeryd` 和 `celerybeat` 分别用来管理 worker 和 beat 任务。用法：/etc/init.d/celeryd {start|stop|restart|status}。 

2. 配置文件    
这两个服务使用的配置文件在 /etc/default/ 目录下的同名文件中。     
配置文件编写参考官方文档 [Generic init-scripts](http://docs.celeryproject.org/en/latest/userguide/daemonizing.html#generic-init-scripts)方式。   