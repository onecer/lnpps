# coding: utf-8
import os
import asyncio
from wasp_eureka import EurekaClient

"""
这里配置注册到Eureka的服务信息。

主要有服务名，端口，IP，Eureka Server服务地址，实例ID

这些信息也可以通过运行时 通过环境变量传递进来。

环境变量配置信息优先级高于默认配置的。

如果环境变量相关信息为空，则使用默认参数
"""
# 服务名
SERVICE_NAME = 'JOKE-SERVICE'
# 服务IP
SERVICE_IP = '127.0.0.1'
# 服务开放端口
SERVICE_PORT = 9999
# Eureka Server地址
EUREKA_URL = 'http://127.0.0.1:8761'
# 主机名
HOSTNAME = "localhost"
# 注册到Eureka的实例ID

env_dict = os.environ

SERVICE_NAME = SERVICE_NAME if not 'SERVICE_NAME' in env_dict.keys() else env_dict['SERVICE_NAME']
SERVICE_IP = SERVICE_IP if not 'SERVICE_IP' in env_dict.keys() else env_dict['SERVICE_IP']
SERVICE_PORT = SERVICE_PORT if not 'SERVICE_PORT' in env_dict.keys() else env_dict['SERVICE_PORT']
EUREKA_URL = EUREKA_URL if not 'EUREKA_URL' in env_dict.keys() else env_dict['EUREKA_URL']
HOSTNAME = HOSTNAME if not 'HOSTNAME' in env_dict.keys() else env_dict['HOSTNAME']
INSTANCE_ID = INSTANCE_ID if not 'INSTANCE_ID' in env_dict.keys() else env_dict['INSTANCE_ID']

loop = asyncio.get_event_loop()

eureka = EurekaClient(app_name=SERVICE_NAME,
                      ip_addr=SERVICE_IP,
                      port=SERVICE_PORT,
                      hostname=HOSTNAME,
                      eureka_url=EUREKA_URL,
                      loop=loop,
                      instance_id=INSTANCE_ID)

async def main():
    await eureka.register()

    while True:
        await asyncio.sleep(40)
        await eureka.renew()

if __name__ == "__main__":
    loop.run_until_complete(main())
