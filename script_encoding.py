
import os
import re

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from utils import shrink_list, separator


data_df = pd.read_csv("data/ori_data/温江.csv")

# print(data_df.info)
print(data_df.columns)
# print(data_df.describe())
# print(data_df.head())
print(data_df.dtypes)

# print(data_df["houseInfo"])
# split_df = data_df["houseInfo"].str.split("|", expand=True)
# print(split_df)
# print(type(split_df))
# split_df.columns = ["type", "size", "orientation", "decorate", "height", "year", "buildType"]
# print(split_df)
# print(split_df.info())


def try_eval(input_obj):
    try:
        output_obj = eval(input_obj)
    except:
        output_obj = input_obj
    return output_obj


def do_re(input_str, re_expression):
    pattern = re.compile(re_expression)
    output_str = pattern.findall(input_str)
    return output_str


def num_compose(lst):
    result = 0
    for i, num in enumerate(lst[::-1]):
        result += int(num) * (10 ** (3 * i))
    return result


def list_re_get(source_list):
    for source_str in source_list:
        if source_str.rstrip()[-1] == "年":
            return int(source_str.rstrip()[0:-1])


def _list_to_list_base_conf_dict(source_list, conf_dict, is_direct):
    if not isinstance(source_list, list):
        return None
    return_list = list()
    for source_str in source_list:
        for conf_key, conf_value in conf_dict.items():
            if not is_direct:
                if conf_key in source_str.split():
                    return_list.append(conf_value)
            else:
                if conf_key in source_str:
                    return_list.append(conf_value)
    return shrink_list(return_list)


def _list_to_dict_base_conf_list(source_list, conf_list):
    return_dict = {config: 0 for config in conf_list}
    for source_str in source_list:
        for conf in conf_list:
            if conf in source_str.split():
                return_dict[conf] = 1
    return return_dict


def try_astype(in_put, tp):
    try:
        return tp(in_put)
    except:
        return None


def series_list_to_base_conf(source_series, conf, is_direct=False):
    match conf:
        case dict():
            tem = source_series.apply(_list_to_list_base_conf_dict, conf_dict=conf, is_direct=is_direct)
            return tem
        case list():
            tem = source_series.apply(_list_to_dict_base_conf_list, conf_list=conf)
            tem = list(tem)
            return pd.DataFrame(tem)
        case _:
            raise TypeError


def list_index(string, index):
    if isinstance(string, str):
        lst = string.split(",")
        return float(lst[index])
    else:
        return None


