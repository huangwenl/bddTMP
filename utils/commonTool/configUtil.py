# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"

import os
import yaml

# ROOT = os.path.abspath(os.path.join(os.path.join(os.getcwd(), os.path.pardir), os.path.pardir))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE_DIR)

class ConfigUtil(object):
    @classmethod
    def getall(cls, path='\\config\\buydodo.yml'):
        """获取配置文件中的配置，返回string"""
        file_path = ROOT + path
        return yaml.load(open(file_path, 'r'))

    @classmethod
    def get(cls, section, option='', path='\\config\\buydodo.yml'):
        """获取配置文件中的配置，返回string"""
        file_path = ROOT + path
        config = yaml.load(open(file_path, 'r'))
        if option:
            result = config[section][option]
        else:
            result = config[section]
        return str(result) if isinstance(result, (str, int)) else result

    @classmethod
    def getint(cls, section, option='', path='\\config\\buydodo.yml'):
        """获取配置文件中的配置，返回int"""
        file_path = ROOT + path
        config = yaml.load(open(file_path, 'r'))
        if option:
            return int(config[section][option])
        else:
            return int(config[section])
