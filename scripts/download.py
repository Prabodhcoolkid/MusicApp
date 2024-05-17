# Selenium Webdriver -> automate Google forms
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
import time, os

def get_links():
    file_path = '../music.txt'
    # Read the links from the text file and create a list
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file.readlines()]
    return links

def get_xpaths(path):
    with open(path, mode="r") as file:
        xpaths_raw = file.readlines()
        return [xpath.rstrip('\n') for xpath in xpaths_raw]

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


def convert_with_selenium(*args, url: str):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options, executable_path="..\\..\\..\\..\\..\\Downloads\\chromedriver.exe")
    driver.get(url)

    for i in range(len(args)):
        def run_task(j: int):  # maybe add a keyword argument saying restart=False, and when true leads to recursive
            if args[j][0] == "send":
                element = driver.find_element(by=By.XPATH, value=args[j][1])
                element.send_keys(args[j][2])
            elif args[j][0] == "click":
                element = driver.find_element(by=By.XPATH, value=args[j][2])
                element.click()
            elif args[j][0] == "wait":
                time.sleep(args[j][1])
            elif args[j][0] == "installing":
                # TODO: check os downloads directory for new file and close the driver
                print("installing")
            else:
                time.sleep(1)
                if args[j][1] == "tab":
                    change_tab(driver)
                else:
                    change_iframe(driver)

        try:
            run_task(i)
        except NoSuchElementException or ElementNotInteractableException:
            print(f"restarting task {i}")

# Code for downloading a list of links
def download_with_ezmp3(links):
    xpaths = get_xpaths('ezmp3/xpaths.txt')
    for link in links:
        converter_url = "https://ezmp3.cc/"
        convert_with_selenium(
            ["send", xpaths[0], link], ["wait", 1],
            ["click", xpaths[1]], ["wait", 7],
            ["click", xpaths[2]],
            url=converter_url
            )
        print("downloading")



