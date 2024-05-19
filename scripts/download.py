import time, os
from selenium_workflow import SeleniumWorkflow

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


# Code for downloading a list of links
def download_with_ezmp3(links, download_path:str):
    xpaths = get_xpaths('ezmp3/xpaths.txt')
    # for link in links:
    converter_url = "https://ezmp3.cc/"
    workflow = SeleniumWorkflow(
        wait=1, recursion=False, xpath=True, download_path=download_path, tasks=[
            ['open', converter_url],
            ['input', xpaths[0], links[1]],
            ['click', xpaths[1]],
            ['wait_for_click', xpaths[2]],
        ])
    workflow.run_workflow()
        



