系统:linux
数据库: mysql5.7+
python:3.5+
安装 supervisor

创建数据库 tencent 字符编码utf-8

下载代码: git clone https://github.com/l3n641/tencent-tool.git

进入项目,创建虚拟环境: python3 -m venv .venv

激活虚拟环境: source ./.venv/bin/activate

复制 env 改名 .env 并且填写mysql 账号和密码

安装requirements.txt依赖: pip install -r requirements.txt

运行数据库迁移工具:flask db upgrade

添加 supervisor 配置文件:
[program:tencent]
command=/data/tencent-tool/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 manage:app
directory=/data/tencent-tool
umask=022
startsecs=0
stopasgroup=true
stopwaitsecs=3
redirect_stderr=true
stdout_logfile=/data/logs/work.log
autorestart=true
autostart=false

重新加载配置文件:supervisorctl reload
执行supervisor:supervisorctl start tencent

配置 nginx:

server {
    listen 80;
    server_name datamofo.cn; # 这是HOST机器的外部域名，用地址也行

    location / {
        proxy_pass http://127.0.0.1:8000; # 这里是指向 gunicorn host 的服务地址
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
 }

创建账号:flask create-user

登陆页面: http://datamofo.cn/auth/login















