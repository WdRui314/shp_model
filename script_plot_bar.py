
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./data/train.csv")

# 'Unnamed: 0.1', 'Unnamed: 0', 'title', 'locateName', 'totalPrice',
#        'unitPrice', 'houseInfo', 'followInfo', 'tags', 'url', 'locateName_0',
#        'locateName_1', 'houseSpace', '1orientation', 'e', 'ne', 'n', 'nw', 'w',
#        'sw', 's', 'se', '1fitment', '毛胚', '简装', '精装', '1houseFloor', '低', '中',
#        '高', '1houseStructure', '塔楼', '板楼', '板塔结合', 'buildTime', '1isNearSubway',
#        'longitude', 'latitude'],
#       dtype='object'


def get_first(lst):
    try:
        lst = json.loads(lst)
        match len(lst):
            case 0:
                return None
            case _:
                return lst[0]
    except:
        return None


def plot_bar(name, is_get_first=False):
    global df
    if is_get_first:
        df[name] = df[name].apply(get_first)
    df_tem = df[["unitPrice", name]]
    df_tem = df_tem.groupby(name).aggregate(np.mean)
    print(df_tem)
    plt.figure(figsize=(8, 8), dpi=80)
    df_tem.plot.bar(color="black", alpha=0.75)
    # plt.title(f"{name}-unitPrice", fontsize=15)
    plt.xlabel(name, fontsize=15)
    plt.ylabel("unitPrice-mean", fontsize=15)
    plt.savefig(f"./fig/bar_{name}-unitPrice")
    print(df_tem)



plot_bar("houseFloor")
plot_bar("fitment")
plot_bar("houseStructure")
plot_bar("isNearSubway")
plot_bar("orientation", is_get_first=True)