def encoding(df_name):
    df = pd.read_csv(f"data/ori_data/{df_name}")
    # 名字
    separator("名字")
    ser_locateName = df["locateName"].apply(try_eval)
    df["locateName_0"] = ser_locateName.apply(lambda x: x[0])
    df["locateName_1"] = ser_locateName.apply(lambda x: x[1])
    print(df[["locateName_0", "locateName_1"]])

    # 总价 已有
    separator("总价")

    # 均价
    separator("均价")
    df["unitPrice"] = df["unitPrice"].astype(str).apply(do_re, re_expression=r"\d+").apply(num_compose)
    print(df["unitPrice"])

    # 面积
    separator("面积")
    df["houseSpace"] = df["totalPrice"].apply(try_astype, tp=float) / df["unitPrice"] * 10000
    print(df["houseSpace"])

    # info解析
    separator("info解析")
    separator("info解析")
    ser_houseInfo = df["houseInfo"].str.split("|")
    print(ser_houseInfo)

    # 方向
    separator("orientation")
    orientation_conf_dict = {"东": 0, "东北": 1, "北": 2, "西北": 3,
                             "西": 4, "西南": 5, "南": 6, "东南": 7}
    df["orientation"] = series_list_to_base_conf(ser_houseInfo, orientation_conf_dict)
    print(df["orientation"])

    # 方向 onehot
    separator("orientation onehot")
    orientation_conf_list = ['东', '东北', '北', '西北', '西', '西南', '南', '东南']
    df = df.join(series_list_to_base_conf(ser_houseInfo, orientation_conf_list))
    print(df[orientation_conf_list])
    orientation_onehot = {'东': "e", '东北': "ne", '北': "n", '西北': "nw",
                          '西': "w", '西南': "sw", '南': "s", '东南': "se"}
    df.rename(columns=orientation_onehot, inplace=True)

    # 装修情况
    separator("装修情况")
    fitment_conf_dict = {"毛胚": 1, "简装": 2, "精装": 3}
    df["fitment"] = series_list_to_base_conf(ser_houseInfo, fitment_conf_dict).fillna(0).astype(int)
    print(df["fitment"])

    # 装修情况 onehot
    separator("装修情况 onehot")
    fitment_conf_list = ["毛胚", "简装", "精装"]
    df = df.join(series_list_to_base_conf(ser_houseInfo, fitment_conf_list))

    # 楼层
    separator("楼层")
    floor_conf_dict = {"低": 1, "中": 2, "高": 3}
    df["houseFloor"] = series_list_to_base_conf(ser_houseInfo, floor_conf_dict, True).fillna(0).astype(int)
    print(df["houseFloor"])

    # 楼层 onehot
    separator("楼层 onehot")
    # floor_conf_list = ["低", "中", "高"]
    # df = df.join(series_list_to_base_conf(ser_houseInfo, floor_conf_list))
    floor_onehot = pd.get_dummies(df["houseFloor"], dtype=int).rename(columns={key: value for value, key in floor_conf_dict.items()})
    for name in floor_conf_dict:
        if name not in floor_onehot.columns:
            floor_onehot[name] = 0
    df = df.join(floor_onehot[[i for i in floor_conf_dict]])

    # houseStructure
    separator("houseStructure")
    houseStructure_conf_dict = {"塔楼": 1, "板楼": 2, "板塔结合": 3}
    df["houseStructure"] = series_list_to_base_conf(ser_houseInfo, houseStructure_conf_dict).fillna(0).astype(int)
    print(df["houseStructure"])

    # houseStructure onehot
    houseStructure_onehot = pd.get_dummies(df["houseStructure"], dtype=int).rename(columns={key: value for value, key in houseStructure_conf_dict.items()})
    for name in houseStructure_conf_dict:
        if name not in houseStructure_onehot.columns:
            houseStructure_onehot[name] = 0
    df = df.join(houseStructure_onehot[[i for i in houseStructure_conf_dict]])

    # buildTime
    separator("buildTime")
    df["buildTime"] = ser_houseInfo.apply(list_re_get)

    # tags解析
    separator("tags解析")
    separator("tags解析")
    ser_tags = df["tags"].apply(try_eval)

    # isNearSubway
    separator("isNearSubway")
    isNearSubway_conf_list = {"近地铁": 1}
    df["isNearSubway"] = series_list_to_base_conf(ser_tags, isNearSubway_conf_list).fillna(0).astype(int)
    print(df["isNearSubway"])

    # locate
    df_name = df_name.split(".")[0]
    print(df_name)
    locate_conf = pd.read_excel(f"./data/locate_map/map-location_{df_name}.xlsx")
    merge_df = df.merge(locate_conf, left_on="locateName_0", right_on="地址", how="left")
    print(merge_df.dtypes)
    merge_df["longitude"] = merge_df["经度,纬度"].apply(list_index, index=0)
    merge_df["latitude"] = merge_df["经度,纬度"].apply(list_index, index=1)

    df[["longitude", "latitude"]] = merge_df[["longitude", "latitude"]]

    separator("final")
    print(df.columns)
    print(df.head())


    return df


def main():
    df_names = os.listdir("data/ori_data/")
    data = list()
    for df_name in df_names:
        data.append(encoding(df_name))
    print(len(data))
    data = pd.concat(data)
    print(data.head())
    print(data.dtypes)
    # train_set, test_set = train_test_split(data, test_size=0.1, random_state=114514)
    # train_set.to_csv("./train.csv")
    # test_set.to_csv("./test.csv")


if __name__ == "__main__":
    main()
