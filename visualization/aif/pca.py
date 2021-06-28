from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import random
import pandas as pd


def get_pca_data(select_val):
    defaultVal = ["adult", "compas", "german"]
    if isUploadedFile(select_val):
        path = "visualization/data/" + select_val
    elif select_val in defaultVal:
        path = "visualization/data/" + select_val + ".data"
    else:
        print("=-=-=-=-=-=-nodata-=-=-=-=-=")
        path = "visualization/data/compas.data"

    data_sp = []
    le = preprocessing.LabelEncoder()

    if isUploadedFile(select_val):
        df = pd.read_csv(path).fillna("")
        data_sp = list(df)
        data = df.values.tolist()

    else:
        f = open(path)
        data = []
        while True:
            line = f.readline()
            if not line:
                break
            data.append(line)

        data = data[:-1]
        data_sp = data[0].split(",")

    new_data = []

    for i in range(len(data)):
        if isUploadedFile(select_val):
            tmp_data = data[i]
        else:
            if data[i].find('"') != -1:
                s = []
                data[i] = data[i].split('"')

                for d in data[i]:
                    if len(d) and d[0] != "," and d[len(d) - 1] != ",":
                        s.append(d)
                    else:
                        if d == "":
                            continue
                        if d[0] == ",":
                            d = d[1:]
                        if d[-1] == ",":
                            d = d[:-1]
                        if d != "":
                            s.extend(d.split(","))
                if len(s) == len(data_sp) - 1:
                    print("last index null", len(s), len(data[0]) - 1)
                    s.append("")
                tmp_data = s
            else:
                tmp_data = data[i].split(",")
            # 라인이 비어있는지 확인(마지막 개행제거)
            if isEmptyLint(tmp_data[:-1]):
                continue

        for idx, d in enumerate(tmp_data):
            try:
                tmp_data[idx] = int(d)
            except:
                continue
        new_data.append(tmp_data)

    # -------------------------------지우기-----------------------------
    print("data length test+++++++", end="\n\n")
    testtt = True
    for i in new_data:
        if len(new_data[0]) != len(i):
            print("다름!!", len(new_data[0]), len(i), i)
            testtt = False
    if testtt:
        print("통과")
    else:
        print("error")
    # ====================================================================

    # 인코딩
    for i in range(len(new_data[0])):
        trans_list = []
        for d in new_data:
            trans_list.append(d[i])
        le.fit(trans_list)
        trans_res = le.transform(trans_list)

        for idx, d in enumerate(new_data):
            d[i] = trans_res[idx]

    # PCA 모델 생성 및 학습
    tsne = TSNE(n_components=2, n_iter=500)
    pca = PCA(n_components=2)

    if select_val == "compas":
        new_data = list(map(lambda x: x[1:52], new_data))

    new_data_std = StandardScaler().fit_transform(new_data)

    pca_features = pca.fit_transform(new_data_std)
    # pca_features = tsne.fit_transform(new_data_std)

    xf = pca_features[:, 0]
    yf = pca_features[:, 1]
    xy_data = list(map(lambda x, y: [round(x, 2), round(y, 2)], xf, yf))
    # xy_data = random.sample(xy_data, 10000)
    return xy_data


# 비어있는 라인 식별
def isEmptyLint(tmp_data):
    tmp = True
    for x in tmp_data:
        if x != "":
            tmp = False
            break
    return tmp


def isUploadedFile(select_val):
    return True if select_val.split(".")[-1] == "csv" else False

