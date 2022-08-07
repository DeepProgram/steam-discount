import time
from datetime import datetime
from typing import Callable


class Timer:
    def __init__(self, credentials: dict, start_daily_task: Callable, start_scraping_task: Callable):
        self.credentials = credentials
        self.startDailyTask = start_daily_task
        self.startScrapingTask = start_scraping_task

    def start_timer(self, scrap_obj: object, stats_obj: object, send_mail_obj: object):
        send_mail_hour, send_mail_minute = map(int, self.credentials["sendmail"].split(":"))
        if self.credentials["gatherdata"][0] == "minutes":
            scrap_minute = self.credentials["gatherdata"][1]
        else:
            scrap_minute = int(self.credentials["gatherdata"][1] * 60)
        stats_dict = None
        count = 0
        while 1:
            if datetime.now().hour == send_mail_hour and datetime.now().minute == send_mail_minute:
                self.startDailyTask(send_mail_obj, stats_dict)
            if count == scrap_minute:
                count = 0
                stats_dict = self.startScrapingTask(scrap_obj, stats_obj)
            count += 1
            time.sleep(60)
 
