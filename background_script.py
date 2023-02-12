import numpy as np
import time
import os
from dotenv import load_dotenv
load_dotenv()

max = 5
user = os.getenv("email")
sleep = 1

print("Hello", user)
print("Let's count to", max)
count = 0
x = np.arange(1, max+1)
while True:
    print(x[count])
    if count == max-1:
        print("Script completed")
        break

    count += 1
    time.sleep(sleep)
