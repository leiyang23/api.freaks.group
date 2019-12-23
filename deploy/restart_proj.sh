#!/usr/bin bash
echo "正在重启项目。。。"

echo "web 服务器重启。。。"
kill -9 $(pidof uwsgi3)
uwsgi3 -i /home/api.freaks.group/deploy/uwsgi.ini;
supervisorctl restart daphne;
echo "web 服务器已启动"

echo "celery 重启。。。"
sh /home/api.freaks.group/deploy/celery/celeryd.sh restart;
sh /home/api.freaks.group/deploy/celery/celerybeat.sh restart;
echo "celery 已启动"

echo "项目已启动"
