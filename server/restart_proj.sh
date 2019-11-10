#!/usr/bin bash
echo "正在重启项目。。。"

echo "web 服务器重启。。。"
killall -9 uwsgi3;
killall -9 uwsgi3;
killall -9 uwsgi3;
uwsgi3 -i /www/wwwroot/api.freaks.group/server/uwsgi.ini;
supervisorctl restart daphne;
echo "web 服务器已启动"

echo "celery 重启。。。"
/etc/init.d/celeryd restart;
/etc/init.d/celerybeat restart;
echo "celery 已启动"

echo "项目已启动"
