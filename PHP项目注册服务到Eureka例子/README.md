# 注册PHP项目到eureka的例子

例子项目结构如下：

```bash
example-use-sidecar
├── code # 网站代码目录 对应Dockerfile里面的COPY到/var/www/html目录
│   └── index.php
├── conf # 一些配置，如nginx，supervisor的
│   ├── default # nginx默认网站配置
│   └── services.ini # 名字随意，后缀必须.ini，supervisor配置
├── Dockerfile 
├── env # 环境配置 目录名对应 Dockerfile中的 RUN_ENV 值，在build中复制环境配置
│   ├── dev
│   │   └── config.php
│   └── prod
│       └── config.php
├── README.md
└── sidecar.py # 注册到Eureka的脚本，可以不提供status信息。
```

`sidecar.py`

目前只是一个简单的服务注册脚本。

和官方的sidecar不同，它不检测status信息确认目标是否存活。

在注册之后，定时renew刷新保持注册记录。

如果容器退出了，它自然也挂了。缺陷是如果是nginx或者php进程挂了。不能正常提供web服务，它还会继续把服务注册在线。

## 怎么添加一个进程让它持续执行。

添加一个supervisor的配置行了。

然后添加它到`/etc/supervisor.conf.d/`目录即可。

如我要挂着`sidecar.py`让它不断执行注册服务。

新建一个`services.ini`文件

```ini
[program:sidecar]
command=python3 /sidecar.py ; the program (relative uses PATH, can take args)
;process_name=%(program_name)s ; process_name expr (default %(program_name)s)
;numprocs=1                    ; number of processes copies to start (def 1)
;events=EVENT                  ; event notif. types to subscribe to (req'd)
;buffer_size=10                ; event buffer queue size (default 10)
;directory=/tmp                ; directory to cwd to before exec (def no cwd)
;umask=022                     ; umask for process (default None)
;priority=-1                   ; the relative start priority (default -1)
autostart=true                ; start at supervisord start (default: true)
;startsecs=1                   ; # of secs prog must stay up to be running (def. 1)
;startretries=3                ; max # of serial start failures when starting (default 3)
;autorestart=unexpected        ; autorestart if exited after running (def: unexpected)
;exitcodes=0,2                 ; 'expected' exit codes used with autorestart (default 0,2)
;stopsignal=QUIT               ; signal used to kill process (default TERM)
;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
;stopasgroup=false             ; send stop signal to the UNIX process group (default false)
;killasgroup=false             ; SIGKILL the UNIX process group (def false)
;user=chrism                   ; setuid to this UNIX account to run the program
redirect_stderr=true         ; redirect_stderr=true is not allowed for eventlisteners
stdout_logfile=/dev/stdout      ; stdout log path, NONE for none; default AUTO
stdout_logfile_maxbytes=0   ; max # logfile bytes b4 rotation (default 50MB)
;stdout_logfile_backups=10     ; # of stdout logfile backups (0 means none, default 10)
;stdout_events_enabled=false   ; emit events on stdout writes (default false)
;stderr_logfile=/dev/stderr      ; stderr log path, NONE for none; default AUTO
;stderr_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stderr_logfile_backups=10     ; # of stderr logfile backups (0 means none, default 10)
;stderr_events_enabled=false   ; emit events on stderr writes (default false)
;environment=A="1",B="2"       ; process environment additions
;serverurl=AUTO                ; override serverurl computation (childutils)
```

关键配置有：

```ini
[program:sidecar] ;起个名字，显示在supervisor中方便管理的
command=python3 /sidecar.py ;运行额命令或脚本
redirect_stderr=true ; 重定向错误输出
stdout_logfile=/dev/stdout ; 打印日志到stdout 这样docker logs可以看到
stdout_logfile_maxbytes=0 ; 输出到stdout设备，这个设置为0，不然有异常
```

`Dockerfile`

```dockerfile
FROM doubleshit/lnpps:php7.1
# 声明运行环境
ENV RUN_ENV=dev
# 复制网站源码
COPY --chown=www-data:www-data ./code /var/www/html
# 复制配置文件
COPY --chown=www-data:www-data ./env/${RUN_ENV} /var/www/html
# 复制nginx默认网站配置
COPY ./conf/default /etc/nginx/conf.d/default.conf
# 配置Sidecar
COPY ./sidecar.py /sidecar.py
RUN pip3 install wasp-eureka asyncio -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# 复制supervisor配置文件，主要配置运行了sidecar.py
COPY ./conf/services.ini /etc/supervisor.conf.d/
```
