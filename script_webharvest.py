
import parsel

import pandas as pd

import webharvest
from utils import Doc


lianjia_css_conf = Doc("./config/lianjia_html.json").get_js()

url_head, url_loc_dict, url_pg = Doc("./config/lianjia_url.json").get_js()


def parse_lianjia(html, css_conf):
    data = list()
    divs = webharvest.base_css(html, css_conf[0])
    for div in divs:
        data.append(webharvest.base_css_dict(div, css_conf[1]))
    return data


def main():
    for loc, url_loc in url_loc_dict.items():
        data_list = list()
        for i in range(1, 100):
            url = f"{url_head}{url_loc}{url_pg}{i}"
            html = webharvest.get_html(url)
            Doc(f"./data/html/{loc}.txt").log(html, split="\n*#*#split#*#*\n", istime=False)
            data = parse_lianjia(html, lianjia_css_conf)
            data_list.extend(data)
        data_pd = pd.DataFrame(data_list)
        data_pd.to_csv(f"./data/{loc}.csv")
        print(f"{loc}已获取完成")


if __name__ == "__main__":
    main()
