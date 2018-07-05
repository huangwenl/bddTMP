# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"
import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE_DIR)

class MyLogger(object):
    logger = logging.getLogger('my_color_logger')
    resultPath = os.path.join(ROOT, "result")

    # 如果不存在文件夹创建文件夹
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)
    # 以时间格式命名运行结果文件名
    logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d")))
    # 创建保持日志文件夹
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    # 定义日志级别
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger_handler = logging.FileHandler(os.path.join(logPath, str(datetime.now().strftime("%Y%m%d")) + ".log"))
        formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
        logger_handler.setFormatter(formatter)
        logger.addHandler(logger_handler)

    @classmethod
    def debug(cls, msg):
        cls.logger.debug(str(msg))

    @classmethod
    def info(cls, msg):
        cls.logger.info(str(msg))

    @classmethod
    def error(cls, msg):
        cls.logger.error(str(msg))

    @classmethod
    def warn(cls, msg):
        cls.logger.warning(str(msg))

# logs = MyLogger()
# logs.info("huangwenliang")