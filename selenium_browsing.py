from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging

driver = None

ua_youtubetv='Mozilla/5.0 (SMART-TV; Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'

def get_driver(options=None):
    global driver
    if options is None:
        options = webdriver.ChromeOptions()
    if driver is None:
        options.add_argument('--use-fake-ui-for-media-stream')
        driver = webdriver.Chrome(options=options)
    return driver


def open_pc_site():
    try: 
        global driver
        current_url = "chrome://version/"
        driver = get_driver()
        if driver is not None:
            current_url = driver.current_url
            driver.close()          
        driver = None
        options = webdriver.ChromeOptions()
        driver = get_driver(options)
        driver.set_window_size(720, 1280)
        driver.get(current_url)
    except Exception as e:
        print(f"Error executing code: {e}")


def open_youtube_tv():
    try: 
        global driver
        driver = get_driver()
        if driver is not None:
            driver.close()
        driver = None
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent=' + ua_youtubetv)
        driver = get_driver(options)
        driver.set_window_size(1280, 720)
        driver.get("https://www.youtube.com/tv#/")
    except Exception as e:
        print(f"Error executing code: {e}")

def link_click(link):
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, link).click()
    except Exception as e:
        print(f"Error executing code: {e}")

def exec_command(command):
    driver = get_driver()
    try:
        code = compile(command, '<string>', 'exec')
    except SyntaxError as e:
        print(f"Syntax error in your code: {e}")
    else:
        try:
            logging.debug(f"driver:{driver}")
            logging.debug(f"command:{command}")
            exec(code)
        except Exception as e:
            print(f"Error executing code: {e}") 
    return f"exec_command({command})" 

def main():
    command = [
        'driver.get("https://www.yahoo.co.jp")',
        'link_click("ニュース")',
        'link_click("速報")',
        "open_youtube_tv()",
        "open_pc_site()",
        'driver.get("https://www.youtube.com")'
    ]
    for i in command:
        result = exec_command(i)
        time.sleep(2)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")    
    main()