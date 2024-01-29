from automatic_selenium import AutomaticDriver,By,Keys,ActionType
import time

driver = AutomaticDriver(no_head=False)
driver.access_url("https://www.google.com/")
element = driver.find_element_and_attribute(access_target=By.ID,value="APjFqb")
# Send text
driver.send_text(element=element,content="Machine Learning")
# # Enter
# driver.send_key(key=Keys.ENTER,element=element)
# Find object
element = driver.find_element_and_attribute(access_target=By.XPATH,value="//input[@class='gNO89b']")
# Click
driver.simple_action(element=element,action_type=ActionType.CLICK)

time.sleep(3)

