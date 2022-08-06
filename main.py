from stats import Stats
from sendmail import SendMail
from scrap import ScrapData
from timer import Timer
from sqlalchemy.orm import sessionmaker
import db
import json

def startDailyTask(sendMailObj,statsDict):
  sendMailObj.setCredentials(statsDict)
  print("\n\n\t\t\t\t**** SENDING MAIL ****\n")
  sendMailObj.sendMail()
  print("\n\n\t\t\t\t**** MAIL SENT.. WAITING FOR NEXT RUN..... ****\n")

def startScrapingTask(scrapObj,statsObj):
  print("\n\n\t\t\t\t**** SCRAPING DATA ****\n")
  scrapObj.scrapData()
  print("\n\n\t\t\t\t**** CREATING STATS ****\n")
  return [statsObj.getOverallStats(),statsObj.getTodaysStats(),statsObj.getMonthlyStats()]


if __name__ == "__main__":
  Session = sessionmaker(bind=db.engine)
  session = Session()
  credentials = json.loads(open("credentials.txt","r").read())
  scrapObj = ScrapData(session, db, credentials)
  statsObj = Stats(session, db)
  sendMailObj = SendMail(credentials)
  timerObj = Timer(credentials, startDailyTask, startScrapingTask)
  timerObj.startTimer(scrapObj,statsObj,sendMailObj)