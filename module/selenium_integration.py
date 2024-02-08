from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
import os,pwd,platform
from utils.supported_type import SimpleAction,BrowserType,DriverAction
img_folder = "Image"

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

    def access_url(self,url:str,implicit_wait = 1):
        # Wait until the web is fully loaded
        self.driver.implicitly_wait(implicit_wait)
        # Access to url
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

    def send_key(self,key,element,overide=True):
        if isinstance(key,str):
            # Clear if not overide
            if not overide: element.clear()
        element.send_keys(key)

    def handle_simple_action(self,element,action_type=SimpleAction):
        # Left click
        if action_type == SimpleAction.LEFT_CLICK:
            self.action.click(element)
        # Right click
        elif action_type == SimpleAction.RIGHT_CLICK:
            self.action.context_click(element)
        # Double click
        elif action_type == SimpleAction.DOUBLE_CLICK:
            self.action.double_click(element)
        # Release key down on this element
        elif action_type == SimpleAction.RELEASE:
            self.action.release(element)
        # Click and hold action
        elif action_type == SimpleAction.CLICK_AND_HOLD:
            self.action.click_and_hold(element)
        # Make the action
        self.action.perform()

    def move_to_element(self,element):
        # Move to element
        # self.action.move_to_element(element)
        self.action.click(element)
        self.action.perform()

    def drag_and_drop(self,source_element,target_element):
        self.action.drag_and_drop(source_element, target_element)
        self.action.perform()

    def send_keystroke(self,key_to_hold:Keys,key_to_click:Keys):
        # Send keystroke to the service
        self.action.key_down(key_to_hold).send_keys(key_to_click).key_up(key_to_hold)
        self.action.perform()

    def handle_driver_action(self,action=DriverAction):
        if action == DriverAction.FORWARD:
            self.driver.forward()
        elif action == DriverAction.BACK:
            self.driver.back()
        elif action == DriverAction.REFRESH:
            self.driver.refresh()
        elif action == DriverAction.FULL_SCREEN:
            self.driver.maximize_window()
        elif action == DriverAction.MINIMIZE_WINDOW:
            self.driver.minimize_window()

    def insert_script(self,script=None):
        base_script = "alert('alert via selenium')"
        if script != None:
            base_script = script
        self.driver.execute_async_script(base_script)

    def get_screenshot(self,img_name = "img.png"):
        # Base 64 image format
        # base64_img = self.driver.get_screenshot_as_base64()

        # Create image folder
        os.makedirs(img_folder,exist_ok=True)

        # Define img path
        img_path = os.path.join(img_folder,img_name)

        self.driver.get_screenshot_as_file(img_path)
        print(f"Save image: {img_name} to folder {img_folder}")

    def get_window_rectangle(self):
        # Get the x position, y postion, width and height of current driver window
        return self.driver.get_window_rect()

    def set_window_rec(self,x_pos=0,y_pos=0,width=300,height=300):
        # Set the dimensions of windows
        self.driver.set_window_rect(x=x_pos,y=y_pos,width=width,height=height)
    def get_current_url(self):
        # Get current url
        return self.driver.current_url

    def open_new_tab(self):
        # Open new tab
        self.driver.execute_script("window.open()")

    def get_all_tab_id(self):
        # Get all window handles
        return self.driver.window_handles

    def get_current_tab_id(self):
        return self.driver.current_window_handle

    def switch_tab(self,tab_id):
        self.driver.switch_to.window(tab_id)

        # def move_to_offset(self,x_offset,y_offset):
    #     self.action.move_by_offset(xoffset=x_offset,yoffset=y_offset)
    #     self.action.perform()




