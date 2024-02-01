from automatic_module import AutomaticDriver,By,Keys
from utils.supported_type import SimpleAction
import time

driver = AutomaticDriver()
driver.access_url("https://www.google.com/")
element = driver.find_element(access_target=By.ID,value="APjFqb")
# Send text
driver.send_text(element=element,content="Machine Learning")
# Enter
driver.send_key(key=Keys.ENTER,element=element)
# Click
# driver.simple_action(element=element,action_type=SimpleAction.CLICK)

