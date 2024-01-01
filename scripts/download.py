# Selenium Webdriver -> automate Google forms
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import time
import os

def change_iframe(driver: webdriver.Chrome):
    # Store iframe web element
    # switching to second iframe based on index
    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    for iframe in iframes:
        driver.switch_to.frame(iframe)
        print("iframes switched")
        try:
            driver.find_element(By.XPATH, '//*[@id="dismiss-button"]').click()
        except NoSuchElementException:
            continue
        else:
            break


def change_tab(driver: webdriver.Chrome):

    # change tabs after a link happens to be clicked #
    original_window = driver.current_window_handle
    # Check we don't have other windows open already
    print(len(driver.window_handles))

    # Wait for the new window or tab
    time.sleep(1)
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            print("tab changed")
            break
    # ------------------------------------------------- #


def convert_with_selenium(*args):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs", {
        "download.defualt_directory": r"C:\Users\abaadmin\Downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    driver = webdriver.Chrome(options=options)
    driver.get(url="https://yt1s.ltd/en194h/youtube-to-mp3")

    for i in range(len(args)):
        def run_task(j: int):  # maybe add a keyword argument saying restart=False, and when true leads to recursive
            if args[j][0] == "send":
                element = driver.find_element(by=By.XPATH, value=args[j][1])
                element.send_keys(args[j][2])
            elif args[j][0] == "click":
                if args[j][1] == "x":
                    element = driver.find_element(by=By.XPATH, value=args[j][2])
                else:
                    element = driver.find_element(by=By.ID, value=args[j][2])
                element.click()
            elif args[j][0] == "wait":
                time.sleep(args[j][1])
            else:
                time.sleep(1)
                if args[j][1] == "tab":
                    change_tab(driver)
                else:
                    change_iframe(driver)

        try:
            run_task(i)
        except ElementNotInteractableException or NoSuchElementException:
            print("restarting")
            run_task(i - 1)
            run_task(i)


# Code for downloading a list of links
def download_songs():
    # Specify the path to your text file
    file_path = '../music.txt'
    # Read the links from the text file and create a list
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file.readlines()]

    # Print the list of links (optional)
    
    path = "./downloaded_songs"
    for link in links:
        url_input_xpath = '//*[@id="txt-url"]'
        url_convert_xpath = '//*[@id="btn-submit"]'
        redirect_button_xpath = '//*[@id="mp3"]/table/tbody/tr/td[3]/a'
        add_xpath = "//*[@id='prime-popover-close-button']/a/img"
        download_button_id = 'A_downloadUrl'
        convert_with_selenium(["send", url_input_xpath, link],
                              ["click", "x", url_convert_xpath], ["wait", 1.5],
                              ["click", "x", redirect_button_xpath], ["change", "tab"], ["wait", 10],
                              ["click", "id", download_button_id], ["wait", 1], ["change", "iframe"])
        print("downloading\n")
        break


download_songs()

        