# Selenium Webdriver -> automate Google forms
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
import time
import os
import glob

def get_links():
    file_path = 'music.txt'
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
    extension_file_path = 'C:\\Users\\abaadmin\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\cjpalhdlnbpafiamejdnhcphjbkeiagm\\1.54.0_32.crx'
    options.add_extension(extension_file_path)

    driver = webdriver.Chrome(options=options)
    driver.get(url=url)

    def element_intercepted_exception_handling():
        # Getting link and opening it in new tab, rather than manually clicking an uninteractable element
        element = driver.find_element(by=By.XPATH, value=args[i][2])
        download_link = element.get_attribute("href")
        driver.quit()
        # open new webdriver with download link:
        options2 = webdriver.ChromeOptions()
        options2.add_experimental_option("detach", True)
        options2.add_experimental_option("prefs", {
            "download.defualt_directory": r"C:\Users\abaadmin\Downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        new_driver = webdriver.Chrome(options=options2)
        new_driver.get("https://google.com")
        new_driver.execute_script(f'window.open("{download_link}", "_blank");')

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
            # TODO: go over https://www.selenium.dev/documentation/webdriver/waits/
            while True:
                try:
                    run_task(i - 1)
                    run_task(i)
                except NoSuchElementException or ElementNotInteractableException:
                    run_task(i - 1)
                    run_task(i)
                except ElementClickInterceptedException:
                    element_intercepted_exception_handling()
                    break
                else:
                    break
        except ElementClickInterceptedException:
            element_intercepted_exception_handling()



# Code for downloading a list of links
def download_with_ezmp3(links, path):
    xpaths = get_xpaths('scripts\ezmp3\xpaths.txt')
    for link in links:
        converter_url = "https://ezmp3.cc/"
        convert_with_selenium(
            ["send", xpaths[0], link], ["wait", 1],
            ["click", "x", xpaths[1]], ["wait", 7],
            ["click", "x", xpaths[2]],
            url=converter_url
            )
        print("downloading")



