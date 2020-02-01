"""
celery 应用只能从此读取配置文件，读取不到 celery_proj 以外的文件，
之所以将 celery 应用放到 django 内，是为了 django 读取 celery的任务，
如果放平级，无论怎么导入，celery 和 django 中的模块总有读取出现问题的一方。
"""
import logging

DEBUG = False

REDIS_HOST = '127.0.0.1' if DEBUG else '47.111.175.222'
REDIS_PWD = "" if DEBUG else "fuckyou!"

# 配置邮箱
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'leiyang_ace@163.com'  # 帐号
EMAIL_HOST_PASSWORD = '1005931665sqm'  # 密码


# logging 配置
logger = logging.getLogger("调试信息")
logger.setLevel(logging.ERROR)

ch = logging.StreamHandler()
format_console = logging.Formatter("%(filename)s - %(levelname)s - %(lineno)s - %(message)s")

ch.setFormatter(format_console)

logger.addHandler(ch)
