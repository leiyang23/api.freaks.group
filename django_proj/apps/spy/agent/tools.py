import os
import platform


def get_cpu_model():
    if platform.system().lower() == "windows":
        return ""
    model = os.popen("cat /proc/cpuinfo |grep 'model name' |sed 's/model name\t: //g' |tail -n 1 2>/dev/null").read()
    if isinstance(model, bytes):
        model = model.decode("utf8")
    return model
