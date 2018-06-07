# -*- coding: UTF-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import os
from bs4 import BeautifulSoup
from readcase.models import testcase, case
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def insertSql(list):
    cases = testcase()
    for i in range(0, len(list)):
        id = list[i]["id"]
        title = list[i]["title"]
        pid = list[i]["pid"]
        children_list = list[i]["children"]
        try:
            cases.id = int(id)
            cases.title = title
            cases.pid = int(pid)
            cases.save()
        except Exception as e:
            print("插入数据出错")
        if len(children_list) == 0:
            pass
        else:
            insertSql(children_list)


def pase_html2json(filename):
    baseDir = os.path.dirname(os.path.abspath(__name__))
    filePath = os.path.join(baseDir + "\\uploads\\", filename)
    file = open(file=filePath, encoding="utf-8").read()
    soup = BeautifulSoup(file, "html.parser")
    allData = []
    count = 1
    for k in soup.find_all("a"):
        value = k.text.replace(u'\xa0', u'$')
        allData.append([count, value])
        count += 1
    sz = []
    allData[0].append(0)
    allData[1].append(0)
    sz.append(allData[0])
    sz.append(allData[1])
    for i in range(len(allData)):
        if i > 1:
            prew_index = len(allData[i - 1][1]) - len(allData[i - 1][1].replace('$', ''))
            now_index = len(allData[i][1]) - len(allData[i][1].replace('$', ''))
            if now_index - prew_index == 1:
                allData[i].append(allData[i - 1][0])
            elif now_index - prew_index == 0:
                try:
                    allData[i].append(allData[i - 1][2])
                except Exception as e:
                    print(e)
            elif now_index - prew_index < 0:
                for l in range(0, len(sz)):
                    # 找新数组
                    _prew_index = len(sz[(len(sz) - 1) - l][1]) - len(sz[(len(sz) - 1) - l][1].replace('$', ''))
                    if now_index - _prew_index == 0:
                        allData[i].append(sz[(len(sz) - 1) - l][2])
                        break
            sz.append(allData[i])
    newResult = getchild(0, sz)
    for item in range(1, len(newResult)):
        newResult[0]["children"].append(newResult[item])
    for item in range(1, len(newResult)):
        newResult.pop()
    return newResult


def getchild(pid, sz):
    result = []
    for obj in sz:
        if obj[2] == pid:
            result.append({
                "id": obj[0],
                "title": obj[1].replace('$', ''),
                "pid": obj[2],
                "children": getchild(obj[0], sz),
            })
    return result


def index(request):
    return render(request, "index.html")


def handle_upload_file(file, filename):
    baseDir = os.path.dirname(os.path.abspath(__name__))
    path = os.path.join(baseDir, 'uploads')  # 上传文件的保存路径
    if not os.path.exists(path):
        os.makedirs(path)
    if len(file) == 0 or filename == "":
        pass
    else:
        with open(os.path.join(path, filename), 'wb+')as destination:
            for chunk in file.chunks():
                destination.write(chunk)


def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    if request.method == "POST":
        if request.FILES.get("upload", "") == "":
            return render(request, "upload.html")
        handle_upload_file(request.FILES.get("upload", ""), str(request.FILES.get("upload", "")))
        insertSql(pase_html2json(str(request.FILES.get("upload", ""))))
        dashboard()
        return HttpResponseRedirect('/readcase/data_manage/')


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if username == "skyhuang" and password == "123456":
        return HttpResponseRedirect("/readcase/data_manage/")
    else:
        return render(request, "login2.html")


