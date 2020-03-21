from selenium import webdriver
import requests
import time

proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}

def download(url):
    filename = str(time.time()) + ".jpg"
    while True:
        try:
            resp = requests.get(url, proxies=proxies)
            with open('E:/pic/' + filename, 'wb') as f:
                f.write(resp.content)
            print("file " + filename + "done")
            break
        except:
            print("file " + filename + " download error")
            time.sleep(1)
            continue


# 设置本地代理
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--proxy-server=http://127.0.0.1:1080")

# executable_path是本地的ChromeDriver路径
browser = webdriver.Chrome(chrome_options = chromeOptions, executable_path="E:\chromedriver_win32\chromedriver.exe")

# 每一页中主题的Xpath路径
xpath_list = []
for i in range(11, 101):
    temp = '//*[@id="ajaxtable"]/tbody[2]/tr[' + str(i) + ']/td[2]/h3/a'
    xpath_list.append(temp)

global n

for i in range(1, 100):
    while True:
        try:
            browser.get("http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i))
            break
        except:
            time.sleep(1)
            print("get url " + "http://t66y.com/thread0806.php?fid=8&search=&page=" + str(i) + " failed,try again")
            continue
    for item in xpath_list:
        try:
            browser.find_element_by_xpath(item).click()
            time.sleep(1)
            n = browser.window_handles
            browser.switch_to.window(n[-1])
            img_list = browser.find_elements_by_tag_name("img")
            for image in img_list:
                download(image.get_attribute('src'))
            browser.close()
            browser.switch_to.window(n[0])
        except:
            browser.close()
            browser.switch_to.window(n[0])
            continue
    browser.close()