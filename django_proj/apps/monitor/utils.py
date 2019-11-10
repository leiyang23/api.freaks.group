def monitor_info():
    """返回主机监控信息"""
    import psutil
    import time
    import platform

    # 操作系统信息
    res = {
        "os": {
            "system": platform.system(),
            "version": platform.release(),
        }
    }
    # 开机时长
    t = time.time() - psutil.boot_time()
    days = int(t / 24 / 3600)
    hours = int((t - days * 24 * 3600) / 3600)
    minutes = int((t - days * 24 * 3600 - hours * 3600) / 60)
    res['work_time'] = {"days": days, "hours": hours, "minutes": minutes}

    # cpu 占用及核数
    res['cpu'] = {
        "cores": psutil.cpu_count(logical=False),
        'load': psutil.cpu_percent(percpu=False)
    }

    # 内存情况
    mem = psutil.virtual_memory()
    res['memory'] = {"total": mem.total, "used": mem.used, "available": mem.available, "percent": mem.percent}

    # 存储
    disk = psutil.disk_usage("/")
    res['disk'] = {"total": disk.total, "used": disk.used, "percent": disk.percent}

    # 负载
    load = psutil.getloadavg()
    res['load'] = {"mins_1": load[0], "mins_5": load[1], "mins_15": load[2]}

    # 连接数
    res['conn'] = len(psutil.net_connections(kind="all"))

    # 磁盘IO
    # disk_io = psutil.disk_io_counters()
    # print(disk_io)
    # read_rate = disk_io.read_bytes / disk_io.read_time * 1000 / 1024
    # write_rate = disk_io.write_bytes / disk_io.write_time * 1000 / 1024
    # print(read_rate, write_rate)

    return res


if __name__ == '__main__':
    '(read_count     =1621962, write_count=3127916, read_bytes=34730353152, write_bytes=111218112512, read_time=1575, write_time=1001)'
    print(monitor_info())
