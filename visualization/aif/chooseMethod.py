import sys
sys.path.append("../")
import numpy as np
from tqdm import tqdm

from aif360.datasets import BinaryLabelDataset
from aif360.datasets import AdultDataset, GermanDataset, CompasDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.metrics import ClassificationMetric
from aif360.algorithms.preprocessing.optim_preproc_helpers.data_preproc_functions        import load_preproc_data_adult, load_preproc_data_german, load_preproc_data_compas
from sklearn.metrics import accuracy_score
from common_utils import compute_metrics

from demo_adversarial_debiasing import ad_debiasing
from demo_reject_option_classification import rej_option_classification
from demo_reweighing_preproc import reweighing_pre
import tensorflow as tf


result_before = []
result_after = []
#result_after = reweighing_pre.Run(0, 0)

result_before = ad_debiasing.Run_before(0, 0)
result_after = ad_debiasing.Run_after(0, 0)



print("before")
for i in range(0,len(result_before)):
    print(result_before[i])

print("after")
for i in range(0,len(result_after)):
    print(result_after[i])


class simulator:
    result_before = []
    result_after = []
    def Run_before(datatype):
        if datatype == 0:
            print("adult")
        elif datatype == 1:
            print("german")
        elif datatype == 2:
            print("compas")

    def Run(methodType, dataType, protected_attribute_used):
        if methodType == 0: #debiasing
            result_before = ad_debiasing.Run_before(dataType, protected_attribute_used)
            result_after = ad_debiasing.Run_after(dataType, protected_attribute_used)
        elif methodType == 1: #reject
            result_after = rej_option_classification.Run(dataType, protected_attribute_used)
        elif methodType == 2: #reweighing
            result_after = reweighing_pre.Run(dataType, protected_attribute_used)



#rej_option_classification.Run(0,0)

