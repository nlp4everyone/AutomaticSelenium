from module.selenium_integration import AutomaticDriver,By,Keys,DriverAction
import time

"""
This script is trying to handle some basic function of Selenium
"""

driver = AutomaticDriver()
driver.access_url("https://google.com/",implicit_wait=2)
# Find element
element = driver.find_element(By.ID,"APjFqb")

# Send text
driver.send_key(key="Machine Learning",element=element)
# Enter
driver.send_key(key=Keys.ENTER,element=element)
time.sleep(1)
# Back to previous web
driver.handle_driver_action(action=DriverAction.BACK)
time.sleep(1)
# Refresh the current website
driver.handle_driver_action(action=DriverAction.REFRESH)

