# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from .aif.demo_adversarial_debiasing import ad_debiasing
from .aif.demo_reject_option_classification import rej_option_classification
from .aif.demo_reweighing_preproc import reweighing_pre
from .aif.demo_optim_data_preproc import optim_pre
from .aif.pca import get_pca_data
from .aif.tsne import get_tsne_data

import time
import json
import pandas as pd
import numpy as np
import os
import math

import urllib.request


@csrf_exempt
def data(request):
    request.session.clear()
    return render(request, "data.html")


@csrf_exempt
def check(request):
    if request.POST:
        data = request.POST.dict()
        select_val = data["select_val"]
        if select_val == None:
            select_val = "compas"
        request.session["select_val"] = select_val
        # air_re = ad_debiasing.Run(0, 0)
        print(dict(select_val=select_val))
        return render(request, "", dict(select_val=select_val))
    else:
        return redirect("/data")


@csrf_exempt
def before_chart_data(request):
    select_val = request.session.get("select_val")

    if select_val == "german":
        data_num = 1
    elif select_val == "compas":
        data_num = 2
    else:
        data_num = 0  # adult

    print("pca start")
    pca_xy_data = get_pca_data(select_val)
    print("tsen start")
    tsen_xy_data = get_tsne_data(select_val)

    # aif_sex = [0.6805542718669072, 0.2885129845577049, -0.2555749744530078, 0.16167207084908367, 0.16642568513154748]
    # aif_race = [0.6651622649901727, 0, -0.46325241104090453, 0.2835150780766775, 0.17735412756979385]
    print("aif start")
    aif_sex = ad_debiasing.Run_before(data_num, 0)
    aif_race = ad_debiasing.Run_before(data_num, 1)

    aif_race = list(map(lambda x: round(x, 2), aif_race))
    aif_sex = list(map(lambda x: round(x, 2), aif_sex))
    # time.sleep(1)

    return HttpResponse(
        json.dumps(
            {
                "aif_sex": aif_sex,
                "aif_race": aif_race,
                "pca_xy_data": pca_xy_data,
                "tsen_xy_data": tsen_xy_data,
            }
        )
    )


def numberTest(value):
    return list(map(lambda x: float(x) if x.isdigit() else x, value))


def conv_inf_nan(x):
    if x == np.inf:
        print("\n\n---INF---{}\n\n".format(type(x)))
        return 1.0
    elif math.isnan(x):
        print("\n\n---NAN---{}\n\n".format(type(x)))
        return 0.0
    else:
        print("===NUMBER===", x, type(x))
        return x


@csrf_exempt
def after_chart_data(request):
    msgtag = "view > after_chart_data, 세션값들 바로 출력".split(",")
    print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
    print(
        request.session.get("protect"),
        request.session.get("features"),
        request.session.get("optimValue"),
        request.session.get("label"),
    )
    print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

    select_val = request.session.get("select_val")
    select_val2 = request.session.get("select_val2")

    if select_val == "adult":
        data_num = 0
        protect = ["Race", "White", "Sex", "Male"]
        features = []
        optimValue = []
        label = []
    elif select_val == "german":
        data_num = 1
        protect = ["Sex", "Male", "Age", "Old"]
        features = []
        optimValue = []
        label = []
    elif select_val == "compas":
        data_num = 2
        protect = ["Sex", "Female", "Race", "Caucasian"]
        features = []
        optimValue = []
        label = []
    else:
        data_num = 3
        protect = numberTest(request.session.get("protect"))
        features = numberTest(request.session.get("features"))
        label = numberTest(request.session.get("label"))

        optimValue = []
        optim = request.session.get("optimValue")
        for ilist in optim:
            print(ilist)
            optimValue.append(numberTest(ilist))

    pca_xy_data = get_pca_data(select_val)
    tsen_xy_data = get_tsne_data(select_val, protect)

    msgtag = "view > after_chart_data, 세션값들 출력".split(",")
    print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
    print(select_val, select_val2, protect, features, optimValue, label)
    print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")
    if select_val2 == "Reweighing":
        aif_value1 = reweighing_pre.Run(
            select_val, protect, 0, features, optimValue, label
        )
        aif_value2 = reweighing_pre.Run(
            select_val, protect, 1, features, optimValue, label
        )

    elif select_val2 == "Optimized pre-processing":
        aif_value1 = optim_pre.Run(select_val, protect, 0, features, optimValue, label)
        aif_value2 = optim_pre.Run(select_val, protect, 1, features, optimValue, label)

    elif select_val2 == "Adversarial Debiasing":
        aif_value1 = ad_debiasing.Run_before(
            select_val, protect, 0, features, optimValue, label
        )
        aif_value2 = ad_debiasing.Run_before(
            select_val, protect, 1, features, optimValue, label
        )
        before_val1_acc = aif_value1.pop()
        before_val2_acc = aif_value2.pop()
        aif_value1 += ad_debiasing.Run_after(
            select_val, protect, 0, features, optimValue, label
        )
        aif_value2 += ad_debiasing.Run_after(
            select_val, protect, 1, features, optimValue, label
        )
        aif_value1.insert(-1, before_val1_acc)
        aif_value2.insert(-1, before_val2_acc)

        msgtag = "view > after_chart_data > Adversarial,aif값들".split(",")
        print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
        print(aif_value1)
        print(aif_value2)
        print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

    elif select_val2 == "Reject Option Based Classification":
        aif_value1 = rej_option_classification.Run(
            select_val, protect, 0, features, optimValue, label
        )
        aif_value2 = rej_option_classification.Run(
            select_val, protect, 1, features, optimValue, label
        )

    aif_value2 = list(map(lambda x: round(x, 2), aif_value2))
    aif_value1 = list(map(lambda x: round(x, 2), aif_value1))

    # 무한값 0으로 변경
    aif_value1 = list(map(lambda x: conv_inf_nan(x), aif_value1))
    aif_value2 = list(map(lambda x: conv_inf_nan(x), aif_value2))

    msgtag = "view > after_chart_data, 리턴 전에 값들".split(",")
    print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
    print(protect, aif_value2, aif_value2, pca_xy_data[:10], tsen_xy_data[:10])
    print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

    msgtag = "view > after_chart_data, 세션값들 마지막 출력".split(",")
    print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
    print(
        request.session.get("protect"),
        request.session.get("features"),
        request.session.get("optimValue"),
        request.session.get("label"),
    )
    print(select_val, select_val2, protect, features, optimValue, label)

    print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

    return HttpResponse(
        json.dumps(
            {
                "protect": protect,
                "aif_value1": aif_value1,
                "aif_value2": aif_value2,
                "pca_xy_data": pca_xy_data,
                "tsen_xy_data": tsen_xy_data,
            }
        )
    )


