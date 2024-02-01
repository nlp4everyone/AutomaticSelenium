from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
#create chromeoptions instance
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

#provide location where chrome stores profiles
options.add_argument(r"--user-data-dir=/home/phong/.config/google-chrome")

#provide the profile name with which we want to open browser
options.add_argument(r'--profile-directory=Profile 6')

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

#provide website url here
driver.get("https://omayo.blogspot.com/")

#find element using its id
print(driver.find_element(By.ID,"home"))