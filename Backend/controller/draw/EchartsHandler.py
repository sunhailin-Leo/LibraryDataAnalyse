# -*- coding: UTF-8 -*-
"""
Created on 2017年12月17日
@author: Leo
"""

# 系统库
import re

# 第三方库
import pandas as pd
from pyecharts import Bar, Pie, WordCloud, Page, Style

# 项目内部库
from Backend.controller.logger.LoggerHandler import Logger

# # 日志中心
logger = Logger(logger='EchartsHandler.py').get_logger()

# Echart图(HTML)导出路径
Echart_Output_Path = "./controller/output/"


class DrawByEcharts:
    def __init__(self, is_json_mode: bool):
        """
        :param is_json_mode: 是否开启JSON模式
        当json_mode为True时则不会生成本地文件.
        """
        self._json_mode = is_json_mode

        # Style样式对象
        self.style = Style(width=1440, height=900)

    def draw_reader_count(self, data_list: list):
        """
        画图书馆借阅人数分布图
        :param data_list:
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        attr = ['广商学生', '职院学生', '教职工']

        # 画图
        title = "图书馆借阅人群统计图"
        chart = Bar(title, **self.style.init_style)
        chart.add(attr, attr, data_list, is_more_utils=True)

        if self._json_mode:
            return chart.options
        else:
            self._public_page_render(chart=chart, filename=title)

    def draw_top_15_book(
            self,
            borrow_count_15: pd.DataFrame,
            title: str,
            bar_title=None,
            bar_subtitle=None):
        """
        学生借书榜的前15本
        :param bar_subtitle:副标题
        :param bar_title: 标题
        :param borrow_count_15: Dataframe
        :param title: 页面标题和文件名
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        if bar_title is not None:
            assert isinstance(bar_title, str)
        if bar_subtitle is not None:
            assert isinstance(bar_subtitle, str)

        attr = borrow_count_15['BookName'].tolist()
        v1 = borrow_count_15['Count'].tolist()
        chart = Bar(title=bar_title,
                    subtitle=bar_subtitle,
                    **self.style.init_style)

        chart.add("", attr, v1,
                  is_datazoom_show=True,
                  datazoom_type='both',
                  is_more_utils=True,
                  datazoom_range=[0, 65],
                  mark_line=["average"],
                  is_label_show=True,
                  label_formatter='{b}-{c}',
                  label_pos='top',
                  label_color=['#B0E2FF'])

        if self._json_mode:
            return chart.options
        else:
            self._public_page_render(chart=chart,
                                     filename=title,
                                     page_title=title)

    def draw_dif_grade_stu(self, group_by_grade: pd.DataFrame):
        """
        各年级借阅人数统计图(含广商和职院学生)
        :param group_by_grade: 数据
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        group_by_grade['Grade'] = [
            re.findall(
                r'\d+',
                x.replace(
                    "123",
                    ""))[0] for x in group_by_grade['Department'].tolist()]
        group_result = group_by_grade.groupby(['Grade'])
        grade = []
        people = []
        for i in group_result:
            grade.append(i[0] + "级")
            people.append(len(i[1]))

        if self._json_mode:
            return self.draw_pie_chart(title="各年级借阅人数统计图(含广商和职院学生)",
                                       x_list=grade,
                                       y_list=people)
        else:
            return self.draw_pie_chart(title="各年级借阅人数统计图(含广商和职院学生)",
                                       x_list=grade,
                                       y_list=people)

    def draw_dif_faculty_borrow_info(
            self,
            data: pd.DataFrame,
            title: str,
            df_category_name="Department"):
        """
        # 统计广商各学院借书记录或康大各系
        :param df_category_name: 默认Department, 另外一个是Faculty
        :param data: 学生数据
        :param title: 标题
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        if df_category_name not in ['Department', 'Faculty']:
            raise ValueError("You give wrong key")
        x = []
        y = []
        for i in data.groupby([df_category_name]):
            x.append(i[0])
            y.append(len(i[1]))

        if self._json_mode:
            return self.draw_pie_chart(title=title, x_list=x, y_list=y)
        else:
            self.draw_pie_chart(title=title, x_list=x, y_list=y)

    def draw_publisher_author_word_cloud(self, publisher: list, author: list):
        """
        画出版社和作者的词云
        :param publisher:
        :param author:
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        if len(publisher) < 1:
            logger.error("No Data!")
            raise ValueError("Publisher list is empty!")
        elif len(author) < 1:
            logger.error("No Data!")
            raise ValueError("Author list is empty!")

        name = ['热门出版社', '热门作者']

        # 画图
        page = Page()
        chart = WordCloud(name[0], **self.style.init_style)
        chart.add("", publisher[0], publisher[1], word_size_range=[12, 80], shape="cardioid")
        page.add(chart)

        chart_1 = WordCloud(name[1], **self.style.init_style)
        chart_1.add("", author[0], author[1], word_size_range=[12, 80], shape="pentagon")
        page.add(chart_1)

        if self._json_mode:
            chart_json = [chart.options, chart_1.options]
            return chart_json
        else:
            logger.debug("正在导出: " + Echart_Output_Path + "&".join(name) + ".html")
            page.render(Echart_Output_Path + "&".join(name) + ".html")

    def draw_book_price_chart(self, stage_list: list):
        """
        图书价格分布图
        :param stage_list: 各分段数据
        :return:
        """
        page = Page()
        x = ["0~20", "20~40", "40~60", "60~80", "80~100", "100~"]
        bar_chart = Bar("图书价格分布(柱状图)", **self.style.init_style)
        bar_chart.add("", x, stage_list, is_more_utils=True, is_label_show=True)
        page.add(bar_chart)

        pie_chart = Pie("图书价格分布(饼图)", **self.style.init_style)
        pie_chart.add("", x, stage_list,
                      is_label_show=True,
                      legend_orient='vertical',
                      legend_pos='left',
                      legend_top="center")
        page.add(pie_chart)

        if self._json_mode:
            chart_json = [bar_chart.options, pie_chart.options]
            return chart_json
        else:
            logger.debug("正在导出: " + Echart_Output_Path + "图书价格分布图" + ".html")
            page.render(Echart_Output_Path + "图书价格分布图" + ".html")

    ##########################################################################
    def draw_pie_chart(self, title: str, x_list: list, y_list: list):
        """
        饼图公共方法
        :param title: 标题
        :param x_list: x轴(类别)
        :param y_list: y轴(人数)
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        chart = Pie(title, title_pos='center', **self.style.init_style)
        chart.add("", x_list, y_list,
                  label_text_size=16,
                  is_label_show=True,
                  legend_orient='vertical',
                  legend_pos='left',
                  is_more_utils=True)

        if self._json_mode:
            return chart.options
        else:
            self._public_page_render(chart=chart, filename=title)

    def draw_bar_chart(self, title: str, x_list: list, y_list: list, name=None):
        """
        柱状图公共方法
        :param title: 标题
        :param x_list: x轴(类别)
        :param y_list: y轴(人数)
        :param name: 堆叠时的名称
        :return: 无返回值(如果self._json_mode为True则有返回值)
        """
        chart = Bar(title, **self.style.init_style)
        if len(y_list) > 1:
            for i in range(len(y_list)):
                chart.add(name[i], x_list, y_list[i], is_more_utils=True)
        else:
            chart.add("", x_list, y_list)

        if self._json_mode:
            return chart.options
        else:
            self._public_page_render(chart=chart, filename=title)

    ##########################################################################
    @staticmethod
    def _public_page_render(chart, filename: str, page_title="Echarts"):
        """
        公共的画图渲染界面的方法
        :param chart: 画图对象
        :param filename: 文件名(标题名)
        :return:
        """
        page = Page(page_title=page_title)
        page.add(chart)
        logger.debug("正在导出: " + Echart_Output_Path + filename + ".html")
        page.render(Echart_Output_Path + filename + ".html")
