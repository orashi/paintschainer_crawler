# decoding=utf-8
import logging
import os
import time

import requests
from selenium import webdriver

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s] - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


session = requests.session()

input_files = ["/home/orashi/桌面/3307FAB48F237E5A26F426F09E6B5ACA_1520239305621_out.png", "/home/orashi/桌面/A59D58E6224FD4117E6CC191899E65B1_1520929421000_out.png", "/home/orashi/桌面/9D24ECFD08202E76850700B9DC05FB19_1520191627767_out.png","/home/orashi/桌面/11838367_p0.jpg"]
output_path = "/home/orashi/桌面/crawlerd"

driver = webdriver.Chrome('/home/orashi/spsofts/chromedriver')
#脚本要与asd.html 同一目录
driver.get("http://paintschainer.preferred.tech/index_zh.html")
#定位上传按钮，添加本地文件 info-button
driver.find_element_by_id('info-button').click()


if len(input_files) <= 1:
    print("missing input_files")
    exit(-1)

time.sleep(10)

for input_file in input_files:
    try:
        driver.find_element_by_id("upload-button").send_keys(input_file)
        time.sleep(2)
        while True:
            try:
                draft = driver.find_element_by_css_selector(".painted_section__pictureDraft--V-q7w")
            except Exception as e:
                # print(Exception, e)
                break
        url = driver.find_element_by_id("paintedImage").get_property("src")

        print("input_file:{}".format(input_file))
        print("canna")
        r = session.get(url=url)
        with open(os.path.join(output_path, "canna", os.path.split(input_file)[1]), "wb") as binary:
            binary.write(r.content)

        for mode in ["satsuki", "tanpopo"]:
            driver.execute_script('$("input[value={}]").click()'.format(mode))
            while True:
                try:
                    draft = driver.find_element_by_css_selector(".painted_section__pictureDraft--V-q7w")
                except Exception as e:
                    # print(Exception, e)
                    break
            new_url = driver.find_element_by_id("paintedImage").get_property("src")
            print(mode)
            r = session.get(url=new_url)
            with open(os.path.join(output_path, mode, os.path.split(input_file)[1]), "wb") as binary:
                binary.write(r.content)
            url = new_url

    except Exception as e:
        logger.exception(e)


# time.sleep(10)
# driver.quit()
