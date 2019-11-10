#!/usr/bin bash
echo "正在启动项目。。。"

echo "web 服务器启动。。。"
killall -9 uwsgi3;
killall -9 uwsgi3;
killall -9 uwsgi3;
uwsgi3 -i /www/wwwroot/api.freaks.group/server/uwsgi.ini;
supervisorctl start daphne;
echo "web 服务器已启动"

echo "celery 启动。。。"
/etc/init.d/celeryd start;
/etc/init.d/celerybeat start;
echo "celery 已启动"

echo "项目已启动"