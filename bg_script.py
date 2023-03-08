from findbolig import FindBolig
from time import sleep


filters = """ 
    Commune=Frederiksberg&
    City=København+V,København+Ø&
    Rooms=2&
    RentalPeriod=Unlimited&
    Rent=16000
""".replace('\n','').replace(' ', '')
refresh_delay = 30
max_errors = 60

findbolig = FindBolig(filters)
findbolig.init_webdriver(headless=False)

error_count = 0
while True: 
    try: 
        findbolig.go_to_base()
        apartments = findbolig.get_apartments()
        
        if len(apartments) > 0:
            findbolig.login()
            findbolig.sign_up(apartments[0])
            print("Signed up to residence!", apartments[0].get_property("href"))
            sleep(3)
            print("Terminating script ...")
            sleep(3)
            break
        
        sleep(refresh_delay)
    
    except:
        error_count += 1
        print(f"Something went wrong ... {error_count}/{max_errors}")
        if error_count == max_errors:
            sleep(3)
            print("Terminating script ...")
            sleep(3)
            break