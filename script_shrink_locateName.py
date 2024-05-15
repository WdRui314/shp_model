
import os
import pandas as pd
import numpy as np

csv_list = os.listdir("./data")
print(csv_list)


def get_list_index(lst):
    lst = eval(lst)
    return lst[0]


for csv_path in csv_list:
    locateName = list()
    if csv_path[-3:-1] == "cs":
        print(csv_path)
        df = pd.read_csv(f"./data/{csv_path}")
        try:
            df["locateName_0"] = df["locateName"].apply(get_list_index)
            series_unique = df["locateName_0"].unique()
            series_unique = pd.Series(series_unique)
            series_unique.to_csv(f"./data/locatePath/locateName_{csv_path}")
        except:
            print("fail")
            continue
