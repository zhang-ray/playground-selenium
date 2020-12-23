from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os, fnmatch, shutil
import _thread
import traceback 

def random_view():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def init(chrome_path):
    result = find(r'chromedriver*.exe', os.path.dirname(os.path.realpath(__file__)))
    shutil.copyfile(result[0], os.path.join(chrome_path, r'chromedriver.exe'))


def entry(chrome_path, dest_page):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--incognito")
    # chromeOptions.add_argument('--headless')
    # chromeOptions.add_argument('--no-sandbox')

    driver = webdriver.Chrome(os.path.join(chrome_path, r'chromedriver.exe'), options=chromeOptions)  # 浏览器驱动

    driver.delete_all_cookies()  # 删除cookie

    driver.get(dest_page)
    driver.refresh()

    time.sleep(10)
    source = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a')
    # action chain object creation
    action = ActionChains(driver)
    # move to the element and click then perform the operation
    action.move_to_element(source).click().perform()

    random_view()

    # to close the browser
    time.sleep(30) 
    driver.quit()





if __name__ == "__main__":
    # chrome_path = r'C:\Users\root\scoop\apps\googlechrome\81.0.4044.138'
    chrome_path = r'C:\Program Files\Google\Chrome\Application'
    init(chrome_path)

    for i in range(100):
        try:
            _thread.start_new_thread(entry,(chrome_path, os.getenv('DEST_PAGE')))
            time.sleep(1)
        except:
            traceback.print_exc() 

