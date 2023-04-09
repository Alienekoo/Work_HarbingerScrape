#main code
import harbingerscrape 
import sys
from harbingerscrape import harbingerScrape

amsAction = input('Please enter current status of what AMS is doing: ')
customerImpact = input('What is the Customer Impact? Please input NA if there is no impact: ')
chimeBridge = input('Any ongoing chime bridge? Please put NA if not: ')

if(len(sys.argv))>1:
  sm = harbingerScrape(sys.argv[1], amsAction, customerImpact, chimeBridge)
  try: 
    sm.openHarbinger()
  except Exception as e:
    print("An internal error occured. Please verify if the harbinger is valid and AMS impacted. Please run the script again.")
else:
  print("Please Enter the Harbinger ID and other inputs as asked., python3 Harbingerscrape/MIMEmail.py 21682")
