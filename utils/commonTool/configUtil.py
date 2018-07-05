# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"

import os
import yaml
from utils.log.mylog import MyLogger

# ROOT = os.path.abspath(os.path.join(os.path.join(os.getcwd(), os.path.pardir), os.path.pardir))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE_DIR)
log = MyLogger()


class ConfigUtil(object):
    @classmethod
    def getall(cls, path='\\config\\buydodo.yml'):
        """获取配置文件中的配置，返回string"""
        log.info("读取%s配置文件中的配置数据" % path)
        file_path = ROOT + path
        str = yaml.load(open(file_path, 'r'))
        log.info("配置数据为%s" % str)
        return str

    @classmethod
    def get(cls, section, option='', path='\\config\\buydodo.yml'):
        """获取配置文件中的配置，返回string"""
        log.info("读取%s配置文件中的配置数据" % path)
        file_path = ROOT + path
        config = yaml.load(open(file_path, 'r'))
        if option:
            result = config[section][option]
        else:
            result = config[section]
        log.info("配置数据为%s" % result)
        return str(result) if isinstance(result, (str, int)) else result

    @classmethod
    def getint(cls, section, option='', path='\\config\\buydodo.yml'):
        """获取配置文件中的配置，返回int"""
        log.info("读取%s配置文件中的配置数据" % path)
        file_path = ROOT + path
        config = yaml.load(open(file_path, 'r'))
        if option:
            log.info("配置数据为%s" % int(config[section][option]))
            return int(config[section][option])
        else:
            log.info("配置数据为%s" % int(config[section]))
            return int(config[section])
