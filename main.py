from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time,os,pwd
import platform
from enum import Enum

# Browser
class Browser(Enum):
    CHROME = 0
    FIREFOX = 1

class ProfileType(Enum):
    FIRST = 0
    ALL = 1

class AutomaticDriver():
    def __init__(self,browser_type=Browser.CHROME,no_head = True,profile_type=ProfileType.FIRST):
        # Define chrome browser
        if browser_type == Browser.CHROME:
            print("Working in Chrome mode!")
            # Get profile
            profile_url,profile_list = self._get_profile(profile_type)
            # Define Option
            options = self._chrome_option(no_head=no_head,profile_url=profile_url,profile_list=profile_list)
            # Set driver
            self.driver = self._chrome_driver(options=options)
        # Define firefox browser
        elif browser_type == Browser.FIREFOX:
            print("Working in Firefox mode")
            self.driver = self._firefox_driver()
        else:
            self.driver = None

    def _chrome_driver(self,options):
        # Init driver
        # try:
        #     # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        #     self.driver = webdriver.Chrome(options=options)
        # except:
            # When have a problem, using default driver
        default_option = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=default_option)
        return self.driver

    def _chrome_option(self,no_head:bool,profile_url:str,profile_list:str):
        options = webdriver.ChromeOptions()
        # options.add_argument("--disable-extensions")
        # options.add_argument("--disable-popup-blocking")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--disable-plugins-discovery")
        # options.add_argument("--no-sandbox")
        # provide location where chrome stores profiles

        # Add this option to fix bugs
        # options.add_argument("--remote-debugging-port=8000")
        # No header
        if no_head: options.add_argument("--headless")

        # Linux case
        user_data_url = fr"--user-data-dir={profile_url}"

        # Set profile
        options.add_argument(user_data_url)
        options.add_argument(rf'--profile-directory={profile_list}')
        return options

    def _firefox_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        # Init firefox driver
        return webdriver.Firefox()

    def _get_profile(self,profile_type):
        # Current os
        main_os = platform.system()
        if main_os != "Linux": raise Exception("Current supporting Linux operation system")

        # Check profile
        try:
            # Get username
            machine_name = pwd.getpwuid(os.getuid())[0]
            # Default url
            profile_url = f"/home/{machine_name}/.config/google-chrome"
            # Profile list
            profile_list = [profile_name for profile_name in os.listdir(profile_url) if profile_name.startswith("Profile")]
            # Sorted list
            profile_list = sorted(profile_list)

            # Print out state
            print(f"There are {len(profile_list)} profile with this computer. Including: " + ", ".join(profile_list))

            if profile_type == ProfileType.FIRST:
                profile_list = profile_list[0]
            return profile_url,profile_list
        # Print exception
        except Exception as e:
            print(e)
            raise Exception("Failed when loading project")

    def access_url(self,url:str,implicit_wait = 5) -> str:
        # Access to url
        self.driver.implicitly_wait(implicit_wait)
        self.driver.get(url)

    def get_page_source(self):
        # Get page source
        return self.driver.page_source

    def get_title(self):
        # Get title
        return self.driver.title

    def find_element_and_attribute(self,access_target,value:str):
        # Find object
        element = self.driver.find_element(access_target,value)
        # Role of the element
        role = element.aria_role
        # Element property
        element_text = element.text
        element_location = element.location
        element_pic = element.screenshot_as_png # element.screenshot
        print(element)
        print(f"Element text: {element_text}. Role: {role}. Location: {element_location}")

        return element

    def send_text(self,content:str,element,overide=True):
        # if isinstance(element,WebElement): raise Exception("Please insert webelement to handle this action")
        # If not overide
        if not overide: element.clear()
        element.send_keys(content)

    def send_key(self,key,element,overide=True):
        element.send_keys(key)

# Show instruction
# notePath = "notes.txt"
# if os.path.exists(notePath):
#     with open(notePath,'r') as f:
#         print(f.read())


