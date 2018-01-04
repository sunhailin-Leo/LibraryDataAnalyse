# -*- coding: UTF-8 -*-
"""
Created on 2017年12月1日
@author: Leo
"""

# 第三方库
from flask import Flask, Blueprint
from flask_restful import Api

# 项目内部库
from Backend.bankend_controller.resources.generate_charts import *


class Backend:
    def __init__(self, mode="dev"):
        # 项目启动模式
        self._mode = mode

        # 项目版本前缀
        self._version_prefix = "/v1"

        # 项目初始化
        self._app = Flask(__name__)
        self._api_bp = Blueprint('api', __name__)
        self._api = Api(self._api_bp)

    @staticmethod
    def _load_config() -> dict:
        """
        加载配置文件(暂时不启用)
        :return: json
        """
        pass

    def _register_router(self):
        """
        注册路由
        """
        # 只返回人数（接口只返回人数不返回画图的JSON） ok
        self._api.add_resource(LibraryBorrowPeopleType, self._version_prefix + "/charts/dif_people")

        self._api.add_resource(GzccTop15, self._version_prefix + "/charts/gzcc_top")
        self._api.add_resource(KdTop15, self._version_prefix + "/charts/kd_top")
        self._api.add_resource(Grade, self._version_prefix + "/charts/grade")
        self._api.add_resource(Sex, self._version_prefix + "/charts/sex")
        self._api.add_resource(SexDuplicate, self._version_prefix + "/charts/sex_1")
        self._api.add_resource(GzccFaculty, self._version_prefix + "/charts/gzcc_faculty")
        self._api.add_resource(KdFaculty, self._version_prefix + "/charts/kd_faculty")
        self._api.add_resource(BorrowReturnMonths, self._version_prefix + "/charts/br_months")
        self._api.add_resource(BorrowReturnWeekdays, self._version_prefix + "/charts/br_weekdays")
        self._api.add_resource(BorrowReturnQuantum, self._version_prefix + "/charts/br_quantum")
        self._api.add_resource(DifFloorBorrow, self._version_prefix + "/charts/dif_floor")
        self._api.add_resource(PublishAuthor, self._version_prefix + "/charts/p_a")

        # 注册蓝图
        self._app.register_blueprint(self._api_bp)

    def start(self):
        # 注册路由
        self._register_router()
        # 启动
        self._app.run(port=10010, debug=True)


if __name__ == '__main__':
    # 初始化
    b = Backend()
    # 启动
    b.start()
