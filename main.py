import subprocess
import asyncio
import os
import sys

#获取插件路径 加载backend中各个py文件
try:
    from helpers import get_homebrew_path,get_home_path,get_user
    HOMEBREW_PATH = get_homebrew_path(get_home_path(get_user()))   
    sys.path.append("{}/plugins/ayaled/backend".format(HOMEBREW_PATH))
    from config import logging
    logging.info("ayaled main.py")
except Exception as e:
    logging.error(e)

class Plugin:
    async def _main(self):
        while True:
            await asyncio.sleep(3)

    def set_lightOff(self, value: bool):
        try:
            logging.info("set_lightOff")
        except Exception as e:
            logging.error(e)
            return False
