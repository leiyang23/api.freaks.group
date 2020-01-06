import redis
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

from celery_proj import settings
from celery_proj.app import app


@app.task()
def reset_api_times():
    """定时任务：每天凌晨清除百度云接口调用量"""
    with redis.Redis(host=settings.REDIS_HOST, password=settings.REDIS_PWD, db=9) as redis_client:
        redis_client.delete("ocr_type")


@app.task()
def send_email(receivers: list, subject: str, con: str):
    msg = MIMEText(con, 'html', 'utf-8')
    msg['From'] = formataddr(("leon", settings.EMAIL_HOST_USER))
    msg['To'] = formataddr((None, '; '.join(receivers)))
    msg['Subject'] = Header(subject, 'utf-8').encode()

    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, 465, timeout=30)  # SMTP协议默认端口是25，SMTP_SSL使用 465，
    # deploy.set_debuglevel(1)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(settings.EMAIL_HOST_USER, receivers, msg.as_string())
    server.quit()
    return True
