from selenium import webdriver
import requests
import time
import os
from multiprocessing import Process

proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

def download_pic(url, pic_title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36 Edg/80.0.361.109'
    }
    retry_count = 1;
    pic_title = pic_title + '.jpg'
    while retry_count < 11:
        try:
            resp = requests.get(url = url, proxies=proxies, headers = headers, timeout = 30)
            with open('E:/pic/' + pic_title, 'wb') as f:
                f.write(resp.content)
            print("file " + pic_title + "done")
            break
        except:
            print("file " + pic_title + " download error, retry " + str(retry_count) + " times")
            time.sleep(1)
            continue

def filename_replace(filename):
    for str_illegal in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(str_illegal, '-')
    return filename

def start(start_page ,pid_target):
    print("process start, NO." + str(start_page) + " !")
    # 设置本地代理
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:1080")

    # executable_path是本地的ChromeDriver路径
    browser = webdriver.Chrome(chrome_options = chrome_options, executable_path="E:\chromedriver_win32\chromedriver.exe")
    browser.set_page_load_timeout(60)

    # 每一页中主题的Xpath路径
    xpath_list = []
    for i in range(11, 101):
        temp = '//*[@id="ajaxtable"]/tbody[2]/tr[' + str(i) + ']/td[2]/h3/a'
        xpath_list.append(temp)

    for i in range(start_page, 100, pid_target):
        while True:
            try:
                print("getting: NO. " + str(i) + " page")
                browser.get("http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i))
                print("NO." + str(i) + " page load successful, url: " + "http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i))
                break
            except:
                time.sleep(3)
                print("get url " + "http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i) + " failed,try again")
                continue
        for item in xpath_list:
            try:
                browser.find_element_by_xpath(item).click()
                n = browser.window_handles
                browser.switch_to.window(n[-1])
                print("getting url: " + str(browser.current_url) + " start...")
                img_list = browser.find_elements_by_tag_name("img")
                pic_title = filename_replace(browser.title)
                for i in range(len(img_list)):
                    download_pic(img_list[i].get_attribute('src'), pic_title + '(' + str(i) + ')')
                browser.close()
                browser.switch_to.window(n[0])
            except:
                browser.quit()
                continue
        browser.quit()

if __name__ == '__main__':
    p_1 = Process(target=start, args=(1, 8))
    p_2 = Process(target=start, args=(2, 8))
    p_3 = Process(target=start, args=(3, 8))
    p_4 = Process(target=start, args=(4, 8))
    p_5 = Process(target=start, args=(5, 8))
    p_6 = Process(target=start, args=(6, 8))
    p_7 = Process(target=start, args=(7, 8))
    p_8 = Process(target=start, args=(8, 8))
    p_1.start()
    p_2.start()
    p_3.start()
    p_4.start()
    p_5.start()
    p_6.start()
    p_7.start()
    p_8.start()
    p_1.join()
    p_2.join()
    p_3.join()
    p_4.join()
    p_5.join()
    p_6.join()
    p_7.join()
    p_8.join()