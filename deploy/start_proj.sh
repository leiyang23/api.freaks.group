#!/usr/bin bash
echo "正在启动项目。。。"

echo "web 服务器启动。。。"
kill -9 $(pidof uwsgi3)
uwsgi3 -i /home/api.freaks.group/deploy/uwsgi.ini;
supervisorctl start daphne;
echo "web 服务器已启动"

echo "celery 启动。。。"
sh /home/api.freaks.group/deploy/celery/celeryd.sh start;
sh /home/api.freaks.group/deploy/celery/celerybeat.sh start;
echo "celery 已启动"

echo "项目已启动"