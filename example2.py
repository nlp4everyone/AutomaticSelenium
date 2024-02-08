from module.selenium_integration import AutomaticDriver,By,Keys,DriverAction
import time

"""
This script is trying to open multiple tabs at once
"""

driver = AutomaticDriver()
# Open new windows
driver.open_new_tab()
all_tab = driver.get_all_tab_id()
driver.switch_tab(all_tab[-1])
driver.access_url("https://www.google.com/")
driver.switch_tab(all_tab[0])
driver.access_url("https://www.google.com/")

time.sleep(5)