# 处理上传用例文件的数据写入case表中
def dashboard():
    alldata = testcase.objects.all()
    ids = []
    pids = []
    for i in alldata:
        ids.append(i.id)
        pids.append(i.pid)
    frist_caseModel_id = [i for i in pids if i not in ids]  # [0,0,0,0]
    caseModelData = testcase.objects.exclude(pid__in=frist_caseModel_id)  # 除pid=0的所有数据
    second_id = testcase.objects.filter(pid=frist_caseModel_id[0])
    second_caseModel_id = [i.id for i in second_id]  # [1,2,7,15]
    second_caseModelData = testcase.objects.exclude(pid__in=second_caseModel_id)  # [4,8,10,13,16]
    third_pid = [i.pid for i in second_caseModelData]  # [4,8,10,13,16]
    projectName = alldata[0].title
    modelName = ""
    caseds = ""
    re_list = []
    for i in caseModelData:
        re_json = {"caseId": i.id, "projectName": projectName, "modelName": modelName, "case": caseds,
                   "casestatu": i.result}
        if i.id not in third_pid:
            if i.pid in third_pid:
                parent_id = testcase.objects.get(id=i.pid).pid
                caseTitle = testcase.objects.get(id=parent_id).title
                re_json["modelName"] = caseTitle
                title1 = testcase.objects.get(id=i.pid).title
                title2 = i.title
                re_json["case"] = title1 + "--->" + title2
                re_list.append(re_json)
            else:
                caseTitle = testcase.objects.get(id=i.pid).title
                re_json["modelName"] = caseTitle
                re_json["case"] = i.title
                re_list.append(re_json)
        else:
            pass

    for i in range(0, len(re_list)):
        allcase = case()
        allcase.caseId = int(re_list[i]["caseId"])
        allcase.project = re_list[i]["projectName"]
        allcase.modelName = re_list[i]["modelName"]
        allcase.caseDetail = re_list[i]["case"]
        allcase.result = int(re_list[i]["casestatu"])
        allcase.save()


# 分页功能
def data_manage(request):
    # data_list = case.objects.all()
    data_list = case.objects.get_queryset().order_by('id')
    paginator = Paginator(data_list, 10)
    page = request.GET.get("page")
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return render(request, "casedashboard.html", {"data": data})


def executecase(request):
    if request.method == "GET":
        id = request.GET.get("caseid")
        statu = request.GET.get("statu")
        cases = case.objects.get(id=id)
        cases.result = int(statu)
        cases.save()
    if request.method == "POST":
        try:
            params = request.POST.get("data")
            param_list = params.split("&")[1:]
            statu = param_list[0].split("=")[1]
            caseIds = param_list[1].split("=")[1:]
            case_ids_list = caseIds[0].split(",")
            for k in case_ids_list:
                if len(k) == 0:
                    pass
                else:
                    cases = case.objects.get(id=k)
                    cases.result = int(statu)
                    cases.save()
        except Exception:
            return HttpResponse(0)
    return HttpResponseRedirect("/readcase/data_manage/")


def casechart(request):
    projectName = request.GET.get("input_project")
    if projectName == None or len(projectName.strip()) <= 0:
        return render(request, "casechart.html")
    modelName_distinct = case.objects.filter(project__contains=projectName).values("modelName").distinct()
    if len(modelName_distinct) == 0:
        return render(request, "casechart.html")
    chartList = []
    success_total = 0
    skip_total = 0
    fail_total = 0
    cases_total = 0

    for i in modelName_distinct:
        re_json = {"projectName": "", "modelName": "", "casetotal": "", "success": "", "skip": "", "fail": ""}
        re_json["projectName"] = case.objects.filter(modelName=i["modelName"])[0].project
        re_json["modelName"] = i["modelName"]
        re_json["success"] = case.objects.filter(modelName=i["modelName"]).filter(result=0).count()
        re_json["skip"] = case.objects.filter(modelName=i["modelName"]).filter(result=2).count()
        re_json["fail"] = case.objects.filter(modelName=i["modelName"]).filter(result=1).count()
        re_json["casetotal"] = case.objects.filter(modelName=i["modelName"]).count()
        chartList.append(re_json)

    for j in chartList:
        success_total += int(j["success"])
        skip_total += int(j["skip"])
        fail_total += int(j["fail"])
        cases_total += int(j["casetotal"])
        re_total = {"success_total": success_total, "skip_total": skip_total, "fail_total": fail_total,
                    "cases_total": cases_total}
    return render(request, "casechart.html", {"data": chartList, "re_total": re_total})
