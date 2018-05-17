# PHP微服务Docker镜像描述

主要整合了常用几个服务，并替换了一些源码下载地址为国内的，比如alpine，composer

至于为何PHP环境有Python，这里主要考虑到进程管理和到时候用Python 程序作为Eureka Client注册和续约服务。

[Docker Registry doubleshit/lnpps](https://hub.docker.com/r/doubleshit/lnpps/)

## 环境

- PHP：7.1

- Python： 2.7.15 / 3.6.5

- Nginx: 1.14.0

- PHP-FPM

- Supervisor

- Composer

## 开放端口

- `80` Nginx端口，默认提供`/var/www/html`下的web服务

- `9000` PHP-FPM 服务端口

- `9001` Supervisor在线管理端口

## 环境主要信息

`PHP`

```code
Configuration File (php.ini) Path => /usr/local/etc/php

Scan this dir for additional .ini files => /usr/local/etc/php/conf.d

```

`Python`

```code
/usr/local/bin/pip
/usr/local/bin/pip3
/usr/local/bin/python
/usr/local/bin/python3
```

`Nginx`

```code
主配置：/etc/nginx/nginx.conf
默认网站配置：/etc/nginx/conf.d/default.conf
其它网站配置目录：/etc/nginx/conf.d/
```

`PHP-FPM`

```code
configuration file /usr/local/etc/php-fpm.conf
Pool Definitions /usr/local/etc/php-fpm.d/
```

`Supervisor`

```code
主配置：`/etc/supervisord.conf`

进程配置：`/etc/supervisor.conf.d/` *建议一个单独的服务依赖进程都归并到一个文件*
```

`EntryPoint启动脚本`：

`/start.sh` *主要用于运行supervisor，其它进程在supervisor里面配置*

如果有一些在运行时需要运行一次，非守护进程类型的，可以复制这个文件，把命令加到`exec supervisord -c /xxxxxx`这条启动supervisor的命令前面。

然后Dockerfile把它COPY 到根目录即可。如：`COPY start.sh /start.sh`

基础镜像启动时，entryponit默认就是执行这个脚本。只要复制到对的路径，无需另外添加CMD命令或者ENTRYPOINT命令来执行它。

`网站默认路径`:

 `/var/www/html`
