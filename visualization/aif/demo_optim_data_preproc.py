import sys

sys.path.append("../")
import numpy as np
from tqdm import tqdm

from aif360.datasets import BinaryLabelDataset

# from aif360.datasets import AdultDataset, GermanDataset, CompasDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.metrics import ClassificationMetric
from aif360.metrics.utils import compute_boolean_conditioning_vector

# from aif360.algorithms.preprocessing.optim_preproc import OptimPreproc

# from aif360.algorithms.preprocessing.optim_preproc_helpers.data_preproc_functions import (
#     load_preproc_data_adult,
#     load_preproc_data_german,
#     load_preproc_data_compas,
# )

# from aif360.algorithms.preprocessing.optim_preproc_helpers.distortion_functions import (
#     get_distortion_adult,
#     get_distortion_german,
#     get_distortion_compas,
# )
# from aif360.algorithms.preprocessing.optim_preproc_helpers.opt_tools import OptTools

from .common_utils import compute_metrics

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

from IPython.display import Markdown, display
import matplotlib.pyplot as plt

from .lib.data_preproc_functions import (
    load_preproc_data_adult,
    load_preproc_data_german,
    load_preproc_data_compas,
)
from .lib.distortion_functions import (
    get_distortion_adult,
    get_distortion_german,
    get_distortion_compas,
)

# 업로드 데이터 테스트
from .lib.data_preproc_custom import load_preproc_upload_data

from .lib.optim_helper.upload_distortion_functions import get_distortion_upload_data
from .lib.optim_helper.opt_tools import OptTools
from .lib.optim_helper.optim_preproc import OptimPreproc


