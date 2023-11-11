from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
# Add options as needed
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
