#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'lihongcheng'
# @Time: 2019/08/20

# import pymssql
# from pymssql import OperationalError, InterfaceError
import pyodbc
from .config import CONFIG_FILE, Config
import platform

conf = Config(CONFIG_FILE)


class DBConnect:
    """
    connect DB
    """
    def __init__(self):
        os_name = platform.system()
        # 可以链接yaml文件中指定的数据库
        if os_name == 'Windows':
            self.DB_config = conf.get('data5_dev')
        elif os_name == 'Linux':
            self.DB_config = conf.get('data5_port')

        self.driver = self.DB_config.get('driver')
        self.server = self.DB_config.get('server')
        self.user = self.DB_config.get('user')
        self.password = self.DB_config.get('password')
        self.database = self.DB_config.get('database')

        self.conn = pyodbc.connect(driver=self.driver, server=self.server, user=self.user, password=self.password, database=self.database, charset='utf8')
        self.cur = self.conn.cursor()