class optim_pre:
    def Run(
        select_val,
        select_protect,
        protected_attribute_used,
        select_features,
        optim_val,
        label,
    ):
        result = []
        dataset_used = select_val

        if dataset_used == "adult":
            #     dataset_orig = AdultDataset()
            if protected_attribute_used == 1:
                privileged_groups = [{"sex": 1}]
                unprivileged_groups = [{"sex": 0}]
                dataset_orig = load_preproc_data_adult(["sex"])
            else:
                privileged_groups = [{"race": 1}]
                unprivileged_groups = [{"race": 0}]
                dataset_orig = load_preproc_data_adult(["race"])

            optim_options = {
                "distortion_fun": get_distortion_adult,
                "epsilon": 0.05,
                "clist": [0.99, 1.99, 2.99],
                "dlist": [0.1, 0.05, 0],
            }

        elif dataset_used == "german":
            #     dataset_orig = GermanDataset()
            if protected_attribute_used == 1:
                privileged_groups = [{"sex": 1}]
                unprivileged_groups = [{"sex": 0}]
                dataset_orig = load_preproc_data_german(["sex"])

                optim_options = {
                    "distortion_fun": get_distortion_german,
                    "epsilon": 0.05,
                    "clist": [0.99, 1.99, 2.99],
                    "dlist": [0.1, 0.05, 0],
                }

            else:
                privileged_groups = [{"age": 1}]
                unprivileged_groups = [{"age": 0}]
                dataset_orig = load_preproc_data_german(["age"])

                optim_options = {
                    "distortion_fun": get_distortion_german,
                    "epsilon": 0.1,
                    "clist": [0.99, 1.99, 2.99],
                    "dlist": [0.1, 0.05, 0],
                }

        elif dataset_used == "compas":
            #     dataset_orig = CompasDataset()
            if protected_attribute_used == 1:
                privileged_groups = [{"sex": 0}]
                unprivileged_groups = [{"sex": 1}]
                dataset_orig = load_preproc_data_compas(["sex"])
                # print("\n\n{}\n\n".format(dataset_orig[:10]))
            else:
                privileged_groups = [{"race": 1}]
                unprivileged_groups = [{"race": 0}]
                dataset_orig = load_preproc_data_compas(["race"])
                # print("\n\n{}\n\n".format(dataset_orig[:10]))

            optim_options = {
                "distortion_fun": get_distortion_compas,
                "epsilon": 0.05,
                "clist": [0.99, 1.99, 2.99],
                "dlist": [0.1, 0.05, 0],
            }

        else:
            msgtag = "demo_reweighing_preproc > Run, reweighing에서 preproc들어가기 전".split(
                ","
            )
            print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
            print(select_val, select_protect, select_features, label)
            print(
                "==========E : [{}]{}==========".format(msgtag[0], msgtag[1]),
                end="\n\n",
            )

            if protected_attribute_used:
                privileged_groups = [{select_protect[0]: 1}]
                unprivileged_groups = [{select_protect[0]: 0}]
                dataset_orig = load_preproc_upload_data(
                    select_val,
                    select_protect[0],
                    select_protect,
                    select_features,
                    optim_val,
                    label,
                )

                msgtag = "demo_reweighing_preproc > Run, reweighing에서 preproc해서 나온 dataset_orig 바로 출력".split(
                    ","
                )
                print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
                print(dataset_orig)
                print(
                    "==========E : [{}]{}==========".format(msgtag[0], msgtag[1]),
                    end="\n\n",
                )

            else:
                privileged_groups = [{select_protect[2]: 1}]
                unprivileged_groups = [{select_protect[2]: 0}]
                dataset_orig = load_preproc_upload_data(
                    select_val,
                    select_protect[2],
                    select_protect,
                    select_features,
                    optim_val,
                    label,
                )
                msgtag = "demo_reweighing_preproc > Run, reweighing에서 preproc해서 나온 dataset_orig 바로 출력".split(
                    ","
                )
                print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
                print(dataset_orig)
                print(
                    "==========E : [{}]{}==========".format(msgtag[0], msgtag[1]),
                    end="\n\n",
                )

            optim_options = {
                "distortion_fun": get_distortion_upload_data,
                "epsilon": 0.05,
                "clist": [0.99, 1.99, 2.99],
                "dlist": [0.1, 0.05, 0],
            }

        # random seed
        np.random.seed(1)

        # Split into train, validation, and test
        dataset_orig_train, dataset_orig_vt = dataset_orig.split([0.7], shuffle=True)
        dataset_orig_valid, dataset_orig_test = dataset_orig_vt.split(
            [0.5], shuffle=True
        )

        # print out some labels, names, etc.
        display(Markdown("#### Training Dataset shape"))
        print(dataset_orig_train.features.shape)
        display(Markdown("#### Favorable and unfavorable labels"))
        print(dataset_orig_train.favorable_label, dataset_orig_train.unfavorable_label)
        display(Markdown("#### Protected attribute names"))
        print(dataset_orig_train.protected_attribute_names)
        display(Markdown("#### Privileged and unprivileged protected attribute values"))
        print(
            dataset_orig_train.privileged_protected_attributes,
            dataset_orig_train.unprivileged_protected_attributes,
        )
        display(Markdown("#### Dataset feature names"))
        print(dataset_orig_train.feature_names)

        # Metric for the original dataset
        metric_orig_train = BinaryLabelDatasetMetric(
            dataset_orig_train,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups,
        )
        display(Markdown("#### Original training dataset"))
        print(
            "Difference in mean outcomes between unprivileged and privileged groups = %f"
            % metric_orig_train.mean_difference()
        )

        OP = OptimPreproc(
            OptTools,
            optim_options,
            select_val,
            select_protect,
            select_features,
            optim_val,
            label,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups,
        )

        OP = OP.fit(dataset_orig_train)

        # Transform training data and align features
        dataset_transf_train = OP.transform(dataset_orig_train, transform_Y=True)
        dataset_transf_train = dataset_orig_train.align_datasets(dataset_transf_train)

        metric_transf_train = BinaryLabelDatasetMetric(
            dataset_transf_train,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups,
        )
        display(Markdown("#### Transformed training dataset"))
        print(
            "Difference in mean outcomes between unprivileged and privileged groups = %f"
            % metric_transf_train.mean_difference()
        )

        ### Testing
        assert np.abs(metric_transf_train.mean_difference()) < np.abs(
            metric_orig_train.mean_difference()
        )

        dataset_orig_test = dataset_transf_train.align_datasets(dataset_orig_test)
        display(Markdown("#### Testing Dataset shape"))
        print(dataset_orig_test.features.shape)

        metric_orig_test = BinaryLabelDatasetMetric(
            dataset_orig_test,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups,
        )
        display(Markdown("#### Original test dataset"))
        print(
            "Difference in mean outcomes between unprivileged and privileged groups = %f"
            % metric_orig_test.mean_difference()
        )

        dataset_transf_test = OP.transform(dataset_orig_test, transform_Y=True)
        dataset_transf_test = dataset_orig_test.align_datasets(dataset_transf_test)

        metric_transf_test = BinaryLabelDatasetMetric(
            dataset_transf_test,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups,
        )
        display(Markdown("#### Transformed test dataset"))
        print(
            "Difference in mean outcomes between unprivileged and privileged groups = %f"
            % metric_transf_test.mean_difference()
        )

        ### Testing
        assert np.abs(metric_transf_test.mean_difference()) < np.abs(
            metric_orig_test.mean_difference()
        )

        # Logistic regression classifier and predictions
        scale_orig = StandardScaler()
        X_train = scale_orig.fit_transform(dataset_orig_train.features)
        y_train = dataset_orig_train.labels.ravel()

        lmod = LogisticRegression()
        lmod.fit(X_train, y_train)
        y_train_pred = lmod.predict(X_train)

        # positive class index
        pos_ind = np.where(lmod.classes_ == dataset_orig_train.favorable_label)[0][0]

        dataset_orig_train_pred = dataset_orig_train.copy()
        dataset_orig_train_pred.labels = y_train_pred

        dataset_orig_valid_pred = dataset_orig_valid.copy(deepcopy=True)
        X_valid = scale_orig.transform(dataset_orig_valid_pred.features)
        y_valid = dataset_orig_valid_pred.labels
        dataset_orig_valid_pred.scores = lmod.predict_proba(X_valid)[
            :, pos_ind
        ].reshape(-1, 1)

        dataset_orig_test_pred = dataset_orig_test.copy(deepcopy=True)
        X_test = scale_orig.transform(dataset_orig_test_pred.features)
        y_test = dataset_orig_test_pred.labels
        dataset_orig_test_pred.scores = lmod.predict_proba(X_test)[:, pos_ind].reshape(
            -1, 1
        )

        num_thresh = 100
        ba_arr = np.zeros(num_thresh)
        class_thresh_arr = np.linspace(0.01, 0.99, num_thresh)
        for idx, class_thresh in enumerate(class_thresh_arr):

            fav_inds = dataset_orig_valid_pred.scores > class_thresh
            dataset_orig_valid_pred.labels[
                fav_inds
            ] = dataset_orig_valid_pred.favorable_label
            dataset_orig_valid_pred.labels[
                ~fav_inds
            ] = dataset_orig_valid_pred.unfavorable_label

            classified_metric_orig_valid = ClassificationMetric(
                dataset_orig_valid,
                dataset_orig_valid_pred,
                unprivileged_groups=unprivileged_groups,
                privileged_groups=privileged_groups,
            )

            ba_arr[idx] = 0.5 * (
                classified_metric_orig_valid.true_positive_rate()
                + classified_metric_orig_valid.true_negative_rate()
            )

        best_ind = np.where(ba_arr == np.max(ba_arr))[0][0]
        best_class_thresh = class_thresh_arr[best_ind]

        print(
            "Best balanced accuracy (no fairness constraints) = %.4f" % np.max(ba_arr)
        )
        print(
            "Optimal classification threshold (no fairness constraints) = %.4f"
            % best_class_thresh
        )

        display(Markdown("#### Predictions from original testing data"))

        bal_acc_arr_orig = []
        disp_imp_arr_orig = []
        avg_odds_diff_arr_orig = []

        display(Markdown("#### Testing set"))
        display(Markdown("##### Raw predictions - No fairness constraints"))

        for thresh in tqdm(class_thresh_arr):
            if thresh == best_class_thresh:
                disp = True
            else:
                disp = False

            fav_inds = dataset_orig_test_pred.scores > thresh
            dataset_orig_test_pred.labels[
                fav_inds
            ] = dataset_orig_test_pred.favorable_label
            dataset_orig_test_pred.labels[
                ~fav_inds
            ] = dataset_orig_test_pred.unfavorable_label

            metric_test_bef = compute_metrics(
                dataset_orig_test,
                dataset_orig_test_pred,
                unprivileged_groups,
                privileged_groups,
                disp=disp,
            )

            bal_acc_arr_orig.append(metric_test_bef["Balanced accuracy"])
            avg_odds_diff_arr_orig.append(metric_test_bef["Average odds difference"])
            disp_imp_arr_orig.append(metric_test_bef["Disparate impact"])

            if disp:
                balAcc_before = metric_test_bef["Balanced accuracy"]
                # result.append(metric_test_bef["Balanced accuracy"])
                result.append(metric_test_bef["Statistical parity difference"])
                result.append(metric_test_bef["Disparate impact"])
                result.append(metric_test_bef["Equal opportunity difference"])
                result.append(metric_test_bef["Average odds difference"])
                result.append(metric_test_bef["Theil index"])

        # fig, ax1 = plt.subplots(figsize=(10,7))
        # ax1.plot(class_thresh_arr, bal_acc_arr_orig)
        # ax1.set_xlabel('Classification Thresholds', fontsize=16, fontweight='bold')
        # ax1.set_ylabel('Balanced Accuracy', color='b', fontsize=16, fontweight='bold')
        # ax1.xaxis.set_tick_params(labelsize=14)
        # ax1.yaxis.set_tick_params(labelsize=14)

        # ax2 = ax1.twinx()
        # ax2.plot(class_thresh_arr, np.abs(1.0-np.array(disp_imp_arr_orig)), color='r')
        # ax2.set_ylabel('abs(1-disparate impact)', color='r', fontsize=16, fontweight='bold')
        # ax2.axvline(np.array(class_thresh_arr)[best_ind],
        #             color='k', linestyle=':')
        # ax2.yaxis.set_tick_params(labelsize=14)
        # ax2.grid(True)

        disp_imp_at_best_bal_acc_orig = np.abs(1.0 - np.array(disp_imp_arr_orig))[
            best_ind
        ]

        scale_transf = StandardScaler()
        X_train = scale_transf.fit_transform(dataset_transf_train.features)
        y_train = dataset_transf_train.labels.ravel()

        lmod = LogisticRegression()
        lmod.fit(X_train, y_train)
        y_train_pred = lmod.predict(X_train)

        dataset_transf_train_pred = dataset_transf_train.copy()
        dataset_transf_train_pred.labels = y_train_pred

        dataset_transf_test_pred = dataset_transf_test.copy(deepcopy=True)
        X_test = scale_transf.transform(dataset_transf_test_pred.features)
        y_test = dataset_transf_test_pred.labels
        dataset_transf_test_pred.scores = lmod.predict_proba(X_test)[
            :, pos_ind
        ].reshape(-1, 1)

        display(Markdown("#### Predictions from transformed testing data"))

        bal_acc_arr_transf = []
        disp_imp_arr_transf = []
        avg_odds_diff_arr_transf = []

        display(Markdown("#### Testing set"))
        display(Markdown("##### Transformed predictions - No fairness constraints"))

        for thresh in tqdm(class_thresh_arr):
            if thresh == best_class_thresh:
                disp = True
            else:
                disp = False
            fav_inds = dataset_transf_test_pred.scores > thresh
            dataset_transf_test_pred.labels[
                fav_inds
            ] = dataset_transf_test_pred.favorable_label
            dataset_transf_test_pred.labels[
                ~fav_inds
            ] = dataset_transf_test_pred.unfavorable_label

            metric_test_aft = compute_metrics(
                dataset_transf_test,
                dataset_transf_test_pred,
                unprivileged_groups,
                privileged_groups,
                disp=disp,
            )

            bal_acc_arr_transf.append(metric_test_bef["Balanced accuracy"])
            avg_odds_diff_arr_transf.append(metric_test_bef["Average odds difference"])
            disp_imp_arr_transf.append(metric_test_bef["Disparate impact"])

            if disp:
                balAcc_after = metric_test_aft["Balanced accuracy"]
                result.append(metric_test_aft["Statistical parity difference"])
                result.append(metric_test_aft["Disparate impact"])
                result.append(metric_test_aft["Equal opportunity difference"])
                result.append(metric_test_aft["Average odds difference"])
                result.append(metric_test_aft["Theil index"])

        # fig, ax1 = plt.subplots(figsize=(10,7))
        # ax1.plot(class_thresh_arr, bal_acc_arr_transf)
        # ax1.set_xlabel('Classification Thresholds', fontsize=16, fontweight='bold')
        # ax1.set_ylabel('Balanced Accuracy', color='b', fontsize=16, fontweight='bold')
        # ax1.xaxis.set_tick_params(labelsize=14)
        # ax1.yaxis.set_tick_params(labelsize=14)

        # ax2 = ax1.twinx()
        # ax2.plot(class_thresh_arr, np.abs(1.0-np.array(disp_imp_arr_transf)), color='r')
        # ax2.set_ylabel('abs(1-disparate impact)', color='r', fontsize=16, fontweight='bold')
        # ax2.axvline(np.array(class_thresh_arr)[best_ind],
        #             color='k', linestyle=':')
        # ax2.yaxis.set_tick_params(labelsize=14)
        # ax2.grid(True)

        # disp_imp_at_best_bal_acc_transf = np.abs(1.0-np.array(disp_imp_arr_transf))[best_ind]

        # ### testing
        # assert disp_imp_at_best_bal_acc_transf < disp_imp_at_best_bal_acc_orig

        result.append(balAcc_before)
        result.append(balAcc_after)
        return result

