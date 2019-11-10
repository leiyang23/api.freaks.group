#!/usr/bin bash
echo "正在重启项目。。。"

echo "web 服务器重启。。。"
supervisorctl reatart uwsgi;
supervisorctl reatart daphne;
echo "web 服务器已启动"

echo "celery 重启。。。"
/etc/init.d/celeryd reatart;
/etc/init.d/celerybeat reatart;
echo "celery 已启动"

echo "项目已启动"
