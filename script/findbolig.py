from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()
from typing import List
import time
import os



class FindBolig():
    def __init__(self, filters: str):
        self.url_base = "https://findbolig.nu/da-dk/find?" + filters
        self.email = os.getenv("email")
        self.pw = os.getenv("password")
        if self.email is None or self.pw is None:
            raise ConnectionError("Failed to retrieve credentials from .env")

    def init_webdriver(self, headless: bool = True):
        options = Options()
        options.headless = headless
        self.driver = webdriver.Chrome(options=options)
    
    def decline_cookies(self):
        try:
            self.driver.find_element(By.ID, 'declineButton').click()
        except:
            pass

    def go_to_base(self):
        self.attempt_get(self.url_base)
        self.decline_cookies()

    def attempt_get(self, url: str):
        self.driver.get(url)

    def get_apartments(self, timeout: int = 10) -> List[WebElement]:
        timeout_count = 0
        while True:            
            apartments = self.driver.find_elements(By.CLASS_NAME, "property-card")
            timeout_count += 1
            if len(apartments) > 0:
                return apartments
            if timeout_count == timeout:
                return apartments
            time.sleep(1)
    
    def sign_up(self, apartment_url: str):
        self.attempt_get(apartment_url)
        self.login()
        self.attempt_find_clickable(By.XPATH, '//*[text()="Bestil fremvisning"]').click()

    def attempt_find_clickable(
            self, 
            by: str, 
            value: str, 
            timeout: float = 10) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        return element

    def login(self):
        if self.logged_out():
            self.attempt_find_clickable(By.XPATH, '//*[@id="app"]/header/div[2]').click()
            # Input email
            self.attempt_find_clickable(By.ID, "emailInput").send_keys(self.email)
            # "Fortsæt"
            self.attempt_find_clickable(By.XPATH, '//button[text()="Fortsæt"]').click()
            # Input pw
            self.attempt_find_clickable(By.ID, "loginPasswordInputxt").send_keys(self.pw)
            # "Log ind"
            self.attempt_find_clickable(By.XPATH, '//button[text()="Log ind"]').click()

    def logged_out(self) -> bool:
        try:
            check = self.attempt_find_clickable(By.XPATH, '//*[@id="app"]/header/div[2]', 5)
            return True
        except:
            check = self.attempt_find_clickable(By.XPATH, '//*[text()="Min side"]', 5)
            return False
            
    def close(self):
        self.driver.close()