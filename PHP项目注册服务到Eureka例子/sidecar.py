# coding: utf-8
import os
import asyncio
from wasp_eureka import EurekaClient

SERVICE_NAME = 'JOKE-SERVICE'
SERVICE_IP = '120.79.138.224'
SERVICE_PORT = 9999
EUREKA_URL = 'http://120.79.138.224:8761'
HOSTNAME = "localhost"
INSTANCE_ID = "{}:{}".format(SERVICE_IP, SERVICE_PORT)

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
