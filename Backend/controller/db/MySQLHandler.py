# -*- coding: UTF-8 -*-
"""
Created on 2017年12月17日
@author: Leo
"""

# 系统库
import json

# 第三方库
import pymysql

# 项目内部库
from Backend.controller.logger.LoggerHandler import Logger

# 日志中心
logger = Logger(logger='MySQLHandler.py').get_logger()


# 错误字典
CODE_dict = {1045: "数据库用户名或者密码错误.",
             1049: "找不到当前数据库.",
             2003: "超时无法连接到数据库,数据库地址或端口错误"}

# SQL配置文件路径
SQL_CONFIG_PATH = "./controller/conf_file/db.json"


# 数据源
class DataSource:
    def __init__(
            self,
            host="127.0.0.1",
            port=3306,
            user="",
            password="",
            db="",
            charset="utf8",
            connect_timeout=2,
            json_config=False):

        # 如果json_config 为False需要检查参数
        if json_config is False and (user == "" or password == "" or db == ""):
            logger.debug("用户名密码或数据库名称不正确,请重试!")
            return

        # 如果json_config 为True则不用看参数是多少了
        if json_config:
            config = self._load_config_from_json()
            host = config['host']
            port = config['port']
            user = config['user']
            password = config['password']
            db = config['database']
            logger.debug(
                "用户名:%s\t数据库名称:%s\t\t数据库地址:%s\t数据库端口:%s" %
                (user, db, host, port))

        try:
            # 数据库连接
            self.conn = pymysql.Connect(host=host,
                                        port=port,
                                        user=user,
                                        password=password,
                                        database=db,
                                        charset=charset,
                                        connect_timeout=connect_timeout)
            logger.debug("连接数据库成功!")
        except Exception as err:
            # 数据库连接报错处理
            self._db_connect_error_handler(msg=tuple(eval(str(err))))

    @staticmethod
    def _db_connect_error_handler(msg):
        """
        数据库连接报错处理
        :param msg: 错误信息
        :return: 无返回值
        """
        if isinstance(msg[0], int):
            try:
                logger.debug(msg=CODE_dict[msg[0]] + "\t" + "详情: %s" % msg[1])
            except KeyError:
                logger.debug(msg=msg[1])

    @staticmethod
    def _load_config_from_json() -> dict:
        """
        从json读取MySQL配置信息
        :return:
        """
        try:
            db_config = json.loads(
                open(SQL_CONFIG_PATH,
                     encoding="UTF-8").read())['mysql']
        except FileNotFoundError:
            db_config = json.loads(
                open("." + SQL_CONFIG_PATH,
                     encoding="UTF-8").read())['mysql']
        # 这样输出比较好看
        # print(json.dumps(db_config, indent=4))
        return db_config
