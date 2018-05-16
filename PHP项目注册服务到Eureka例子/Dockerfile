FROM doubleshit/lnpps:php7.1
# 声明运行环境
ENV RUN_ENV=dev
# 复制网站源码
COPY --chown=www-data:www-data ./code /var/www/html
# 复制配置文件
COPY --chown=www-data:www-data ./env/${RUN_ENV} /var/www/html
# 复制nginx默认网站配置
COPY ./conf/default /etc/nginx/conf.d/default.conf
# 配置Sidecar 该脚本的依赖装在基础镜像中了。
COPY ./sidecar.py /sidecar.py
# 复制supervisor配置文件，主要配置运行了sidecar.py
COPY ./conf/services.ini /etc/supervisor.conf.d/