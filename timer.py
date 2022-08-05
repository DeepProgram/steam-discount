import schedule
import time
import scrap
import sendmail
import json


def startTimer():
  credentials = json.loads(open("credentials.txt","r").read())
  schedule.every().day.at(credentials["sendmail"]).do(sendmail.sendMail)
  if credentials["gatherdata"][0] == "minutes":
    schedule.every(credentials["gatherdata"][1]).minutes.do(scrap.startScraping)
  elif credentials["gatherdata"][0] == "hours":
    schedule.every(credentials["gatherdata"][1]).hours.do(scrap.startScraping)


  while 1:
    schedule.run_pending()
    time.sleep(1)