import time
import re
import platform
from dataclasses import dataclass, field

import psutil
import paramiko
import chardet


def monitor_info():
    """返回主机监控信息"""

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


@dataclass(unsafe_hash=True)
class SSH:
    host: str
    username: str
    password: str
    port: int = field(default=22, )
    _trans: paramiko.Transport = None
    _create_time: float = field(default=time.time(), hash=True)

    def __post_init__(self):
        self._trans = self._transport()

    def _transport(self):
        try:
            self.port = int(self.port)
            t = paramiko.Transport((self.host, self.port))
            t.connect(username=self.username, password=self.password)
            print("已连接")
            return t
        except Exception as e:
            raise ConnectionError

    def get_ssh(self):
        ssh = paramiko.SSHClient()
        ssh._transport = self._trans
        return ssh

    def get_shell(self):
        ssh = self.get_ssh()
        return ssh.invoke_shell()

    @staticmethod
    def cmd(s, command):
        time.sleep(.3)
        s.send(command + "\n")

        resp = b""
        while True:
            time.sleep(.5)
            ret = s.recv(1024)
            resp += ret
            if len(ret) < 1024:
                break

        char = chardet.detect(resp)
        encoding = "utf-8" if char['encoding'] is None else char['encoding']
        resp = resp.decode(encoding)

        pat = "\033[[\d;]+m"  # 清除 彩色控制符
        resp = re.sub(pat, '', resp)

        return resp


if __name__ == '__main__':
    '(read_count     =1621962, write_count=3127916, read_bytes=34730353152, write_bytes=111218112512, read_time=1575, write_time=1001)'
    print(monitor_info())

    h = SSH("47.111.175.222", 22, "root", "1005931665Ecs")

    sh = h.get_shell()
    h.cmd(sh, "ls")
    h.cmd(sh, "cd /home/")
    h.cmd(sh, "ls ")