# 로컬 csv 업로드시
@csrf_exempt
def uploadCSV(request):
    if request.method == "POST":
        if not "csvFile" in request.FILES:
            print(request.FILES)
            return HttpResponse(401)
        csvData = request.FILES["csvFile"]

        # 파일 저장
        fs = FileSystemStorage()
        filename = fs.save(csvData.name, csvData)
        uploaded_file_url = fs.url(filename)

        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", filename
        )
        df = pd.read_csv(filepath)
        dlist = df.values.tolist()
        dlist.insert(0, list(df))

        return HttpResponse(json.dumps({"csvName": filename, "csvFile": dlist}))
    return HttpResponse(status=405)


# url csv 업로드시
@csrf_exempt
def uploadUrlCSV(request):
    if request.method == "POST":
        csvUrl = request.POST["url"]
        filename = request.POST["filename"]
        filename = filename if filename.split(".")[-1] == "csv" else filename + ".csv"
        # url
        urllib.request.urlretrieve(csvUrl, "data/" + filename)

        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", filename
        )

        df = pd.read_csv(filepath)
        dlist = df.values.tolist()
        dlist.insert(0, list(df))

        return HttpResponse(json.dumps({"csvName": filename, "csvFile": dlist}))
    return HttpResponse(status=405)


# 선택한 항목 세션에 저장
@csrf_exempt
def select_attribute_option(request):
    if request.method == "POST":
        request.session["protect"] = request.POST["protect"].split(",")
        features = request.POST["features"].split(",")
        features[-1] = features[-1].replace("\n", "")
        request.session["features"] = features
        request.session["optimValue"] = stringToArray(
            request.POST["optimValue"].split(",")
        )
        request.session["label"] = request.POST["label"].split(",")

    return HttpResponse()


def stringToArray(str):
    result = []
    for i in range(0, len(str), 3):
        result.append([str[i], str[i + 1], str[i + 2]])

    return result


@csrf_exempt
def mitigate(request):
    if request.POST:
        data = request.POST.dict()
        select_val = data["select_val"]

        if select_val == None:
            select_val = "compas"

        request.session["select_val"] = select_val
        return render(request, "mitigate.html", dict(select_val=select_val))
    # post 아닐경우 /data에 머무르기
    else:
        return redirect("/data")


@csrf_exempt
def compare(request):
    if request.POST:
        data = request.POST.dict()
        select_val = data["select_val"]
        select_val2 = data["select_val2"]
        request.session["select_val2"] = select_val2
        return render(
            request,
            "compare.html",
            dict(select_val=select_val, select_val2=select_val2),
        )
    else:
        return redirect("/data")

