import os

import pandas as pd

from aif360.datasets import StandardDataset

# from .selected_dataset import Selected_dataset
default_mappings = {
    "label_maps": [{1.0: "Copy", 0.0: "New"}],
    "protected_attribute_maps": [
        {0.0: "other", 1.0: "Female"},
        {1.0: "Single", 0.0: "other"},
    ],
}


# def default_preprocessing(df):
#     """Perform the same preprocessing as the original analysis:
#     https://github.com/propublica/compas-analysis/blob/master/Compas%20Analysis.ipynb
#     """
#     return df[
#         (df.days_b_screening_arrest <= 30)
#         & (df.days_b_screening_arrest >= -30)
#         & (df.is_recid != -1)
#         & (df.c_charge_degree != "O")
#         & (df.score_text != "N/A")
#     ]


class UploadDataset(StandardDataset):
    def __init__(
        self,
        file_name=None,
        label_name=None,
        favorable_classes=[0],
        protected_attribute_names=None,
        privileged_classes=None,
        instance_weights_name=None,
        categorical_features=None,
        features_to_keep=None,
        features_to_drop=[],
        na_values=[],
        custom_preprocessing=None,
        metadata=default_mappings,
    ):

        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "..",
            "..",
            "data",
            file_name,
        )

        msgtag = "upload_dataset > init, preproc에서 받은 인자들 출력".split(",")
        print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
        print(
            file_name,
            label_name,
            protected_attribute_names,
            privileged_classes,
            categorical_features,
            features_to_keep,
            metadata,
        )
        print("==========E : [{}]{}==========".format(msgtag[0], msgtag[1]), end="\n\n")

        try:
            df = pd.read_csv(filepath, na_values=na_values)

            msgtag = "upload_dataset > init, csv 파일을 upload_dataset에서 읽은 직후 바로 df 출력".split(
                ","
            )
            print("\n\n----------S : [{}]{}----------".format(msgtag[0], msgtag[1]))
            print(df)
            print(df[:20])
            print("metadata : ", metadata)
            print(
                "==========E : [{}]{}==========".format(msgtag[0], msgtag[1]),
                end="\n\n",
            )

        except IOError as err:
            print("IOError: {}".format(err))
            print("To use this class, please download the following file:")
            print(
                "\n\thttps://raw.githubusercontent.com/propublica/compas-analysis/master/compas-scores-two-years.csv"
            )
            print("\nand place it, as-is, in the folder:")
            print(
                "\n\t{}\n".format(
                    os.path.abspath(
                        os.path.join(
                            os.path.abspath(__file__),
                            "..",
                            "..",
                            "data",
                            "raw",
                            "compas",
                        )
                    )
                )
            )
            import sys

            sys.exit(1)

        super(UploadDataset, self).__init__(
            df=df,
            label_name=label_name,
            favorable_classes=favorable_classes,
            protected_attribute_names=protected_attribute_names,
            privileged_classes=privileged_classes,
            instance_weights_name=instance_weights_name,
            categorical_features=categorical_features,
            features_to_keep=features_to_keep,
            features_to_drop=features_to_drop,
            na_values=na_values,
            custom_preprocessing=custom_preprocessing,
            metadata=metadata,
        )
