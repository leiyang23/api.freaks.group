#!/usr/bin bash
echo "正在启动项目。。。"

echo "web 服务器启动。。。"
kill -9 $(pidof uwsgi3)
uwsgi3 -i /www/wwwroot/api.freaks.group/server/uwsgi.ini;
supervisorctl start daphne;
echo "web 服务器已启动"

echo "celery 启动。。。"
sh /www/wwwroot/api.freaks.group/server/celery/celeryd.sh start;
sh /www/wwwroot/api.freaks.group/server/celery/celerybeat.sh start;
echo "celery 已启动"

echo "项目已启动"