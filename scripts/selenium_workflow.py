from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException

# TODO: Improve the Selenium workflow class
class SeleniumWorkflow:
    def __init__(self, download_path:str, wait:int=0, recursion:bool=False, xpath:bool=False, tasks:list=[]):
        self.download_path = download_path
        # Check for wait time
        if wait > 0:
            self.tasks = self.insert_wait(wait, tasks)
        else:
            self.tasks = tasks
        self.recursion = recursion
        self.xpath = xpath
            
    
    def insert_wait(self, wait_time, tasks):
        new_tasks = []
        for task in tasks:
            new_tasks.append(task)
            new_tasks.append(['wait', wait_time])
        return new_tasks

    def get_options(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_path,  
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        chrome_options.add_experimental_option("detach", True)
        return chrome_options

    def run_workflow(self):
        # setup the driver
        options = self.get_options()
        driver = webdriver.Chrome(options=options)
        try:
            for task in self.tasks:
                action = task[0]
                if action == 'open':
                    url = task[1]
                    driver.get(url)
                elif action == 'click':
                    element_id = task[1]
                    if self.xpath:
                        element = driver.find_element(By.XPATH, element_id)
                    else:
                        element = driver.find_element(By.ID ,element_id)
                    element.click()
                elif action == 'input':
                    element_id = task[1]
                    text = task[2]
                    if self.xpath:
                        element = driver.find_element(By.XPATH, element_id)
                    else:
                        element = driver.find_element(By.ID ,element_id)
                    element.send_keys(text)
                elif action == 'wait_for_click':
                    # Explicit wait for an element to be clickable
                    xpath = task[1]
                    wait = WebDriverWait(driver, 3)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    print("Waiting for element to be clickable")
                    element.click()
                elif action == 'wait':
                    wait = WebDriverWait(driver, task[1])
        except ElementNotInteractableException:
            # TODO: Create Exception Handlers
            print("Element is not interactable")
        finally:
            print("Workflow completed")
            # driver.quit()

# Example usage
"""
workflow = SeleniumWorkflow(
    0, False, False,
    tasks=[['open', 'https://www.example.com'],
    ['input', 'username', 'my_username'],
    ['input', 'password', 'my_password'],
    ['click', 'login_button']]
)
workflow.run_workflow()
"""

# TODO: Learn about custom exceptions, stack-tracing etc. in Python
class SeleniumWorkflowException(Exception):
    pass