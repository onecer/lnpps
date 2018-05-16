# PHP微服务Docker镜像描述

主要整合了常用几个服务，并替换了一些源码下载地址为国内的，比如apline，composer

至于为何PHP环境有Python，这里主要考虑到进程管理和到时候用Python 程序作为Eureka Client注册和续约服务。

## 环境

- PHP：7.1

- Python： 2.7

- Nginx: 1.14.0

- PHP-FPM

- Supervisor

- Composer

## 开放端口

- `80` Nginx端口，默认提供`/var/www/html`下的web服务

- `9000` PHP-FPM 服务端口

- `9001` Supervisor在线管理端口

## 环境主要配置路径

`PHP`

PHP.ini:

Python

Nginx

主配置：/etc/nginx/nginx.conf
默认网站配置：/etc/nginx/conf.d/default.conf
其它网站配置目录：/etc/nginx/conf.d/

PHP-FPM

Supervisor

主配置：`/etc/supervisord.conf`

进程配置：`/etc/supervisor.conf.d/` *建议一个单独的服务依赖进程都归并到一个文件*

EntryPoint启动脚本：`/start.sh` *主要用于运行supervisor，其它进程在supervisor里面配置*

网站默认路径 `/var/www/html`

## 使用例子

