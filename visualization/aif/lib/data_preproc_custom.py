# from aif360.datasets import AdultDataset, GermanDataset, CompasDataset
from .upload_dataset import UploadDataset

import pandas as pd
import numpy as np
import math

import sys


def isnum(x):
    return (type(x) == str and x.isdigit()) or (
        (
            type(x) == float
            or type(x) == int
            or type(x) == np.int64
            or type(x) == np.float64
        )
        and not math.isnan(x)
    )


def load_preproc_upload_data(
    file_name=None,
    protected_attributes=None,
    protected_key_val=None,
    select_features=None,
    optim_val=None,
    label=None,
):
    def custom_preprocessing(df):
        # import math

        df = df[select_features]

        msgtag = "data_preproc_custom > custom_preprocessing, custom_preprocessing안에서 전처리 할 값들과 전처리 전 df".split(
            ","
        )
        print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
        print(protected_key_val, label)
        print(df)
        print(df[:20])
        print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

        def conv_val(x, protect_val):
            if x == protect_val:
                return 1.0
            else:
                return 0.0

        def conv_label_str(x, sel_label):
            if x == sel_label:
                return 1
            else:
                return 0

        def conv_label_num(x, sel_label):
            if math.isnan(x):
                return 0
            if label[-1] == ">":
                if x > sel_label:
                    return 1
                else:
                    return 0
            elif label[-1] == ">=":
                if x >= sel_label:
                    return 1
                else:
                    return 0
            elif label[-1] == "=":
                if x == sel_label:
                    return 1
                else:
                    return 0
            elif label[-1] == "<=":
                if x <= sel_label:
                    return 1
                else:
                    return 0
            elif label[-1] == "<":
                if x < sel_label:
                    return 1
                else:
                    return 0

        def conv_str2num(x):
            if math.isnan(x):
                return 0
            if isnum(x):
                return float(x)
            else:
                return x

        def conv_optim_str(x, sel_item):
            if x == sel_item:
                return sel_item[0] + "=" + sel_item[1]
            else:
                return sel_item[0] + "!=" + sel_item[1]

        def conv_optim_num(x, sel_item):
            if math.isnan(x):
                return math.nan
            if sel_item[-1] == ">":
                if x > sel_item[1]:
                    return str(sel_item[0]) + str(sel_item[2]) + str(sel_item[1])
                else:
                    return str(sel_item[0]) + "!=" + str(sel_item[1])
            elif sel_item[-1] == ">=":
                if x >= sel_item[1]:
                    return str(sel_item[0]) + str(sel_item[2]) + str(sel_item[1])
                else:
                    return str(sel_item[0]) + "!=" + str(sel_item[1])
            elif sel_item[-1] == "=":
                if x == sel_item[1]:
                    return str(sel_item[0]) + str(sel_item[2]) + str(sel_item[1])
                else:
                    return str(sel_item[0]) + "!=" + str(sel_item[1])
            elif sel_item[-1] == "<=":
                if x <= sel_item[1]:
                    return str(sel_item[0]) + str(sel_item[2]) + str(sel_item[1])
                else:
                    return str(sel_item[0]) + "!=" + str(sel_item[1])
            elif sel_item[-1] == "<":
                if x < sel_item[1]:
                    return str(sel_item[0]) + str(sel_item[2]) + str(sel_item[1])
                else:
                    return str(sel_item[0]) + "!=" + str(sel_item[1])

        df[protected_key_val[0]] = df[protected_key_val[0]].apply(
            lambda x: conv_val(x, protected_key_val[1])
        )
        df[protected_key_val[2]] = df[protected_key_val[2]].apply(
            lambda x: conv_val(x, protected_key_val[3])
        )

        if isnum(label[1]):
            df[label[0]] = df[label[0]].apply(lambda x: conv_label_num(x, label[1]))
        else:
            df[label[0]] = df[label[0]].apply(lambda x: conv_label_str(x, label[1]))

        for optim_item in optim_val:
            if isnum(optim_item[1]):
                df[optim_item[0]] = df[optim_item[0]].apply(
                    lambda x: conv_optim_num(x, optim_item)
                )
            else:
                df[optim_item[0]] = df[optim_item[0]].apply(
                    lambda x: conv_optim_str(x, optim_item)
                )

        msgtag = "data_preproc_custom > custom_preprocessing, custom_preprocessing안에서 전처리 후 df, df의 label의 종류".split(
            ","
        )
        print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
        print(df)
        print(df[:20])
        print(set(df[label[0]]))
        print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

        return df

    msgtag = "data_preproc_custom > custom_preprocessing, preproc에 들어와서 받은 인자 출력".split(
        ","
    )
    print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
    print(file_name, protected_attributes, protected_key_val, select_features, label)
    print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

    XD_features = (
        select_features[: select_features.index(label[0])]
        + select_features[select_features.index(label[0]) + 1 :]
    )

    # 보호속성 있으면 그대로 사용
    D_features = [protected_attributes]
    Y_features = [label[0]]

    # 선택 속성에서 보호속성 제거
    X_features = list(set(XD_features) - set(D_features))

    categorical_features = list(set(XD_features) - set(protected_key_val[0::2]))

    # privileged classes
    all_privileged_classes = {
        protected_key_val[0]: [1.0],
        protected_key_val[2]: [1.0],
    }

    # protected attribute maps
    all_protected_attribute_maps = {
        protected_key_val[0]: {0.0: "other", 1.0: protected_key_val[1]},
        protected_key_val[2]: {1.0: protected_key_val[3], 0.0: "other"},
    }

    msgtag = "data_preproc_custom > 바로출력, preproc 에서 받은 값으로 uploadData에 넘기는 값들".split(
        ","
    )
    print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
    print(
        file_name, XD_features, D_features, Y_features, X_features, categorical_features
    )
    print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

    return UploadDataset(
        file_name=file_name,
        label_name=Y_features[0],
        favorable_classes=[0],
        protected_attribute_names=D_features,
        privileged_classes=[all_privileged_classes[x] for x in D_features],
        instance_weights_name=None,
        categorical_features=categorical_features,
        features_to_keep=X_features + Y_features + D_features,
        na_values=[],
        metadata={
            "label_maps": [{1.0: label[1], 0.0: (0 if isnum(label[1]) else "other")}],
            "protected_attribute_maps": [
                all_protected_attribute_maps[x] for x in D_features
            ],
        },
        custom_preprocessing=custom_preprocessing,
    )


# def label_preproc(label):
#     if label[-1] == '>':

#     elif label[-1] == '>=':

#     elif label[-1] == '<=':

#     elif label[-1] == '<':

#     else:


# default_mappings = {
#       "label_maps": [{1.0: "Copy", 0.0: "New"}],
#       "protected_attribute_maps": [
#           {0.0: "other", 1.0: "Female"},
#           {1.0: "Single", 0.0: "other"},
#       ],
#     }
