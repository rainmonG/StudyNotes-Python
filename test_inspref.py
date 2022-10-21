#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2022/10/10 17:03
# @Author : wanjian
# @Version：V 0.1
# @File : insp_script_customer.py
# @desc :

import pandas as pd
from oe_script.commen.utils.db_handler.mysql_handler import DbHelper
from oe_script.commen.utils.db_handler.elasticsearch_handler import ESBaseHandler
import json
from functools import reduce
import datetime
from operator import add

# TODO 待完善逻辑
class AlarmBaseHandler:
    def __init__(self, date=None):
        self.db_handler = DbHelper().get_mysql_handler('oedata_online')
        self.es_handler = ESBaseHandler('inspection_customer')
        self.keywords = ["本次巡检值", "上一次巡检值", "第一次巡检值", "出厂值", "最大值", "最小值"]
        self.logic_relation = {"且": "&", "或": "|"}
        self.historical_keywords = self.keywords[1:]
        if date is None:
            self.date = datetime.date.today().strftime("%Y-%m-%d")
        else:
            self.date = date
        self.barcode = self.get_all_barcode()

    def get_all_barcode(self):
        """
        获取所有客户侧需要预警的编码
        """
        sql = "select distinct barcode from table"
        df = self.db_handler.query_pd(sql)
        return df["barcode"].to_list()

    def get_insp_data_by_barcode(self, condition, fields):
        """
        按编码获取巡检数据，condition为str，则传的编码，取当日单次巡检数据，condition为list，则传的条码，取条码的历史巡检值
        """

        if type(condition) == str:
            body = {"barcode": condition}
        elif type(condition) == list:
            body = {"sn": condition}
        else:
            return pd.DataFrame()
        res = self.es_handler.search(body)
        df = pd.DataFrame(res)
        return df

    def get_warning_rules_by_barcode(self, barcode, option=None):
        """
        按编码获取上下门限、预警规则等
        """
        if option == "warning_rules":
            sql = "select warning_rule from table where barcode='{}'".format(barcode)
            df = self.db_handler.query_pd(sql)
        else:
            sql = "select pre_processing_rule, threshold_warning from table where barcode='{}'".format(barcode)
            df = self.db_handler.query_pd(sql)
        return df

    def splice_alarm_data(self, row):
        dic = row.drop("sn").to_dict()
        res = str(dic).replace("'", "").replace("{", "").replace("}", "")
        return res

    def handle_pre_processing_data(self, df, pre_processing_rule):
        """
        此方法用于从dataframe中进行预处理

        :param pd.Dataframe df:  需要筛选的dataframe
        :param dict pre_processing_rule:  筛选规则，如：{'name': '自定义', 'rules': '(ch1_receive_optical_power_report:本次巡检值≥3,或,ch2_receive_optical_power_report:本次巡检值≥3),且,ch1_receive_optical_power_report:本次巡检值≠4'}
        """
        temp_df = pd.DataFrame()
        if pre_processing_rule and not df.empty:
            code_str = "temp_df = df.loc["
            rules = pre_processing_rule["rules"].split(",")
            for rule in rules:
                if rule in ("且", "或"):
                    code_str += self.logic_relation[rule]
                else:
                    field, desc = rule.strip("()").split(":")
                    temp_str = rule.replace(field + ":本次巡检值", "df['{}']".format(field)).replace("=", "==").replace("≥", ">=").replace("≤", "<=").replace("≠", "!=")
                    code_str += ("(" + temp_str + ")")
            code_str += "]"
            try:
                exec(code_str)
            except BaseException as e:
                raise ValueError("预警程序预处理执行报错：{}".format(e))
        return temp_df

    def threshold_warning(self, df, limit_format):
        """
        limit_format = {
        "min_limit": {
            'ch1_receive_optical_power_report': 2,
            'ch1_bias_optical_power_report': 3
        },
        "max_limit": {
            'ch1_receive_optical_power_report': 0,
            'ch1_bias_optical_power_report': 0
        },
        }
        """
        df_alarm_list = []
        if limit_format["max_limit"]:
            df_over_limit_list = []
            for field, limit in limit_format["max_limit"].items():
                df_over_limit = df.loc[df[field] > limit]
                if not df_over_limit.empty:
                    df_over_limit = df_over_limit[["sn", field]]
                    df_over_limit.columns = ["sn", "alarm_data"]
                    df_over_limit["alarm_field"] = field
                    df_over_limit["alarm_data"] = df_over_limit["alarm_data"].apply(lambda x: "{}本次巡检值: ".format(field) + str(x))
                    df_over_limit["warning_type"] = "超上门限"
                    df_over_limit["threshold"] = "{}:本次巡检值>".format(field) + str(limit)
                    df_over_limit_list.append(df_over_limit)
            if df_over_limit_list:
                df_over_limit = pd.concat(df_over_limit_list)
                df_alarm_list.append(df_over_limit)
        if limit_format["min_limit"]:
            df_under_limit_list = []
            for field, limit in limit_format["min_limit"].items():
                df_under_limit = df.loc[df[field] < limit]
                if not df_under_limit.empty:
                    df_under_limit = df_under_limit[["sn", field]]
                    df_under_limit.columns = ["sn", "alarm_data"]
                    df_under_limit["alarm_field"] = field
                    df_under_limit["alarm_data"] = df_under_limit["alarm_data"].apply(lambda x: "{}本次巡检值: ".format(field) + str(x))
                    df_under_limit["warning_type"] = "超下门限"
                    df_under_limit["threshold"] = "{}:本次巡检值>".format(field) + str(limit)
                    df_under_limit_list.append(df_under_limit)
            if df_under_limit_list:
                df_under_limit = pd.concat(df_under_limit_list)
                df_alarm_list.append(df_under_limit)
        if df_alarm_list:
            return pd.concat(df_alarm_list)
        else:
            return pd.DataFrame()

    def warning_by_barcode(self, barcode):
        """
        按编码进行预警
        """
        df_warning_rules = self.get_warning_rules_by_barcode(barcode, option="warning_rules")
        df_front_rules = df_warning_rules.loc[df_warning_rules["front_alarm_rules"] != ""]  # 取出有前置预警条件的规则
        front_alarm_rules = dict(zip(df_front_rules["warning_type"].to_list(), df_front_rules["front_alarm_rules"].to_list()))  # 打包为dict
        field_list = list(set(reduce(add, [eval(field) for field in df_warning_rules["fields"].to_list()])))  # 取出所有预警规则设计的全部字段
        all_alarm_info_list = []
        df_historical = None
        df_threshold_and_per_rules = self.get_warning_rules_by_barcode(barcode)
        #  拿到编码预处理规则以及门限
        pre_processing_rule = df_threshold_and_per_rules["pre_processing_rule"].to_list()
        threshold_rule = df_threshold_and_per_rules["threshold_rule"].to_list()
        df_current = self.get_insp_data_by_barcode(barcode, field_list)
        #  对数据进行预处理
        df_current = self.handle_pre_processing_data(df_current, pre_processing_rule)
        sn_list = df_current["sn"].drop_duplicates().to_list()
        df_over_limit = self.threshold_warning(df_current, threshold_rule)
        all_alarm_info_list.append(df_over_limit)

        for i, row in df_warning_rules:
            warning_type = row['warning_type']
            is_multiple = eval(row["is_multiple"])
            fields = eval(row["fields"])
            rules = row["rules"]
            rules_split = rules.split(";")  # 按分号把单条规则拆分
            historical_flag = False
            #  historical标志位，是否取历史巡检数据
            for key in self.historical_keywords:
                if key in rules_split:
                    historical_flag = True
                    break
            if historical_flag:
                #  已经取过历史数据就不再取了，没取过就按用今日巡检的sn取历史数据，避免重复取值
                if df_historical is None:
                    df_historical = self.get_insp_data_by_barcode(sn_list, field_list)
                df = df_historical[fields]
            else:
                df = df_current[fields]
            df_result = self.warning_by_single_rule(warning_type, is_multiple, fields, rules, rules_split, historical_flag, df)
            all_alarm_info_list.append(df_result)
        df_all = pd.concat(all_alarm_info_list)
        if front_alarm_rules:
            df_all = self.handle_front_warning_rule(df_all, front_alarm_rules)



    def handle_keywords(self, df_group, field, key):
        """
        对每个关键字进行计算
        """
        if key == '最大值':
            temp_df = df_group[field].max().reset_index()
        elif key == '最小值':
            temp_df = df_group[field].min().reset_index()
        elif key == '上一次巡检值':
            newest_index = df_group.apply(lambda x: x[x["insp_date"] == x["insp_date"].max()]).index
            temp = df_group.drop([x[1] for x in newest_index], axis=0)
            temp_df = temp.groupby("sn").apply(lambda x: x[x["insp_date"] == x["insp_date"].max()])[
                [field]].reset_index()[["sn", field]]
        elif key == "本次巡检值":
            temp_df = df_group.apply(lambda x: x[x["insp_date"] == self.date])[[field]].reset_index()
            temp_df = temp_df[["sn", field]]
        else:
            raise ValueError("关键字错误！")
        temp_df.columns = ["sn", field + key]
        return temp_df

    def warning_by_single_rule(self, warning_type, is_multiple, fields, rules, rules_split, historical_flag, df):
        """
        对每条预警规则进行预警逻辑处理
        """
        sn_list = df["sn"].drop_duplicates().to_list()
        if historical_flag:
            df_group = df.groupby("sn")
            key_words = list(set([key for key in self.keywords if key in rules]))  # 此规则包含的关键字
            df_res = pd.DataFrame({"sn": sn_list})
            df_list = [df_res]
            exist_combination = []
            if is_multiple:
                for field in fields:
                    for key in key_words:
                        if (field, key) in exist_combination:
                            continue
                        temp_df = self.handle_keywords(df_group, field, key)
                        exist_combination.append((field, key))
                        df_list.append(temp_df)
                df_all = reduce(lambda lt, rt: pd.merge(lt, rt, how="left", on="sn"), df_list)
                df_list = []
                for field in fields:
                    temp_df = pd.DataFrame()
                    code_str = "temp_df = df_all.loc["
                    for item in rules_split:
                        if item in ("且", "或"):
                            code_str += self.logic_relation[item]
                        else:
                            field_fake, rule = item.strip("()").split(":")
                            temp_str = item.replace(field_fake + ":", "(")
                            for key in key_words:
                                temp_str = temp_str.replace(key, "df_all['{}']".format(field + key))
                            temp_str = temp_str.replace("=", "==").replace("≥", ">=").replace("≤", "<=").replace("≠", "!=")
                            code_str += (temp_str + ")")
                    code_str += "]"
                    try:
                        exec(code_str)
                    except BaseException as e:
                        raise ValueError("预警程序报错！{}".format(e))
                    if not temp_df.empty:
                        cols = [col for col in temp_df.columns.to_list() if field in col]
                        temp_df = temp_df[["sn"] + cols]
                        temp_df["alarm_data"] = temp_df.apply(lambda row: self.splice_alarm_data(row), axis=1)
                        temp_df = temp_df[["sn", "alarm_data"]]
                        temp_df["alarm_field"] = field
                        temp_df["warning_type"] = warning_type
                        temp_df["threshold"] = rules.replace(field_fake, field).replace(";", " ")
                    df_list.append(temp_df)
                df_all = pd.concat(df_list)
                return df_all
            else:
                for item in rules_split:
                    if item not in ("且", "或"):
                        field, rule = item.strip("()").split(":")
                        _key_words = list(set([key for key in key_words if key in rule]))
                        for key in _key_words:
                            if (field, key) in exist_combination:
                                continue
                            temp_df = self.handle_keywords(df_group, field, key)
                            exist_combination.append((field, key))
                            df_list.append(temp_df)
                df_all = reduce(lambda lt, rt: pd.merge(lt, rt, how="left", on="sn"), df_list)
                temp_df = pd.DataFrame()
                code_str = "temp_df = df_all.loc["
                for item in rules_split:
                    if item in ("且", "或"):
                        code_str += self.logic_relation[item]
                    else:
                        field, rule = item.strip("()").split(":")
                        temp_str = item.replace(field + ":", "(")
                        for key in key_words:
                            if key in rule:
                                temp_str = temp_str.replace(key, "df_all['{}']".format(field + key))
                        temp_str = temp_str.replace("=", "==").replace("≥", ">=").replace("≤", "<=").replace("≠", "!=")
                        code_str += (temp_str + ")")
                code_str += "]"
                try:
                    exec(code_str)
                except BaseException as e:
                    raise ValueError("预警程序报错！{}".format(e))
                if not temp_df.empty:
                    temp_df["alarm_data"] = temp_df.apply(lambda row: self.splice_alarm_data(row), axis=1)
                    temp_df = temp_df[["sn", "alarm_data"]]
                    temp_df["alarm_field"] = ';'.join(fields)
                    temp_df["warning_type"] = warning_type
                    temp_df["threshold"] = rules.replace(";", " ")
                return temp_df
        else:
            if is_multiple:
                df_list = []
                for field in fields:
                    temp_df = pd.DataFrame()
                    code_str = "temp_df = df.loc["
                    for item in rules_split:
                        if item in ("且", "或"):
                            code_str += self.logic_relation[item]
                        else:
                            field_fake, rule = item.strip("()").split(":")
                            temp_str = item.replace(field_fake + ":", "(")
                            temp_str = temp_str.replace("本次巡检值", "df['{}']".format(field)).replace("=", "==").replace(
                                "≥", ">=").replace("≤", "<=").replace("≠", "!=")
                            code_str += (temp_str + ")")
                    code_str += "]"
                    try:
                        exec(code_str)
                    except BaseException as e:
                        raise ValueError("预警程序报错！{}".format(e))
                    if not temp_df.empty:
                        temp_df = temp_df[["sn", field]]
                        temp_df.columns = ["sn", "alarm_data"]
                        temp_df["alarm_data"] = temp_df["alarm_data"].apply(lambda x: "{}本次巡检值: ".format(field) + str(x))
                        temp_df["alarm_field"] = field
                        temp_df["warning_type"] = warning_type
                        temp_df["threshold"] = rules.replace(";", " ").replace(field_fake, field)
                    df_list.append(temp_df)
                df_all = pd.concat(df_list)
                return df_all
            else:
                temp_df = pd.DataFrame()
                code_str = "temp_df = df.loc["
                for item in rules_split:
                    if item in ("且", "或"):
                        code_str += self.logic_relation[item]
                    else:
                        field, rule = item.strip("()").split(":")
                        temp_str = item.replace(field + ":", "(")
                        temp_str = temp_str.replace("本次巡检值", "df['{}']".format(field))
                        temp_str = temp_str.replace("=", "==").replace("≥", ">=").replace("≤", "<=").replace("≠", "!=")
                        code_str += (temp_str + ")")
                code_str += "]"
                try:
                    exec(code_str)
                except BaseException as e:
                    raise ValueError("预警程序报错！")
                if not temp_df.empty:
                    temp_df.columns = [col if col == "sn" else col + "本次巡检值" for col in temp_df.columns.to_list()]
                    temp_df["alarm_data"] = temp_df.apply(lambda row: self.splice_alarm_data(row), axis=1)
                    temp_df = temp_df[["sn", "alarm_data"]]
                    temp_df["alarm_field"] = ';'.join(fields)
                    temp_df["warning_type"] = warning_type
                    temp_df["threshold"] = rules.replace(";", " ")
                return temp_df

    def handle_front_warning_rule(self, df, front_alarm_rules):
        """
        对有前置预警要求的规则进一步筛选
        """
        df_group = df.groupby("sn")
        sn_list = df["sn"].drop_duplicates().to_list()
        warning_type_list = df["warning_type"].drop_duplicates().to_list()
        for sn in sn_list:
            df_sn = df_group.get_group(sn)
            delete_warning_type = []
            for warning_type, front_warning_type in front_alarm_rules.items():
                if warning_type in df_sn["warning_type"] and (not set(front_warning_type).issubset(set(warning_type_list))):
                    delete_warning_type.append(warning_type)
            if delete_warning_type:
                df = df.loc[~((df["sn"] == sn) & (df["warning_type"].isin(delete_warning_type)))]
        return df

    def start(self):
        pass
