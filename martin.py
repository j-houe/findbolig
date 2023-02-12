from selenium import webdriver
from selenium.webdriver.chrome.options import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from bs4 import BeautifulSoup
import time
import os
import re
import pandas
from datetime import date
from twilio.rest import Client
import datetime

# Opsætning:
#1 Download chromedriver https://chromedriver.chromium.org/downloads version der tilsvarer chrome version. Check chromeversion her: chrome://settings/help
#2 Sæt sti til chromedriver
Path = "C:\\Trader\\chromedriver.exe"

#3 Opret profil på findbolig - indsæt
brugernavn = "..."
adgangskode = "..."

#4 Gå til: https://www.findbolig.nu/ledigeboliger/liste.aspx?where=K%C3%B8benhavn%2C%20&rentmax=10000&roomsmin=2&m2min=63&showrented=1&showyouth=0&showlimitedperiod=1&showunlimitedperiod=1&showOpenDay=0
# Opdater kriterier, tryk enter og indsæt ny urlkode
url = """
    https://www.findbolig.nu/ledigeboliger/liste.aspx?where=K%C3%B8benhavn%2C%20&
    rentmax=10000&
    roomsmin=2&
    m2min=63&
    showrented=1&
    showyouth=0&
    showlimitedperiod=1&
    showunlimitedperiod=1&
    showOpenDay=0
"""

#5 (optional) Lav en konto på twilio for at modtage sms med lejligheder. Indsæt
twilio_oprettet = False
account_sid = "AC5c7a47e0d00aac57787020c9ae47aba4"
auth_token  = "e90d696fc814b1b291716c9140ae94c3"
nummer_fra = '+13237989806'
nummer_til = '+4525157878'



# --- Kode ---

ConnectionTimeout = 0

options = Options()
options.add_argument("--log-level=3")
options.add_argument("--silent")
options.add_argument("--no-sandbox")
options.add_argument("--disable-logging")
options.add_argument("--mute-audio")

driver = webdriver.Chrome(executable_path=Path, options=options)

try:
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[2]/div[1]/button[3]").click()

except:
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[2]/div[1]/button[3]").click()

time.sleep(5)

appartments = driver.find_elements_by_class_name("advertLink")

for i in range(20*3*60*24*4):
    print(i)
    realtime = datetime.datetime.now()

    # Ændre til True for at sætte computeren i dvale klokken 19
    if False:
        if realtime.hour >= 19:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    try:
        if len(appartments) > 0:
            driver.find_element_by_id("fm1_link_Login").click()
            time.sleep(2)
            driver.find_element_by_id("ctl00_placeholdercontent_1_txt_UserName").send_keys(brugernavn)
            driver.find_element_by_id("ctl00_placeholdercontent_1_txt_Password").send_keys(adgangskode)
            time.sleep(1)
            driver.find_element_by_id("ctl00_placeholdercontent_1_but_LoginShadow").click()
            time.sleep(3)
            driver.get(url)
            time.sleep(3)
            driver.find_elements_by_class_name("advertLink")[1].click()
            time.sleep(3)
            driver.find_element_by_id("ctl00_placeholdercontentright_1_but_Signup").click()
            client = Client(account_sid, auth_token)

            if twilio_oprettet:
                message = client.messages.create(
                    from_=nummer_fra, to=nummer_til,
                    body='Nyt på findbolig'
                )

            time.sleep(60)
            break
        else:
            time.sleep(20)
            driver.refresh()
            ConnectionTimeout = 0
            time.sleep(2)
            appartments = driver.find_elements_by_class_name("advertLink")

    except:

        if ConnectionTimeout <= 5:
            ConnectionTimeout += 1
            time.sleep(15)
            driver.get(url)
            time.sleep(2)
            appartments = driver.find_elements_by_class_name("advertLink")

        else:

            if twilio_oprettet:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    from_=nummer_fra, to=nummer_til,
                    body='Noget gik galt'
                )

            time.sleep(5)
            break

#Kan slukke computeren når den har fundet en lejlighed
#os.system("shutdown /s /t 1")