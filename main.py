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
    from ayaled import AyaLed,Color
    logging.info("ayaled main.py")
except Exception as e:
    logging.error(e)

ledon=True
red=255
green=255
blue=255

class Plugin:
    async def _main(self):
        while True:
            await asyncio.sleep(3)

    def set_ledOn(self, r: int, g: int, b: int):
        try:
            global ledon
            ledon=True
            self.set_ledRGB(r,g,b)
            logging.info(f"set_ledOn:{True}")
        except Exception as e:
            logging.error(e)
            return False
    
    def set_ledOff(self):
        try:
            global ledon
            ledon=False
            AyaLed.set_all_pixels(Color(0,0,0))
            logging.info(f"set_ledOn:{False}")
        except Exception as e:
            logging.error(e)
            return False

    def set_ledRGB(self, r: int, g: int, b: int):
        try:
            if ledon:
                global red,green,blue
                red=r
                green=g
                blue=b
                AyaLed.set_all_pixels(Color(red,green,blue))
                logging.info(f"set_ledOn:{red},{green},{blue}")
            else:
                AyaLed.set_all_pixels(Color(0,0,0))
                logging.info(f"set_ledOn:{0},{0},{0}")
        except Exception as e:
            logging.error(e)
            return False
