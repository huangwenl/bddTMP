# -*- coding: UTF-8 -*-
__Author__ = "Sky Huang"

from utils.commonTool.op_date import *
from utils.commonTool.mySqlUtil import *


class config(object):
    def __init__(self):
        self.op_date = op_date()
        self.ms = MysqlUtil()

    # BUG状态分类:
    bugStatusList = [u'按周统计图', u'统计日期', u'新增', u'已解决', u'已关闭', u'未解决(累计)', u'延期解决(累计)', u'已关闭(累计)', u'总BUG数']
    # 采多多产品&项目
    hengha = [[u"采多多Android1.0"], [u"采多多IOS1.0"], [u"采多多管理后台1.0"], [u"采多多产品1.0"], [u"采多多Android1.1"], [u"采多多IOS1.1"],
              [u"采多多管理后台1.1"]]
    # 采多多产品&项目
    hengha_week = [u"采多多Android1.0", u"采多多IOS1.0", u"采多多管理后台1.0", u"采多多产品1.0", "采多多Android1.1", "采多多IOS1.1",
                   "采多多管理后台1.1"]

    # 采多多产品
    erpyuvmp = [[u"惠龙邦平台(产品)"], [u"采多多(产品)"], [u"分润系统税后金额体现(产品)"]]
    # 采多多产品
    erpyuvmp_week = [u"惠龙邦平台(产品)", u"采多多(产品)", u"分润系统税后金额体现(产品)"]

    # 开发人员
    dev_user = ["ouyangwen", "wuqingjun", "luoyinglin", "dingli", "heyanyang", "liujiaming", "zengjucai", "chenlong",
                "guoguanlan"]
    dev_user_cn = ["欧阳文", "吴庆军", "罗英麟", "丁力", "何衍阳", "刘嘉明", "曾巨才", "陈龙",
                   "郭冠兰"]

    def BugCountByProject(self, projectNo, sql_date):
        ms = self.ms
        projectNo = int(projectNo)
        date_result = self.op_date.month_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        # 查找一个星期内新增的BUG数openedDate 例如今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
        AllNewBugCount_OneWeek = "select count(*) from zt_bug where project = '%d' and deleted = '0' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, start_date, end_date)

        # 查找一个星期内已解决的BUG数(以最近的星期天为准，计算星期一到星期天,包含本周 解决到关闭的BUG) resolvedDate
        AllResolvedBugCount_OneWeek = "select count(*) from zt_bug where project = '%d' and deleted = '0' and `status` <> 'active' and resolution <> 'postponed' and resolvedDate >= '%s' and resolvedDate <= '%s'" % (
            projectNo, start_date, end_date)

        # 查找所有未解决BUG数(以最近的星期天为准，计算星期一到星期天)（当前显示BUG状态为未解决的。包含当前还没被解决的、之前遗留的未解决、以及reopen的BUG（累计数据））
        AllNotResolvedBugCount = "select count(*) from zt_bug where project = '%d' and deleted = '0' and `status` =  'active' and openedDate <= '%s'" % (
            projectNo, end_date)

        # 查找用户所有延期解决的问题
        AllPostponedBugCount = "select count(*) from zt_bug where project = '%d' and deleted = '0' and `status` <> 'closed' and resolution = 'postponed' and resolvedDate <= '%s'" % (
            projectNo, end_date)

        # 查找 一个星期内已关闭的BUG数(以最近的星期天为准，计算星期一到星期天) closedDate
        AllClosedBugCount_OneWeek = "select count(*) from zt_bug where project  = '%d' and deleted = '0' and `status` = 'closed' and closedDate >= '%s' and closedDate <= '%s'" % (
            projectNo, start_date, end_date)

        # 查找 已关闭BUG数(累计)
        AllClosedBugCount = "select count(*) from zt_bug where project  = '%d' and deleted = '0' and `status` = 'closed' and closedDate <= '%s'" % (
            projectNo, end_date)

        # 查找 总BUG数
        AllBugCount = "select count(*) from zt_bug where project  = '%d' and deleted = '0' and openedDate <='%s'" % (
            projectNo, end_date)

        # 新增
        dAllNewBugCount_OneWeek = ms.executeQuery(AllNewBugCount_OneWeek)[0]['count(*)']
        # 已解决
        dAllResolvedBugCount_OneWeek = ms.executeQuery(AllResolvedBugCount_OneWeek)[0]['count(*)']
        # 已关闭
        dAllClosedBugCount_OneWeek = ms.executeQuery(AllClosedBugCount_OneWeek)[0]['count(*)']
        # 未解决(累计数据)
        dAllNotResolvedBugCount = ms.executeQuery(AllNotResolvedBugCount)[0]['count(*)']
        # 延期解决(累计数据)
        dAllPostponedBugCount = ms.executeQuery(AllPostponedBugCount)[0]['count(*)']
        # 已关闭(累计)
        dAllClosedBugCount = ms.executeQuery(AllClosedBugCount)[0]['count(*)']
        # 总BUG数
        dAllBugCount = ms.executeQuery(AllBugCount)[0]['count(*)']
        data = ["%s~%s" % (start_date[:-9], end_date[:-9]), dAllNewBugCount_OneWeek, dAllResolvedBugCount_OneWeek,
                dAllClosedBugCount_OneWeek, dAllNotResolvedBugCount, dAllPostponedBugCount, dAllClosedBugCount,
                dAllBugCount]
        ms.close()
        return data

    def BugCountByProduct(self, productNo, sql_date):
        ms = self.ms
        # data = []
        productNo = int(productNo)
        date_result = self.op_date.month_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        # 查找一个星期内新增的BUG数openedDate 例如今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
        AllNewBugCount_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and openedDate >= '%s' and openedDate <= '%s'" % (
            productNo, start_date, end_date)
        # 查找一个星期内已解决的BUG数(以最近的星期天为准，计算星期一到星期天) resolvedDate
        AllResolvedBugCount_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` <> 'active' and resolution <> 'postponed' and resolvedDate >= '%s' and resolvedDate <= '%s'" % (
            productNo, start_date, end_date)
        # 查找 一个星期内已关闭的BUG数(以最近的星期天为准，计算星期一到星期天) closedDate
        AllClosedBugCount_OneWeek = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and `status` = 'closed' and closedDate >= '%s' and closedDate <= '%s'" % (
            productNo, start_date, end_date)

        # 查找所有未解决BUG数(以最近的星期天为准，计算星期一到星期天)（当前显示BUG状态为未解决的。包含当前还没被解决的、之前遗留的未解决、以及reopen的BUG（累计数据））
        AllNotResolvedBugCount = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` =  'active' and openedDate <= '%s'" % (
            productNo, end_date)
        # 查找用户所有延期解决的问题
        AllPostponedBugCount = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` <> 'closed' and resolution = 'postponed'and resolvedDate <= '%s'" % (
            productNo, end_date)
        # 查找 已关闭BUG数(累计)
        AllClosedBugCount = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and `status` = 'closed' and closedDate <= '%s'" % (
            productNo, end_date)

        # 查找 总BUG数
        AllBugCount = "select count(*) from zt_bug where product  = '%d' and deleted = '0'and openedDate <='%s'" % (
            productNo, end_date)

        # 新增
        dAllNewBugCount_OneWeek = ms.executeQuery(AllNewBugCount_OneWeek)[0]['count(*)']
        # 已解决
        dAllResolvedBugCount_OneWeek = ms.executeQuery(AllResolvedBugCount_OneWeek)[0]['count(*)']
        # 已关闭
        dAllClosedBugCount_OneWeek = ms.executeQuery(AllClosedBugCount_OneWeek)[0]['count(*)']
        # 未解决(累计数据)
        dAllNotResolvedBugCount = ms.executeQuery(AllNotResolvedBugCount)[0]['count(*)']
        # 延期解决(累计数据)
        dAllPostponedBugCount = ms.executeQuery(AllPostponedBugCount)[0]['count(*)']
        # 已关闭(累计)
        dAllClosedBugCount = ms.executeQuery(AllClosedBugCount)[0]['count(*)']
        # 总BUG数
        dAllBugCount = ms.executeQuery(AllBugCount)[0]['count(*)']
        data = ["%s~%s" % (start_date[:-9], end_date[:-9]), dAllNewBugCount_OneWeek, dAllResolvedBugCount_OneWeek,
                dAllClosedBugCount_OneWeek, dAllNotResolvedBugCount, dAllPostponedBugCount, dAllClosedBugCount,
                dAllBugCount]
        ms.close()
        return data

    def BugCountBySevereLevel(self, productNo, sql_date):
        # serverLevel = [u"致命", u"严重", u"一般", u"建议"]
        ms = self.ms
        projectNo = int(productNo)
        date_result = self.op_date.month_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        # 查找一个星期内新增的BUG等级为致命的bug个数openedDate 例如今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
        AllNewBugDeadliness_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '1' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, start_date, end_date)
        # print(AllNewBugDeadliness_OneWeek)
        # 查找一个星期内新增严重的bug个数
        AllNewBugDangerous_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '2' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, start_date, end_date)
        # 查找一个星期内新增一般的bug个数
        AllNewBugGeneral_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '3' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, start_date, end_date)
        # 查找一个星期内新增建议的bug个数
        AllNewBugSuggest_OneWeek = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '4' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, start_date, end_date)

        # 数据库查询
        dAllNewBugDeadliness_OneWeek = ms.executeQuery(AllNewBugDeadliness_OneWeek)[0]['count(*)']
        dAllNewBugDangerous_OneWeek = ms.executeQuery(AllNewBugDangerous_OneWeek)[0]['count(*)']
        dAllNewBugGeneral_OneWeek = ms.executeQuery(AllNewBugGeneral_OneWeek)[0]['count(*)']
        dAllNewBugSuggest_OneWeek = ms.executeQuery(AllNewBugSuggest_OneWeek)[0]['count(*)']

        data = ["%s~%s" % (start_date[:-9], end_date[:-9]), dAllNewBugDeadliness_OneWeek, dAllNewBugDangerous_OneWeek,
                dAllNewBugGeneral_OneWeek, dAllNewBugSuggest_OneWeek]
        ms.close()
        return data

    def BugCountByPerson(self, productNo, sql_date, devuser):
        ms = self.ms
        productNo = int(productNo)
        date_result = self.op_date.month_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        # 查找一个星期内指派给某个开发的新增bug个数
        AllNewBugCount_OneWeek_toDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and assignedTo = '%s' and openedDate >= '%s' and openedDate <= '%s'" % (
            productNo, devuser, start_date, end_date)
        # 查找一个星期内指派给某个开发的已解决bug个数
        AllResolvedBugCount_OneWeek_toDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` <> 'active' and resolution <> 'postponed' and resolvedBy = '%s' and resolvedDate >= '%s' and resolvedDate <= '%s'" % (
            productNo, devuser, start_date, end_date)
        # 查找某个开发所有未解决BUG数(以最近的星期天为准，计算星期一到星期天)（当前显示BUG状态为未解决的。包含当前还没被解决的、之前遗留的未解决、以及reopen的BUG（累计数据））
        AllNotResolvedBugCount_toDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` =  'active' and assignedTo = '%s' and openedDate <= '%s'" % (
            productNo, devuser, end_date)
        # 查找某个开发所有延期解决的bug个数
        AllPostponedBugCount_toDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and `status` <> 'closed' and resolution = 'postponed' and resolvedBy = '%s'and resolvedDate <= '%s'" % (
            productNo, devuser, end_date)
        # 查找 一个星期内某个开发已关闭的BUG数(以最近的星期天为准，计算星期一到星期天) closedDate
        AllClosedBugCount_OneWeek_toDev = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and `status` = 'closed' and resolvedBy = '%s' and closedDate >= '%s' and closedDate <= '%s'" % (
            productNo, devuser, start_date, end_date)
        # 查找某个开发已关闭BUG数(累计)
        AllClosedBugCount_toDev = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and `status` = 'closed' and resolvedBy = '%s'and closedDate <= '%s'" % (
            productNo, devuser, end_date)
        # 查找某个开发总BUG数
        # AllBugCount_toDev = "select count(*) from zt_bug where product  = '%d' and deleted = '0' and assignedTo = '%s' and openedDate <='%s'" % (
        #     productNo, dev_user, end_date)

        # 新增
        dAllNewBugCount_OneWeek_toDev = ms.executeQuery(AllNewBugCount_OneWeek_toDev)[0]['count(*)']
        # 已解决
        dAllResolvedBugCount_OneWeek_toDev = ms.executeQuery(AllResolvedBugCount_OneWeek_toDev)[0]['count(*)']
        # 已关闭
        # dAllClosedBugCount_OneWeek_toDev = ms.executeQuery(AllClosedBugCount_OneWeek_toDev)[0]['count(*)']
        # 未解决(累计数据)
        dAllNotResolvedBugCount_toDev = ms.executeQuery(AllNotResolvedBugCount_toDev)[0]['count(*)']
        # 延期解决(累计数据)
        # dAllPostponedBugCount_toDev = ms.executeQuery(AllPostponedBugCount_toDev)[0]['count(*)']
        # 已关闭(累计)
        dAllClosedBugCount_toDev = ms.executeQuery(AllClosedBugCount_toDev)[0]['count(*)']
        # 总BUG数
        dAllBugCount = dAllClosedBugCount_toDev + dAllNotResolvedBugCount_toDev

        data = {devuser: [dAllNewBugCount_OneWeek_toDev,
                          dAllResolvedBugCount_OneWeek_toDev,
                          dAllNotResolvedBugCount_toDev,
                          dAllClosedBugCount_toDev,
                          dAllBugCount]}
        # print(data)
        return data

    def BugCountByLevelForDev(self, productNo, sql_date, dev_user):
        ms = self.ms
        projectNo = int(productNo)
        date_result = self.op_date.month_get(sql_date)
        start_date = date_result[0][0]
        end_date = date_result[1][0]
        # 查找某个开发一个星期内新增的BUG等级为致命的bug个数openedDate 例如今天为2016-01-04 00:00:00，输入这个时间后，会自动查询2015-12-28 00:00:00---2016-01-03 23:59:59时间段内BUG
        AllNewBugDeadliness_OneWeek_ToDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '1' and assignedTo = '%s' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, dev_user, start_date, end_date)
        # 查找某个开发一个星期内新增严重的bug个数
        AllNewBugDangerous_OneWeek_ToDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '2' and assignedTo = '%s' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, dev_user, start_date, end_date)
        # 查找某个开发一个星期内新增一般的bug个数
        AllNewBugGeneral_OneWeek_ToDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '3' and assignedTo = '%s' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, dev_user, start_date, end_date)
        # 查找某个开发一个星期内新增建议的bug个数
        AllNewBugSuggest_OneWeek_ToDev = "select count(*) from zt_bug where product = '%d' and deleted = '0' and severity = '4' and assignedTo = '%s' and openedDate >= '%s' and openedDate <= '%s'" % (
            projectNo, dev_user, start_date, end_date)

        # 数据库查询
        dAllNewBugDeadliness_OneWeek_ToDev = ms.executeQuery(AllNewBugDeadliness_OneWeek_ToDev)[0]['count(*)']
        dAllNewBugDangerous_OneWeek_ToDev = ms.executeQuery(AllNewBugDangerous_OneWeek_ToDev)[0]['count(*)']
        dAllNewBugGeneral_OneWeek_ToDev = ms.executeQuery(AllNewBugGeneral_OneWeek_ToDev)[0]['count(*)']
        dAllNewBugSuggest_OneWeek_ToDev = ms.executeQuery(AllNewBugSuggest_OneWeek_ToDev)[0]['count(*)']

        data = ["%s~%s" % (start_date[:-9], end_date[:-9]), dAllNewBugDeadliness_OneWeek_ToDev,
                dAllNewBugDangerous_OneWeek_ToDev,
                dAllNewBugGeneral_OneWeek_ToDev, dAllNewBugSuggest_OneWeek_ToDev]
        ms.close()
        return data

    def close(self):
        self.ms.close()

    """
    buydodo:
        按project统计
            采多多Android1.0：9
            采多多IOS1.0:8
            采多多管理后台1.0:7
            采多多产品1.0:10
            采多多Android1.1：14
            采多多IOS1.1: 13
            采多多管理后台1.1: 12
        
    ERP&CRM(Product):
        按照产品编号来进行统计
        # 惠龙邦平台 : 2
        # 采多多:4
        # 分润系统税后金额体现 :5
    """
    '''
    采多多(project)
    '''
    # 采多多Android1.0
    henghashandroid_pjct = 9
    henghashandroid11_pjct = 14
    # 采多多IOS1.0
    henghashios_pjct = 8
    henghashios11_pjct = 13
    # 采多多管理后台1.0
    henghayy_pjct = 7
    henghayy11_pjct = 12

    # 采多多产品1.0
    hengha_pjct = 10

    buydodo_pdct = 4

    hh_pjct = [henghashandroid_pjct, henghashios_pjct, henghayy_pjct, henghashandroid11_pjct,
               henghashios11_pjct, henghayy11_pjct, hengha_pjct]
    hh_pdct = [buydodo_pdct]

    '''
    ERP&CRM(Product):
    '''
    # 惠龙邦平台 : 2
    erp_pdct = 2
    # 采多多:4
    crm_pdct = 4
    # 分润系统税后金额体现 :5
    vmp_pdct = 5
    erp_pdct_list = [erp_pdct, crm_pdct, vmp_pdct]

# if __name__ == "__main__":
#     cn = config()
#     data = {}
#     for i in range(0, len(cn.dev_user)):
#         d = cn.BugCountByPerson(cn.erp_pdct_list[1], "2018-04-06 00:00:00", cn.dev_user[i])
#         data = dict(d, **data)
#     cn.close()
#     print(data)
