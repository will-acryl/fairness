import numpy as np
import pandas as pd
import math


def numberTest(value):
    return list(map(lambda x: float(x) if x.isdigit() else x, value))


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


def get_distortion_upload_data(
    vold, vnew, select_protected, select_features, optim_val, label
):
    distort = {}

    distort[select_protected[0]] = pd.DataFrame(
        {0: [0.0, 2.0], 1: [2.0, 0.0]}, index=[0, 1]
    )

    distort[select_protected[2]] = pd.DataFrame(
        {0: [0.0, 2.0], 1: [2.0, 0.0]}, index=[0, 1]
    )

    # distort[select_protected[0]] = pd.DataFrame(
    #     {
    #         select_protected[0] + "=" + str(select_protected[1]): [0.0, 2.0],
    #         select_protected[0] + "!=" + str(select_protected[1]): [2.0, 0.0],
    #     },
    #     index=[
    #         select_protected[0] + "=" + str(select_protected[1]),
    #         select_protected[0] + "!=" + str(select_protected[1]),
    #     ],
    # )

    # feature convert
    for item in optim_val:
        distort[item[0]] = pd.DataFrame(
            {
                item[0] + item[2] + str(item[1]): [0.0, 2.0],
                item[0] + "!=" + str(item[1]): [2.0, 0.0],
            },
            index=[item[0] + item[2] + str(item[1]), item[0] + "!=" + str(item[1]),],
        )

    if isnum(label[1]):
        distort[label[0]] = pd.DataFrame({0: [0.0, 2.0], 1: [2.0, 0.0]}, index=[0, 1])
    else:
        distort[label[0]] = pd.DataFrame(
            {"other": [0.0, 2.0], label[1]: [2.0, 0.0]}, index=["other", label[1]]
        )

    # distort[label[0]] = pd.DataFrame(
    #     {
    #         label[0] + label[2] + str(label[1]): [0.0, 2.0],
    #         label[0] + "!=" + str(label[1]): [0.0, 2.0],
    #     },
    #     index=[label[0] + label[2] + str(label[1]), label[0] + "!=" + str(label[1]),],
    # )

    total_cost = 0.0
    for k in vold:
        if k in vnew:
            total_cost += float(distort[k].loc[vnew[k], vold[k]])

    return total_cost


def get_distortion_compas(vold, vnew):
    distort = {}
    distort["two_year_recid"] = pd.DataFrame(
        {"No recid.": [0.0, 2.0], "Did recid.": [2.0, 0.0]},
        index=["No recid.", "Did recid."],
    )
    distort["age_cat"] = pd.DataFrame(
        {
            "Less than 25": [0.0, 1.0, 2.0],
            "25 to 45": [1.0, 0.0, 1.0],
            "Greater than 45": [2.0, 1.0, 0.0],
        },
        index=["Less than 25", "25 to 45", "Greater than 45"],
    )
    distort["c_charge_degree"] = pd.DataFrame(
        {"M": [0.0, 2.0], "F": [1.0, 0.0]}, index=["M", "F"]
    )
    distort["priors_count"] = pd.DataFrame(
        {
            "0": [0.0, 1.0, 2.0],
            "1 to 3": [1.0, 0.0, 1.0],
            "More than 3": [2.0, 1.0, 0.0],
        },
        index=["0", "1 to 3", "More than 3"],
    )
    distort["sex"] = pd.DataFrame({0.0: [0.0, 2.0], 1.0: [2.0, 0.0]}, index=[0.0, 1.0])
    distort["race"] = pd.DataFrame({0.0: [0.0, 2.0], 1.0: [2.0, 0.0]}, index=[0.0, 1.0])

    total_cost = 0.0
    for k in vold:
        if k in vnew:
            total_cost += distort[k].loc[vnew[k], vold[k]]

    return total_cost
