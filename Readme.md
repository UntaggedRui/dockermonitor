使用cadvisor和influxdb实现的容器监控demo，主页面只有三个div，可以集成到自己已有的管理系统中。
因为我是集成到openstack中的，所以使用的是python2，感觉python3也能运行吧。。。
# 使用教程
首先在你需要监控的机器上安装cadvisor采集容器信息，并保存到influxdb数据库中。
1. 安装influxdb
   1.1  `sudo docker run -d -p 8083:8083 -p 8086:8086 --name influxdb tutum/influxdb` 启动数据库容器
   1.2  打开`http://localhost:8083/`数据库后台管理,创建数据库`CREATE DATABASE "cadvisor"` cadvisor为数据库名
   1.3 配置角色权限 `CREATE USER "root" WITH PASSWORD 'root' WITH ALL PRIVILEGES` 账号密码都是root
2. 安装cAdvisor
`sudo docker run -d --name cadvisor -p 8080:8080 --volume=/:/rootfs:ro --volume=/var/run:/var/run:ro --volume=/sys:/sys:ro --volume=/var/lib/docker/:/var/lib/docker:ro --volume=/dev/disk/:/dev/disk:ro google/cadvisor -storage_driver=influxdb -storage_driver_db=cadvisor -storage_driver_user=root -storage_driver_password=root -storage_driver_host=192.168.1.8:8086` 启动cAdvisor容器,并使用influxdb为存储(cadvisor数据库名, 数据访问账号密码root, 地址为本地8086端口,别用127.0.0.1.连不上)
3. 安装我写的代码 
  3.1 git clone本仓库到本地后，pip安装requirments。
  3.2 修改数据库连接
  在`/my_app/views/py`文件开始的部分修改数据库的ip地址，用户名，密码。
  3.3 运行`python manage.py runserver 0.0.0.0:7777`，访问后就可以看到容器的数据了
![你好](/static/demo.jpg)


```

```

