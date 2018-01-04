# -*- coding: UTF-8 -*-
"""
Created on 2017年12月17日
@author: Leo
"""

# 系统库
import logging


# 日志中心
class Logger:
    def __init__(
            self,
            logger,
            log_path="./analyse.log",
            file_log_level="DEBUG",
            console_log_level="DEBUG"):

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(filename=log_path, mode='a', encoding="UTF-8")
        fh.setLevel(file_log_level)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(console_log_level)

        # 定义handler的输出格式
        log_format = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        # 定义handler的输出格式
        fh.setFormatter(log_format)
        ch.setFormatter(log_format)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        """
        返回一个日志对象
        :return: 返回一个日志对象
        """
        return self.logger
