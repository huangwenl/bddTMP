# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"

import pymysql.cursors
from utils.commonTool.configUtil import ConfigUtil
from sshtunnel import SSHTunnelForwarder
from utils.commonTool.baseSqlUtil import BaseUtil

host = ConfigUtil.get("Mysql", 'Host')
port = ConfigUtil.getint("Mysql", 'Port')
user = ConfigUtil.get("Mysql", 'User')
pwd = ConfigUtil.get("Mysql", 'Passwd')
db = ConfigUtil.get("Mysql", "DB")
# db = "zentao"
sshusername = ConfigUtil.get("Mysql", "ssh_username")
sshpassword = ConfigUtil.get("Mysql", "ssh_password")
sshport = ConfigUtil.getint("Mysql", "ssh_port")


def connect():
    server = SSHTunnelForwarder(
        ssh_address_or_host=(host, sshport),  # 指定ssh登录的跳转机的address
        ssh_username=sshusername,  # 跳转机的用户
        ssh_password=sshpassword,  # 跳转机的密码
        remote_bind_address=('127.0.0.1', port))
    server.start()
    config = {
        'host': "127.0.0.1",
        'port': server.local_bind_port,
        'user': user,
        'password': pwd,
        'db': db,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    client = pymysql.Connect(**config)
    return client, server


class MysqlUtil(BaseUtil):
    def __init__(self):
        connection = connect()[0]
        super(MysqlUtil, self).__init__(connection)
        self.server = connect()[1]
        self.cursor = self.connection.cursor()

    def executeQuery(self, sql, params=()):
        try:
            data = []
            self.cursor.execute(sql, params)
            data = self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            # self.close()
            return data

    def executeNonQuery(self, sql, params=()):
        try:
            result = 0
            result = self.cursor.execute(sql, params)
            self.connection.commit()
            # res = self.cursor._cursor.rowcount
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(e)
        finally:
            if result:
                lastid = self.cursor.lastrowid
                if lastid:
                    result = lastid
            return result


# mysql = MysqlUtil()
# sql_Str = "select * from zt_bug"
# data = mysql.executeQuery(sql=sql_Str)
# for i in data:
#     print(i)
# mysql.close()
