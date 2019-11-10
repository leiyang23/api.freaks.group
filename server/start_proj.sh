#!/usr/bin bash
echo "正在重启项目。。。"

echo "web 服务器启动。。。"
supervisorctl start uwsgi;
supervisorctl start daphne;
echo "web 服务器已启动"

echo "celery 启动。。。"
/etc/init.d/celeryd start;
/etc/init.d/celerybeat start;
echo "celery 已启动"

echo "项目已启动"