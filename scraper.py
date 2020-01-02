from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
import sys
from datetime import date
import keyboard

uri = "https://www.youtube.com/playlist?list=WL"

def main():
    currDate = date.today()
    fileName = str(currDate.strftime("%d-%m-%Y")+'-VideoTitles.txt')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    allVids = []

    def getTitles():
        vids = []
        for vid in driver.find_elements_by_id('video-title'):
            title = vid.get_attribute('title')
            vids.append(title)
        return vids

    driver = webdriver.Chrome("chromedriver/chromedriver.exe", options=options)
    #driver = webdriver.PhantomJS(r"C:\Users\joe61081\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.implicitly_wait(4)

    print("Connecting to youtube...")
    driver.get(uri)
    time.sleep(2)
    print("Loading Cookies...")
    for cookie in pickle.load(open("googleCookies.pkl", "rb")):
        cookie.pop("expiry", None)
        driver.add_cookie(cookie)
    # pickle.dump(driver.get_cookies(), open("googleCookies.pkl", "wb"))

    time.sleep(2)

    print("Signing in...")
    driver.execute_script("location.reload();")

    time.sleep(2)

    total = driver.find_element_by_xpath('//*[@id="stats"]/yt-formatted-string[1]')
    strTotal = total.get_property('innerHTML')
    intTotal = int(''.join(filter(str.isdigit, strTotal)))

    print("Retrieving Titles...")
    while len(allVids) < intTotal:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        allVids = getTitles()

    print("Saving "+str(len(allVids))+" Titles...")

    with open("titles/"+fileName, 'w', encoding='utf-8') as f:
        for vid in allVids:
            f.write("%s\n" % vid)

    print("Done, Saved to '"+fileName+"'!")

    print("Press Any Key To Exit...")
    if keyboard.read_hotkey() is not None:
        sys.exit(0)

if __name__ == '__main__':
    main()
