import time
from datetime import datetime

class Timer():
  def __init__(self,credentials,startDailyTask,startScrapingTask):
    self.credentials = credentials
    self.startDailyTask = startDailyTask
    self.startScrapingTask = startScrapingTask

  def startTimer(self,scrapObj,statsObj,sendMailObj):
    sendMailHour,sendMailMinute = map(int,self.credentials["sendmail"].split(":"))
    scrapMinute = 0
    if self.credentials["gatherdata"][0] == "minutes":
      scrapMinute = self.credentials["gatherdata"][1]
    else: scrapMinute = int(self.credentials["gatherdata"][1]*60)
    statsDict = None
    count = 0
    while 1:
      if datetime.now().hour == sendMailHour and datetime.now().minute == sendMailMinute:
        self.startDailyTask(sendMailObj,statsDict)
      if count == scrapMinute:
        count = 0
        statsDict = self.startScrapingTask(scrapObj,statsObj)  
      count += 1 
      time.sleep(60)

