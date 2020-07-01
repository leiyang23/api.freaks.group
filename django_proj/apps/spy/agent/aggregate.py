import time
import platform

import psutil

from spy.agent.tools import get_cpu_model


def base():
    """ 机器基础信息 """

    # 开机时长
    t = time.time() - psutil.boot_time()
    days = int(t / 24 / 3600)
    hours = int((t - days * 24 * 3600) / 3600)
    minutes = int((t - days * 24 * 3600 - hours * 3600) / 60)
    work_time = {"days": days, "hours": hours, "minutes": minutes}

    # cpu
    cpu = {
        "model": get_cpu_model(),
        "num": psutil.cpu_count(logical=False),
    }

    # 磁盘信息
    disks = list()
    for disk in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(disk.mountpoint)
        disks.append(
            {"mount": disk.mountpoint,
             "total": disk_usage.total,
             "used": disk_usage.used,
             "percent": disk_usage.percent}
        )

    return {
        "uname": dict(platform.uname()._asdict()),
        "disks": disks,
        "work_time": work_time,
        "cpu": cpu,
        "time": int(time.time())
    }


def realtime(interval=10):
    """ 实时性能 """

    pre_net_io = psutil.net_io_counters(pernic=True)
    pre_disk_io = psutil.disk_io_counters(perdisk=True)

    # CPU
    # blocking interval
    # time.sleep(interval)
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=True)

    # 网速
    speed_net_io = dict()
    for card_name, now_net_io in psutil.net_io_counters(pernic=True).items():
        if card_name.startswith("eth") or card_name.startswith("以太网"):
            speed_bytes_sent = (now_net_io.bytes_sent - pre_net_io[card_name].bytes_sent) / interval
            speed_bytes_recv = (now_net_io.bytes_recv - pre_net_io[card_name].bytes_recv) / interval
            speed_packets_sent = (now_net_io.packets_sent - pre_net_io[card_name].packets_sent) / interval
            speed_packets_recv = (now_net_io.packets_recv - pre_net_io[card_name].packets_recv) / interval

            speed_net_io.update({card_name: [speed_bytes_sent, speed_bytes_recv, speed_packets_sent, speed_packets_recv]})

    # 磁盘读写
    speed_disk_io = dict()
    for disk_name, now_disk_io in psutil.disk_io_counters(perdisk=True).items():
        speed_read_bytes = (now_disk_io.read_bytes - pre_disk_io[disk_name].read_bytes) / interval
        speed_write_bytes = (now_disk_io.write_bytes - pre_disk_io[disk_name].write_bytes) / interval

        speed_disk_io.update({disk_name: [speed_read_bytes, speed_write_bytes]})

    # 内存
    virtual_memory = dict(psutil.virtual_memory()._asdict())

    # 整体负载
    load = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]

    return {
        "net_io": speed_net_io,
        "disk_io": speed_disk_io,
        "cpu_percent": cpu_percent,
        "virtual_memory": virtual_memory,
        "load": load,
        "time": int(time.time())
    }


if __name__ == '__main__':
    # print(base())
    start = time.perf_counter()
    print(realtime(3))
    print(f"{time.perf_counter() - start}")
