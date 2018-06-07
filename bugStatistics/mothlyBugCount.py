# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"

from .bugconfig import *
from utils.commonTool.op_date import *
import sys

sys.path.append("../")
cn = config()
op_date = op_date()


class excelchartbyweek(object):
    def CountBUGAsWeeklyForHuaLa(self, sheet_name, sql_date):
        # 计算开始时间和结束时间
        dateResult = op_date.month_get(sql_date)
        start_date = dateResult[0][0]
        end_date = dateResult[1][0]
        # title = [u'按周统计图', u'统计日期',u'新增', u'已解决',u'已关闭',u'未解决(累计)',u'延期解决(累计)',u'已关闭(累计)',u'总BUG数']
        # buname = [u"哼哈微信端",u"哼哈商户端(android)",u"哼哈商户端(iOS)",u"哼哈后台",u"哼哈生活(产品)"]
        title = cn.bugStatusList
        buname = cn.hengha_week
        # 定义数据列表
        # 花啦微信端统计所有BUG
        data = []
        # 添加哼哈微信用户端BUG数据
        result1 = cn.BugCountByProject(cn.hh_pjct[0], sql_date)
        data.append(result1)
        # 添加哼哈商户端(android)BUG数据
        result2 = cn.BugCountByProject(cn.hh_pjct[1], sql_date)
        data.append(result2)
        # 添加哼哈商户端(iOS)BUG数据
        result3 = cn.BugCountByProject(cn.hh_pjct[2], sql_date)
        data.append(result3)
        # 添加哼哈运营后台BUG数据
        result4 = cn.BugCountByProject(cn.hh_pjct[3], sql_date)
        data.append(result4)
        result11 = cn.BugCountByProject(cn.hh_pjct[4], sql_date)
        data.append(result11)
        result12 = cn.BugCountByProject(cn.hh_pjct[5], sql_date)
        data.append(result12)
        result13 = cn.BugCountByProject(cn.hh_pjct[6], sql_date)
        data.append(result13)
        return data

    def CountBUGAsWeeklyForERP(self, sheet_name, sql_date):
        # 计算开始时间和结束时间
        dateResult = op_date.month_get(sql_date)
        start_date = dateResult[0][0]
        end_date = dateResult[1][0]
        # title = [u'按周统计图', u'统计日期',u'新增', u'已解决',u'已关闭',u'未解决(累计)',u'延期解决(累计)',u'已关闭(累计)',u'总BUG数']
        # buname = [u"ERP2.0(产品)",u"CRM(产品)",u"VMP(产品)"]
        title = cn.bugStatusList
        buname = cn.erpyuvmp_week
        # 定义数据列表
        # ERP统计所有BUG
        data = []
        # 添加ERP2.0 BUG数据
        result1 = cn.BugCountByProduct(cn.erp_pdct_list[0], sql_date)
        data.append(result1)
        # CRM BUG数据
        result2 = cn.BugCountByProduct(cn.erp_pdct_list[1], sql_date)
        data.append(result2)
        # VMP BUG数据
        result3 = cn.BugCountByProduct(cn.erp_pdct_list[2], sql_date)
        data.append(result3)
        return data

    def CountBUGAsWeeklyForDev(self, sheet_name, sql_date):
        # 计算开始时间和结束时间
        dateResult = op_date.month_get(sql_date)
        start_date = dateResult[0][0]
        end_date = dateResult[1][0]

        # title = [u'按周统计图', u'统计日期',u'新增', u'已解决',u'已关闭',u'未解决(累计)',u'延期解决(累计)',u'已关闭(累计)',u'总BUG数']
        # buname = [u"哼哈微信端",u"哼哈商户端(android)",u"哼哈商户端(iOS)",u"哼哈后台",u"哼哈生活(产品)"]
        title = cn.bugStatusList
        buname = cn.dev_user_cn
        # 获取row长度
        row_len = len(buname)
        # 获取col长度
        col_len = len(title)
        # 定义数据列表
        # 花啦微信端统计所有BUG

        data = []
        # 添加哼哈微信用户端BUG数据
        result1 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[0])
        data.append(result1)
        # 添加哼哈商户端(android)BUG数据
        result2 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[1])
        data.append(result2)
        # 添加哼哈商户端(iOS)BUG数据
        result3 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[2])
        data.append(result3)
        # 添加哼哈运营后台BUG数据
        result4 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[3])
        data.append(result4)
        # 添加哼哈生活BUG数据
        result5 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[4])
        data.append(result5)
        result11 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[5])
        data.append(result11)
        result12 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[6])
        data.append(result12)
        result13 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[7])
        data.append(result13)
        result14 = cn.BugCountByPerson(cn.erp_pdct_list[1], sql_date, cn.dev_user[8])
        data.append(result14)
        return data

    def CountBUGLevelAsWeeklyForDev(self, sheet_name, sql_date):
        # 计算开始时间和结束时间
        dateResult = op_date.month_get(sql_date)
        start_date = dateResult[0][0]
        end_date = dateResult[1][0]
        # 定义数据列表
        data_level = []
        result_level_dev = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[0])
        data_level.append(result_level_dev)
        result_level_dev2 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[1])
        data_level.append(result_level_dev2)
        result_level_dev3 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[2])
        data_level.append(result_level_dev3)
        result_level_dev4 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[3])
        data_level.append(result_level_dev4)
        result_level_dev5 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[4])
        data_level.append(result_level_dev5)
        result_level_dev6 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[5])
        data_level.append(result_level_dev6)
        result_level_dev7 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[6])
        data_level.append(result_level_dev7)
        result_level_dev8 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[7])
        data_level.append(result_level_dev8)
        result_level_dev9 = cn.BugCountByLevelForDev(cn.erp_pdct_list[1], sql_date, cn.dev_user[8])
        data_level.append(result_level_dev9)
        return data_level


if __name__ == "__main__":
    # 计算开始时间和结束时间
    print(u"您现在正在使用BUG报表自动生成脚本！！！")
    dateValue = str(input(u'请输入日期(参考格式:2016-01-06 11:11:11) :'))
    if dateValue == "":
        dateNow = datetime.datetime.now()
        print(u"没有输入日期，默认按照当前日期生成报表，当前日期为:")
        print(dateNow)
        dateResult = op_date.week_get(dateNow)
        start_date = dateResult[0][0][:-9]
        end_date = dateResult[1][0][:-9]
        bugcount = excelchartbyweek()
        bugcount.CountBUGAsWeeklyForHuaLa(u"buydodo", dateNow)
        bugcount.CountBUGAsWeeklyForERP(u"product", dateNow)
        bugcount.CountBUGAsWeeklyForDev(u"dev", dateNow)
    else:
        print(u"您输入的日期为:" + dateValue)
        dateResult = op_date.month_get(dateValue)
        start_date = dateResult[0][0][:-9]
        end_date = dateResult[1][0][:-9]
        bugcount = excelchartbyweek()
        bugcount.CountBUGAsWeeklyForHuaLa(u"采多多产品bug按月份统计", dateValue)
        bugcount.CountBUGAsWeeklyForERP(u"各产品线bug按月份统计", dateValue)
        bugcount.CountBUGAsWeeklyForDev(u"开发bug按月份统计", dateValue)
        bugcount.CountBUGLevelAsWeeklyForDev(u"bug优先级按月份统计", dateValue)
