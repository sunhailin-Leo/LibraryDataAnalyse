# -*- coding: UTF-8 -*-
"""
Created on 2017年12月17日
@author: Leo
"""

# 系统库
import re
import sys
import json
import traceback

# 第三方库
import pandas as pd
import pandas.io.sql as pd_sql

# 项目内部库
from Backend.controller.db.MySQLHandler import DataSource
from Backend.controller.draw.EchartsHandler import DrawByEcharts
from Backend.controller.logger.LoggerHandler import Logger
from Backend.controller.util.time_util import TimeUtil


# 日志中心
logger = Logger(logger='analyse.py').get_logger()

# SQL语句json
SQL_JSON = ".././controller/conf_file/sql.json"

# Echart图(HTML)导出路径
Echart_Output_Path = "./output/"

# 数据类型字典
DATA_TYPE = {
    "gzcc": "gzcc_student_sql",
    "kd": "kd_student_sql",
    "teacher": "teacher_sql",
    "gzcc_time": "gzcc_time"
}


class LibraryBorrow:
    def __init__(self, is_json_mode=False, time_mode=False):
        """
        :param is_json_mode: 是否开启JSON模式(传递到画图层的参数)
        当json_mode为True时则不会生成本地文件.
        """
        # 数据库连接对象
        try:
            self._db = DataSource(json_config=True)
            self._conn = self._db.conn
        except AttributeError:
            logger.debug("数据库加载失败")
            self.error_handler()

        # 加载sql文件
        try:
            self._json_sql = json.loads(
                open(SQL_JSON, encoding="UTF-8").read())
        except FileNotFoundError:
            self.error_handler()

        # 判断模式
        self._json_mode = is_json_mode

        # 是否加载时间列
        self.load_time_col = time_mode

        # 初始化画图层
        self.draw = DrawByEcharts(is_json_mode=self._json_mode)

        # 学生数据变量
        self.gzcc = self._load_data(data_type="gzcc")
        self.kd = self._load_data(data_type="kd")
        self.all_student = None
        self.gzcc_with_time = self._load_data(data_type="gzcc_time")

        # 时间工具库
        self._t = TimeUtil()

    def error_handler(self):
        """
        错误处理逻辑,改写错误展现形式
        :return: 返回一个dict(json)
        """
        # 捕获的错误列表
        error_list = traceback.format_exception(*sys.exc_info())
        # 处理错误信息
        error_position = re.sub(
            pattern=r'\s+', repl="", string=error_list[1:][0]).split(",")[:2]
        if self._json_mode is not True:
            logger.debug("错误信息:(如下)\n\t路径: %s\t位置: %s\n\t原因: %s" %
                         (error_position[0].replace("File", ""),
                          error_position[1].replace("line", "第") + "行",
                          error_list[-1]))
            sys.exit(1)
        else:
            error_json = {"路径": error_position[0].replace("File", ""),
                          "位置": error_position[1].replace("line", "第") + "行",
                          "原因": error_list[-1]}
            logger.debug(error_json)
            # sys.exit(1)

    def _mysql_to_pandas(self, json_key=None, sql=None) -> pd.DataFrame:
        """
        mysql数据通过sql语句转换成DataFrame
        :param json_key: json的key值
        :param sql: 自定义sql语句,不通过配置文件维护
        :return: DataFrame
        """
        try:
            if sql is not None and json_key is None and isinstance(sql, str):
                return pd.read_sql_query(sql=sql, con=self._conn)
            elif sql is None and json_key is not None:
                sql_dialects = self._json_sql[json_key]
                return pd.read_sql_query(sql=sql_dialects, con=self._conn)
            else:
                raise ValueError("Please give right arguments!")
        except KeyError:
            self.error_handler()
        except pd_sql.DatabaseError:
            self.error_handler()

    @staticmethod
    def _keep_zh(data) -> str:
        """
        # 去除单位中的数字(对应数据中的年级或者其他)
        :param data: dataframe
        :return:
        """
        p_res = re.sub(pattern=r'\w*', flags=re.L, repl="", string=data)
        return p_res

    def _load_data(self, data_type: str) -> pd.DataFrame:
        """
        数据类型(广商康大教师)
        :param data_type: 学生类型(广商康大教师)
        :return:
        """
        if data_type not in list(DATA_TYPE.keys()):
            raise ValueError("You give wrong type!")
        else:
            df = self._mysql_to_pandas(json_key=DATA_TYPE[data_type])
            df['Type'] = [data_type] * len(df)
            return df

    def _get_all_student(self):
        """
        合并广商学生和康大学生数据并处理列名
        :return: 无返回值
        """
        if self.gzcc is None or self.kd is None:
            raise ValueError(
                "You need call function get_student_data before call this function!")
        else:
            all_stu_df = pd.DataFrame(pd.concat([self.gzcc, self.kd]))
            self.all_student = all_stu_df.rename(
                columns={'单位': 'Department', '题名': 'BookName'})

    def _gzcc_student(self):
        """
        # 广商数据分析
        :return: 无返回值
        """
        gzcc = self.gzcc.rename(columns={'单位': 'Department', '题名': 'BookName'})
        gzcc['Department'] = [self._keep_zh(x)
                              for x in gzcc['Department'].tolist()]
        gzcc.insert(
            1, "Faculty", [
                re.search(
                    r'(.*学院)(.*)', x).groups()[0] for x in gzcc['Department']])
        gzcc.insert(
            2, "Major", [
                re.search(
                    r'(.*学院)(.*)', x).groups()[1] for x in gzcc['Department']])
        gzcc['Faculty'] = [x.replace("国际学院国际学院", "国际学院")
                           for x in gzcc['Faculty']]
        del gzcc['Department']
        return gzcc

    def _kd_student(self):
        """
        职院学生数据分析
        :return: 返回处理数据结果
        """
        kd = self.kd.rename(columns={'单位': 'Department', '题名': 'BookName'})
        kd['Department'] = [
            self._keep_zh(x).replace(
                "职院", "")[
                0:3] for x in kd['Department'].tolist()]
        return kd

    # 分析画图模块(学生)
    ##########################################################################
    def draw_gzcc_stu_top_15(self):
        """
        广商借书的主要题名
        去掉影响数据分布的廉洁修身这本书
        并统计借阅次数前十五的书籍
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        gzcc = self._gzcc_student()
        gzcc['Count'] = [1] * len(gzcc)
        result = gzcc.groupby(['BookName'])
        sum_result = result.sum().sort_values(
            by="Count", ascending=False).reset_index()
        sum_result = sum_result[sum_result['BookName'] != "廉洁修身:大学版.2016"]
        borrow_count_15 = sum_result[:15]
        if self._json_mode:
            return self.draw.draw_top_15_book(
                borrow_count_15=borrow_count_15,
                title="广商学生热门借书榜",
                bar_title="广商学生主要借书类别(可缩放)",
                bar_subtitle="数据截止2016年底(除去廉洁修身借阅记录)")
        else:
            self.draw.draw_top_15_book(
                borrow_count_15=borrow_count_15,
                title="广商学生热门借书榜",
                bar_title="广商学生主要借书类别(可缩放)",
                bar_subtitle="数据截止2016年底(除去廉洁修身借阅记录)")

    def draw_kd_stu_top_15(self):
        """
        # 职院学生借书的主要题名前十五
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        # 职院学生数据
        kd = self._kd_student()
        kd['Count'] = [1] * len(kd)
        result = kd.groupby(['BookName'])
        sum_result = result.sum().sort_values(
            by="Count", ascending=False).reset_index()
        borrow_count_15 = sum_result[:15]

        if self._json_mode:
            return self.draw.draw_top_15_book(
                borrow_count_15=borrow_count_15,
                title="职院学生热门借书榜",
                bar_title="职院学生热门借书榜")
        else:
            self.draw.draw_top_15_book(
                borrow_count_15=borrow_count_15,
                title="职院学生热门借书榜",
                bar_title="职院学生热门借书榜")

    def draw_library_borrow_people_type(self):
        """
        画图书馆借阅人类型分布图
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        if self.gzcc is None or self.kd is None:
            raise ValueError(
                "You need call function get_student_data before call this function!")
        else:
            if self._json_mode:
                try:
                    return [len(self.gzcc), len(self.kd), len(self._mysql_to_pandas(json_key="teacher_sql"))]
                except TypeError:
                    # 尝试解决一个bug
                    self._conn = DataSource(json_config=True).conn
                    return [len(self.gzcc), len(self.kd), len(self._mysql_to_pandas(json_key="teacher_sql"))]
            else:
                self.draw.draw_reader_count(
                    data_list=[
                        len(self.gzcc), len(self.kd), len(
                            self._mysql_to_pandas(
                                json_key="teacher_sql"))])

    def draw_dif_grade(self):
        """
        划分年级并画图
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        if self.all_student is None:
            self._get_all_student()

        if self._json_mode:
            return self.draw.draw_dif_grade_stu(
                group_by_grade=self.all_student)
        else:
            self.draw.draw_dif_grade_stu(group_by_grade=self.all_student)

    def draw_dif_sex(self, not_duplicates=True):
        """
        划分性别并画图(广商学生[职院学生暂无数据])
        :return: 无返回值
        """
        # 有敏感信息
        group_stu_id = pd.read_csv("C:\\Users\\s\\Desktop\\广商借书结果.csv")
        title = "广商学生借书男女比例(累计借书数据)"
        if not_duplicates:
            title = "广商学生借书男女比例(不重复)"
            group_stu_id = group_stu_id.drop_duplicates(['学号'])
        group_stu_id = group_stu_id[['学号', '性别']]
        group_stu_id['性别'] = [
            '男' if i == 1 else '女' for i in group_stu_id['性别']]
        sex_group = group_stu_id.groupby(['性别']).count()
        x_list = list(sex_group.index)
        y_list = sex_group['学号'].tolist()
        if self._json_mode:
            return self.draw.draw_pie_chart(
                title=title, x_list=x_list, y_list=y_list)
        else:
            self.draw.draw_pie_chart(
                title=title, x_list=x_list, y_list=y_list)

    def draw_dif_faculty(self, data_source: str):
        """
        划分不同学院(广商和康大的)
        :param data_source:
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        source = ['gzcc', 'kd']
        if data_source not in source:
            raise ValueError("Please give the right source.")
        else:
            if data_source == "gzcc":
                data = self._gzcc_student()
                title = "各学院借阅人数统计图(广商学生)"
                category_name = "Faculty"
                if self._json_mode:
                    return self.draw.draw_dif_faculty_borrow_info(
                        data=data,
                        title=title,
                        df_category_name=category_name)
                else:
                    self.draw.draw_dif_faculty_borrow_info(
                        data=data,
                        title=title,
                        df_category_name=category_name)
            elif data_source == "kd":
                data = self._kd_student()
                title = "各系借阅人数统计图(职院学生)"
                if self._json_mode:
                    return self.draw.draw_dif_faculty_borrow_info(
                        data=data,
                        title=title)
                else:
                    self.draw.draw_dif_faculty_borrow_info(
                        data=data,
                        title=title)

    def draw_dif_gzcc_borrow_return_month(self):
        """
        画不同时间(月份)借书的人比例
        :return:
        """
        group_months_result_borrow = self.gzcc_with_time.groupby(['借书日期(月份)']).count()[
            '证件号']
        group_months_result_return = self.gzcc_with_time.groupby(['还书日期(月份)']).count()[
            '证件号']
        x = list(group_months_result_borrow.index)
        y = [
            group_months_result_borrow.tolist(),
            group_months_result_return.tolist()]
        name = ['借书', '还书']
        if self._json_mode:
            return self.draw.draw_bar_chart(
                title="每月借还书人数比例", x_list=x, y_list=y, name=name)
        else:
            self.draw.draw_bar_chart(
                title="每月借还书人数比例", x_list=x, y_list=y, name=name)

    def draw_dif_gzcc_borrow_return_weekdays(self):
        """
        画不同时间(周数)借还书的人比例
        :return:
        """
        week_range = [1, 3, 2, 5, 6, 4, 7]
        group_weekdays_result_borrow = self.gzcc_with_time.groupby(['借书日期(周数)']).count()[
            '证件号'].reset_index()
        group_weekdays_result_borrow['rank'] = week_range
        group_weekdays_result_borrow = group_weekdays_result_borrow.sort_values(['rank'])

        group_weekdays_result_return = self.gzcc_with_time.groupby(['还书日期(周数)']).count()[
            '证件号'].reset_index()
        group_weekdays_result_return['rank'] = week_range
        group_weekdays_result_return = group_weekdays_result_return.sort_values(['rank'])

        x = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        y = [
            group_weekdays_result_borrow['证件号'].tolist(),
            group_weekdays_result_return['证件号'].tolist()]
        name = ['借书', '还书']
        if self._json_mode:
            return self.draw.draw_bar_chart(
                title="周一至周日借还书人数比例", x_list=x, y_list=y, name=name)
        else:
            self.draw.draw_bar_chart(
                title="周一至周日借还书人数比例", x_list=x, y_list=y, name=name)

    def draw_dif_gzcc_borrow_return_time_quantum(self):
        """
        画不同时间(上午、下午、晚上)借书的人比例
        :return:
        """
        group_quantum_result_borrow = self.gzcc_with_time.groupby(
            ['借书日期(时间段)']).count()['证件号']
        group_quantum_result_return = self.gzcc_with_time.groupby(
            ['还书日期(时间段)']).count()['证件号'].reset_index()
        group_quantum_result_return = group_quantum_result_return[
            group_quantum_result_return['还书日期(时间段)'] != "半夜"]['证件号']
        x = list(group_quantum_result_borrow.index)
        y = [group_quantum_result_borrow.tolist(), group_quantum_result_return.tolist()]
        name = ['借书', '还书']
        if self._json_mode:
            return self.draw.draw_bar_chart(
                title="早中晚借还书人数比例", x_list=x, y_list=y, name=name)
        else:
            self.draw.draw_bar_chart(
                title="早中晚借还书人数比例", x_list=x, y_list=y, name=name)

    def draw_dif_gzcc_stu_dif_floor_borrow_info(self):
        """
        统计图书馆各层借阅情况
        :return:
        """
        dif_floor_info = self._mysql_to_pandas(
            sql="SELECT 单位, 题名, 索书号, 馆藏地 FROM jieyue "
                "WHERE LENGTH(证件号) = 12 AND 单位 != '100' AND 单位 NOT LIKE '职院%';")
        dif_floor_info['馆藏地'] = [
            x.replace(
                "_x000d_\n",
                "") for x in dif_floor_info['馆藏地']]
        group_floor_info = dif_floor_info.groupby(['馆藏地']).count()['题名']
        x = list(group_floor_info.index)
        y = group_floor_info.tolist()
        if self._json_mode:
            return self.draw.draw_pie_chart(
                title="统计图书馆各层借阅情况", x_list=x, y_list=y)
        else:
            self.draw.draw_pie_chart(title="统计图书馆各层借阅情况", x_list=x, y_list=y)

    def draw_dif_gzcc_book_publish_author(self):
        """
        统计出版社和作者的热门词云
        :return:
        """
        publish_author = self._mysql_to_pandas(
            sql="SELECT 题名, 作者, 出版社 FROM jieyue WHERE "
                "LENGTH(证件号) = 12 AND 单位 != '100' AND 单位 NOT LIKE '职院%';")
        # 过滤异常借书
        publish_author = publish_author[publish_author['题名']
                                        != "廉洁修身:大学版.2016"]
        group_publish = publish_author.groupby(
            ['出版社']).count()['题名'].reset_index().sort_values(
            by="题名", ascending=False)[:100]
        group_author = publish_author.groupby(
            ['作者']).count()['题名'].reset_index().sort_values(
            by="题名", ascending=False)[:100]

        if self._json_mode:
            return self.draw.draw_publisher_author_word_cloud(
                publisher=[
                    group_publish['出版社'], group_publish['题名']], author=[
                    group_author['作者'].tolist(), group_author['题名'].tolist()])
        else:
            self.draw.draw_publisher_author_word_cloud(
                publisher=[
                    group_publish['出版社'], group_publish['题名']], author=[
                    group_author['作者'].tolist(), group_author['题名'].tolist()])

    def draw_library_book_price(self):
        """
        统计图书馆价格区间
        :return:
        """
        book_price = self._mysql_to_pandas(
            sql="SELECT 题名, 价格 FROM jieyue").drop_duplicates(
            ['题名'])
        book_price['价格'] = book_price['价格'].astype(float)

        # 价格有问题,两端有异常值
        book_price = book_price[book_price['价格'] > float(0.0)]

        # print(book_price.describe())

        # 分段
        price_0_20 = book_price[(book_price['价格'] >= float(0)) & (
            book_price['价格'] < float(20))]
        price_20_40 = book_price[(book_price['价格'] >= float(20)) & (
            book_price['价格'] < float(40))]
        price_40_60 = book_price[(book_price['价格'] >= float(40)) & (
            book_price['价格'] < float(60))]
        price_60_80 = book_price[(book_price['价格'] >= float(60)) & (
            book_price['价格'] < float(80))]
        price_80_100 = book_price[(book_price['价格'] >= float(80)) & (
            book_price['价格'] < float(100))]
        price_100_max = book_price[(book_price['价格'] >= float(100))]

        if self._json_mode:
            return self.draw.draw_book_price_chart(
                stage_list=[
                    len(price_0_20),
                    len(price_20_40),
                    len(price_40_60),
                    len(price_60_80),
                    len(price_80_100),
                    len(price_100_max)])
        else:
            self.draw.draw_book_price_chart(
                stage_list=[
                    len(price_0_20),
                    len(price_20_40),
                    len(price_40_60),
                    len(price_60_80),
                    len(price_80_100),
                    len(price_100_max)])

    def draw_gzcc_stu_borrow_info(self):
        """
        学生借书情况一览
        :return:
        """
        stu_info = self._mysql_to_pandas(
            sql="SELECT t1.*, t2.t_sex FROM jieyue_2 AS t1, total AS t2 WHERE t1.证件号 = t2.t_stu_id;")

        def filter_faculty(data: pd.DataFrame) -> pd.DataFrame():
            data['单位'] = [self._keep_zh(x) for x in data['单位'].tolist()]
            data.insert(1, "Faculty", [re.search('(.*学院)(.*)', x).groups()[0] for x in data['单位']])
            data.insert(2, "Major", [re.search(r'(.*学院)(.*)', x).groups()[1] for x in data['单位']])
            data['Faculty'] = [x.replace("国际学院国际学院", "国际学院") for x in data['Faculty']]
            return data

        stu_info = filter_faculty(stu_info)
        group_sex = list(stu_info.groupby(['t_sex']))
        male = group_sex[0][1]
        male_group = male.groupby(['Faculty']).count()
        male_list = male_group['姓名'].tolist()
        index = list(male_group.index)

        female = group_sex[1][1]
        female_group = female.groupby(['Faculty']).count()
        female_list = female_group['姓名'].tolist()

        df = pd.DataFrame([male_list, female_list], index=["Male", "Female"]).T
        df['MalePercent'] = df['Male'] / (df['Male'] + df['Female'])
        df['FemalePercent'] = df['Female'] / (df['Male'] + df['Female'])
        df['Faculty'] = index
        print(df)

        """
        gzcc['Department'] = [self._keep_zh(x)
                              for x in gzcc['Department'].tolist()]
        gzcc.insert(
            1, "Faculty", [
                re.search(
                    r'(.*学院)(.*)', x).groups()[0] for x in gzcc['Department']])
        gzcc.insert(
            2, "Major", [
                re.search(
                    r'(.*学院)(.*)', x).groups()[1] for x in gzcc['Department']])
        gzcc['Faculty'] = [x.replace("国际学院国际学院", "国际学院")
                           for x in gzcc['Faculty']]
        """
        # female = group_sex[1][1]
        # print(female)

    ##########################################################################
    def get_teacher_data(self):
        """
        获取教师数据
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        teacher_df = self._load_data(data_type="teacher")
        print(teacher_df)


if __name__ == '__main__':
    lib = LibraryBorrow(is_json_mode=False, time_mode=True)
    # 学生
    # lib.draw_gzcc_stu_top_15()
    # lib.draw_kd_stu_top_15()
    # lib.draw_library_borrow_people_type()
    # lib.draw_dif_grade()
    # lib.draw_dif_sex()
    # lib.draw_dif_sex(not_duplicates=False)
    # lib.draw_dif_faculty(data_source="gzcc")
    # lib.draw_dif_faculty(data_source="kd")
    # lib.draw_dif_gzcc_borrow_return_month()
    # lib.draw_dif_gzcc_borrow_return_weekdays()
    # lib.draw_dif_gzcc_borrow_return_time_quantum()
    # lib.draw_dif_gzcc_stu_dif_floor_borrow_info()
    # lib.draw_dif_gzcc_book_publish_author()

    # lib.draw_library_book_price()
    lib.draw_gzcc_stu_borrow_info()

    # 教师
    # lib.get_teacher_data()
