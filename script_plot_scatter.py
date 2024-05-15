
import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("./data/train.csv")

y = df["unitPrice"]

# longitude_center = df["longitude"].mean()
# latitude_center = df["latitude"].mean()

id = df["unitPrice"].argmax()
longitude_center = df.iloc[id]["longitude"]
latitude_center = df.iloc[id]["latitude"]

df["distanceToCenter"] = (df["longitude"]-longitude_center)**2 + (df["latitude"]-latitude_center)**2
df["distanceToCenter"] = df["distanceToCenter"].values ** (1/2)


# 'Unnamed: 0.1', 'Unnamed: 0', 'title', 'locateName', 'totalPrice',
#        'unitPrice', 'houseInfo', 'followInfo', 'tags', 'url', 'locateName_0',
#        'locateName_1', 'houseSpace', '1orientation', 'e', 'ne', 'n', 'nw', 'w',
#        'sw', 's', 'se', '1fitment', '毛胚', '简装', '精装', '1houseFloor', '低', '中',
#        '高', '1houseStructure', '塔楼', '板楼', '板塔结合', 'buildTime', '1isNearSubway',
#        'longitude', 'latitude'],
#       dtype='object'


def plt_scatter(name, islog=False, is_drop=False):
    global y, df
    df_tem = df.copy()
    in_y = y.values.copy()
    if islog:
        in_y = np.log(in_y)
    if is_drop:
        df_tem = df_tem[df_tem["buildTime"] > 1980]
        in_y = df_tem["unitPrice"]
    plt.figure(figsize=(8, 8))
    plt.scatter(df_tem[name].values, in_y, color="black", alpha=0.75, s=5)
    # plt.title(f"{name}-unitPrice", fontsize=15)
    plt.xlabel(name, fontsize=15)
    plt.ylabel("unitPrice", fontsize=15)
    plt.savefig(f"./fig/scatter_{name}-unitPrice.jpg")


plt_scatter("houseSpace")
plt_scatter("longitude")
plt_scatter("latitude")
plt_scatter("distanceToCenter")
plt_scatter("buildTime", is_drop=True)
