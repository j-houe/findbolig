from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



# Initiate WebDriver 
options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)
driver.get('https://fplform.com/fpl-optimiser-with-transfers-csv')

# Send extract settings to WebDriver
out_settings = settings.copy()
for key in settings:
    if settings[key]:
        driver.find_element(By.NAME, key).send_keys(settings[key])
    out_settings[key] = driver.find_element(By.NAME, key).get_attribute('value')

# Download
driver.find_element(By.NAME, 'submit').click()
max_delay = 20
delay = 0
while not os.path.exists(filename) or delay == max_delay:
    time.sleep(1)
    delay += 1
driver.close()
