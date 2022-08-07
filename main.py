from stats import Stats
from sendmail import SendMail
from scrap import ScrapData
from timer import Timer
from sqlalchemy.orm import sessionmaker
import db
import json


def start_daily_task(send_mail_obj: SendMail, stats_dict: list):
    send_mail_obj.set_credentials(stats_dict)
    print("\n\n\t\t\t\t**** SENDING MAIL ****\n")
    send_mail_obj.send_mail()
    print("\n\n\t\t\t\t**** MAIL SENT.. WAITING FOR NEXT RUN..... ****\n")


def start_scraping_task(scrap_obj: ScrapData, stats_obj: Stats) -> list:
    print("\n\n\t\t\t\t**** SCRAPING DATA ****\n")
    scrap_obj.scrap_data()
    print("\n\n\t\t\t\t**** CREATING STATS ****\n")
    return [stats_obj.get_overall_stats(), stats_obj.get_today_stats(), stats_obj.get_monthly_stats()]


if __name__ == "__main__":
    Session = sessionmaker(bind=db.engine)
    session = Session()
    credentials = json.loads(open("credentials.txt", "r").read())
    scrapObj = ScrapData(session, db, credentials)
    statsObj = Stats(session, db)
    sendMailObj = SendMail(credentials)
    timerObj = Timer(credentials, start_daily_task, start_scraping_task)
    timerObj.start_timer(scrapObj, statsObj, sendMailObj)
 
