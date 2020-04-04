from selenium import webdriver
import requests
import time
from multiprocessing import Process
import myLog
import sys
from multiprocessing import Pool

proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

def download_pic(url, pic_title, log_instance):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36 Edg/80.0.361.109'
    }
    retry_count = 1
    pic_title = pic_title + '.jpg'
    while retry_count < 11:
        try:
            resp = requests.get(url = url, proxies=proxies, headers = headers, timeout = 30)
            with open('E:/pic/' + pic_title, 'wb') as f:
                f.write(resp.content)
            log_instance.write_log(get_runtime_msg() + "file " + pic_title + "done")
            break
        except:
            log_instance.write_log(get_runtime_msg('error') + "file " + pic_title + " download error, retry " + str(retry_count) + " times")
            time.sleep(1)
            continue

def filename_replace(filename):
    for str_illegal in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(str_illegal, '-')
    return filename

def get_runtime_msg(flag = ''):
    if flag == '':
        msg = "[" + sys._getframe().f_back.f_code.co_filename + " " + str(sys._getframe().f_back.f_lineno) + "] [DEBUG] "
        return msg
    elif flag == 'error':
        msg = "[" + sys._getframe().f_back.f_code.co_filename + " " + str(sys._getframe().f_back.f_lineno) + "] [ERROR] "
        return msg

def start(start_page ,pid_target):
    log_instance = myLog.my_Log()
    log_instance.write_log(get_runtime_msg() + "process start, NO." + str(start_page) + " !")
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
                log_instance.write_log(get_runtime_msg() + "getting: NO. " + str(i) + " page")
                browser.get("http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i))
                log_instance.write_log(get_runtime_msg() + "NO." + str(i) + " page load successful, url: " + "http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i))
                break
            except:
                time.sleep(3)
                log_instance.write_log(get_runtime_msg('error') + "get url " + "http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i) + " failed,try again")
                continue
        for item in xpath_list:
            try:
                browser.find_element_by_xpath(item).click()
                n = browser.window_handles
                browser.switch_to.window(n[-1])
                log_instance.write_log(get_runtime_msg() + "getting url: " + str(browser.current_url) + " start...")
                img_list = browser.find_elements_by_tag_name("img")
                pic_title = filename_replace(browser.title)
                for i in range(len(img_list)):
                    download_pic(img_list[i].get_attribute('src'), pic_title + '(' + str(i) + ')', log_instance)
                browser.close()
                browser.switch_to.window(n[0])
            except Exception as error:
                log_instance.write_log(get_runtime_msg('error') + str(error))
                browser.quit()
                continue
        browser.quit()

if __name__ == '__main__':
    pool_nums = 50
    clsq_pool = Pool(pool_nums)
    for i in range(1, pool_nums + 1):
        clsq_pool.apply_async(start, args=(i,pool_nums + 1))
    clsq_pool.close()
    clsq_pool.join()