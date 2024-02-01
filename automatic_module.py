from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
import time,os,pwd,platform
from utils.supported_type import SimpleAction,BrowserType,AdvancedAction

class AutomaticDriver():
    def __init__(self,browser_type=BrowserType.CHROME,profile_name=None):
        # Profile name
        self.profile_name = profile_name

        # Define chrome browser
        if browser_type == BrowserType.CHROME:
            print("Setup Chrome mode!")
            # Chosse Chrome option
            self._options = self._chrome_option(profile_name=self.profile_name)
            # Set driver
            self.driver = self._chrome_driver(options=self._options)

        # Define firefox browser
        elif browser_type == BrowserType.FIREFOX:
            print("Setup Firefox mode")
            self.driver = self._firefox_driver()
        else:
            raise Exception("Driver hasn't been initialized")

        # create action chain object
        self.action = ActionChains(self.driver)

    def _chrome_driver(self,options):
        # Init driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return self.driver

    def _chrome_option(self,profile_name=None):
        # Current os
        main_os = platform.system()
        if main_os != "Linux": raise Exception("Current supporting Linux operation system")
        # Define options
        options = webdriver.ChromeOptions()

        if isinstance(profile_name,str):
            # Get username
            machine_name = pwd.getpwuid(os.getuid())[0]
            # Default url
            profile_url = f"/home/{machine_name}/.config/google-chrome"

            # Check if profile url existed!
            if not os.path.exists(profile_url): raise Exception(f"{profile_url} not existed in your machine!")
            list_profile = [profile for profile in os.listdir(profile_url) if profile.startswith("Profile")]
            # Check if input profile is existed!
            if not profile_name in list_profile: raise Exception(f"{profile_name} not existed in {profile_url}. Available profile: "+", ".join(list_profile))

            print(f"Working with: {profile_name}. Notice that this mode has no UI!")
            # Add option (No header)
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")

            # Add profile to option
            options.add_argument(fr"--user-data-dir={profile_url}")
            options.add_argument(rf'--profile-directory={profile_name}')
        elif profile_name == None:
            print("Basic mode without Profile!")
        # Other option
        # options.add_argument("--disable-extensions")
        # options.add_argument("--disable-popup-blocking")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--disable-plugins-discovery")
        return options

    def _firefox_driver(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        # Init firefox driver
        return webdriver.Firefox()

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

    def find_element(self,access_target:By,value:str):
        # Find object
        return self.driver.find_element(access_target,value)

    def get_element_attribute(self,element):
        # Role of the element
        element_role = element.aria_role
        # Element property
        element_text = element.text
        element_location = element.location
        print(f"Element text: {element_text}. Role: {element_role}. Location: {element_location}")
        return element_text,element_role,element_location

    def send_text(self,content:str,element,overide=True):
        # If not overide
        if not overide: element.clear()
        element.send_keys(content)

    def send_key(self,key,element):
        element.send_keys(key)

    def simple_action(self,element,action_type=SimpleAction):
        # Select action
        if action_type == SimpleAction.CLICK:
            self.action.click(element)

        # Make the action
        self.action.perform()

    def advance_action(self, element, action_type=AdvancedAction):
        # Select action
        if action_type == AdvancedAction.CLICK_AND_HOLD:
            self.action.click_and_hold(element)

        # Make the action
        self.action.perform()



