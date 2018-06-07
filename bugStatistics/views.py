from django.shortcuts import render
from django.http import JsonResponse
from .bugconfig import config


# Create your views here.


def bugCount(request):
    return render(request, "bug.html")


def getBugData(request):
    cn = config()
    mothods = request.method
    try:
        if mothods == "POST":
            return JsonResponse({"code": 400, "status": "fail"})
        if mothods == "GET":
            # data = {"欧阳文": [22, 18, 19, 34, 29], "吴庆军": [15, 21, 21, 54, 10],
            #         "丁力": [22, 18, 19, 34, 9], "何衍阳": [15, 21, 21, 54, 10],
            #         "刘嘉明": [28, 38, 9, 22, 10], "曾巨才": [12, 13, 11, 4, 20],
            #         "陈龙": [8, 8, 9, 4, 0], "罗英麟": [2, 23, 11, 44, 30], "郭冠兰": [55, 38, 7, 18, 19]}
            data = {}
            for i in range(0, len(cn.dev_user)):
                d = cn.BugCountByPerson(cn.erp_pdct_list[1], "2018-04-06 00:00:00", cn.dev_user[i])
                data = dict(d, **data)
            name_list = []
            value_list = []
            for key, value in data.items():
                name_list.append(key)
                value_list.append(value)
            values = []
            for l1, l2, l3, l4, l5, l6, l7, l8, l9 in zip(*value_list):
                list2 = [l1, l2, l3, l4, l5, l6, l7, l8, l9]
                values.append(list2)
            datas = {"name": name_list, "vaules": values}
            return JsonResponse({"code": 200, "status": "success", "data": datas})
        return JsonResponse({"code": 400, "status": "fail"})
    except Exception as e:
        print(e)