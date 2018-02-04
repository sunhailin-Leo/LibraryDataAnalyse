# -*- coding: UTF-8 -*-
"""
Created on 2017年12月29日
@author: Leo
"""


# 第三方库
from flask import jsonify
from flask_restful import Resource

# 项目内部库
from Backend.controller import analyse

charts = analyse.LibraryBorrow(is_json_mode=True)


class GzccTop15(Resource):
    def get(self):
        res = charts.draw_gzcc_stu_top_15()
        return jsonify(res)


class KdTop15(Resource):
    def get(self):
        res = charts.draw_kd_stu_top_15()
        return jsonify(res)


class LibraryBorrowPeopleType(Resource):
    def get(self):
        res = charts.draw_library_borrow_people_type()
        return jsonify(res)


class Grade(Resource):
    def get(self):
        res = charts.draw_dif_grade()
        return jsonify(res)


class Sex(Resource):
    def get(self):
        res = charts.draw_dif_sex()
        return jsonify(res)


class SexDuplicate(Resource):
    def get(self):
        res = charts.draw_dif_sex(not_duplicates=False)
        return jsonify(res)


class GzccFaculty(Resource):
    def get(self):
        res = charts.draw_dif_faculty(data_source="gzcc")
        return jsonify(res)


class KdFaculty(Resource):
    def get(self):
        res = charts.draw_dif_faculty(data_source="kd")
        return jsonify(res)


class BorrowReturnMonths(Resource):
    def get(self):
        res = charts.draw_dif_gzcc_borrow_return_month()
        return jsonify(res)


class BorrowReturnWeekdays(Resource):
    def get(self):
        res = charts.draw_dif_gzcc_borrow_return_weekdays()
        return jsonify(res)


class BorrowReturnQuantum(Resource):
    def get(self):
        res = charts.draw_dif_gzcc_borrow_return_time_quantum()
        return jsonify(res)


class DifFloorBorrow(Resource):
    def get(self):
        res = charts.draw_dif_gzcc_stu_dif_floor_borrow_info()
        return jsonify(res)


class PublishAuthor(Resource):
    def get(self):
        res = charts.draw_dif_gzcc_book_publish_author()
        return jsonify(res)


class FacultySexBorrowInfo(Resource):
    def get(self):
        res = charts.draw_gzcc_faculty_sex_borrow_info()
        return jsonify(res)