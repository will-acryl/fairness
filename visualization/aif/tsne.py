from sklearn.manifold import TSNE
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd


def get_tsne_data(select_val, protect):
    defaultVal = ["adult", "compas", "german"]
    if isUploadedFile(select_val):
        path = "visualization/data/" + select_val
    elif select_val in defaultVal:
        path = "visualization/data/" + select_val + ".data"
    else:
        print("=-=-=-=-=-=-nodata-=-=-=-=-=")
        path = "visualization/data/compas.data"

    data_sp = []
    attributeKey = []
    attributeVal = []
    le = preprocessing.LabelEncoder()

    if isUploadedFile(select_val):
        df = pd.read_csv(path).fillna("")
        data_sp = list(df)
        data = df.values.tolist()

        temp1, temp2 = getAttributeIndex(data_sp, protect)
        attributeKey.append(temp1)
        attributeKey.append(temp2)

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

        if select_val == "german":
            male_status = ["A91", "A93", "A94"]

            if tmp_data[8] in male_status:
                tmp_data[8] = "Male"
            else:
                tmp_data[8] = "Female"

            if tmp_data[12] >= 25:
                tmp_data[12] = 0
            else:
                tmp_data[12] = 1

        new_data.append(tmp_data)

    if isUploadedFile(select_val):
        temp1, temp2 = getAttributeValueIndex(new_data, attributeKey, protect)
        attributeVal.append(temp1)
        attributeVal.append(temp2)

    for i in range(len(new_data[0])):
        trans_list = []
        for d in new_data:
            trans_list.append(d[i])
        le.fit(trans_list)
        trans_res = le.transform(trans_list)

        for idx, d in enumerate(new_data):
            d[i] = trans_res[idx]

    # 보호속성만 따로 저장
    protectAttribute1 = []
    protectAttribute2 = []
    if isUploadedFile(select_val):
        protectAttribute1, protectAttribute2 = attributeFilter(
            new_data, attributeKey, attributeVal
        )

    elif select_val == "compas":
        for i in range(len(new_data)):
            protectAttribute1.append(new_data[i][5])
            if new_data[i][9] == 2:
                protectAttribute2.append(1)
            else:
                protectAttribute2.append(0)

    elif select_val == "adult":
        for i in range(len(new_data)):
            protectAttribute1.append(new_data[i][9])
            if new_data[i][8] == 4:
                protectAttribute2.append(1)
            else:
                protectAttribute2.append(0)

    elif select_val == "german":
        for i in range(len(new_data)):
            protectAttribute1.append(new_data[i][8])
            protectAttribute2.append(new_data[i][12])

    # t-SNE 모델 생성 및 학습
    tsne = TSNE(random_state=0, learning_rate=100)
    new_data = np.array(new_data)
    new_data = new_data

    if select_val == "compas":
        new_data = list(map(lambda x: x[1:52], new_data))
    digits_tsne = tsne.fit_transform(new_data)

    xf = digits_tsne[:, 0]
    yf = digits_tsne[:, 1]

    xy_data = list(
        map(
            lambda x, y, g, c: [int(round(x)), int(round(y)), int(g), int(c)],
            xf,
            yf,
            protectAttribute1,
            protectAttribute2,
        )
    )

    return xy_data


# 비어있는 라인 식별
def isEmptyLint(tmp_data):
    tmp = True
    for x in tmp_data:
        if x != "":
            tmp = False
            break
    return tmp


# 업로드한 파일인지 구분
def isUploadedFile(select_val):
    return True if select_val.split(".")[-1] == "csv" else False


# 보호속성 인덱스 찾기
def getAttributeIndex(data_sp, protect):
    try:
        return data_sp.index(protect[0]), data_sp.index(protect[2])
    except:
        print("errrrrrr", protect, data_sp)


# 보호속성의 지정 값 인덱스 찾기
def getAttributeValueIndex(new_data, attributeKey, protect):
    for idx, dl in enumerate(new_data):
        try:
            if dl[attributeKey[0]] == int(protect[1]):
                index1 = idx
                break
        except:
            if dl[attributeKey[0]] == protect[1]:
                index1 = idx
                break

    for idx, dl in enumerate(new_data):
        try:
            if dl[attributeKey[1]] == int(protect[3]):
                index2 = idx
                break
        except:
            if dl[attributeKey[1]] == protect[3]:
                index2 = idx
                break
    return index1, index2


# 보호속성 분류
def attributeFilter(new_data, attributeKey, attributeVal):
    attr1 = []
    attr2 = []

    new_data = new_data[:-1]

    num1 = new_data[attributeVal[0]][attributeKey[0]]
    num2 = new_data[attributeVal[1]][attributeKey[1]]

    for i in range(len(new_data)):
        if new_data[i][attributeKey[0]] == num1:
            attr1.append(1)
        else:
            attr1.append(0)

        if new_data[i][attributeKey[1]] == num2:
            attr2.append(1)
        else:
            attr2.append(0)

    return attr1, attr2
