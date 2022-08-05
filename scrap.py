import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import date
import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

import stats


def startScraping():
  print("\n\n\t\t**** SCRAPING DATA ****\n\n")
  Session = sessionmaker(bind=db.engine)
  session = Session()
  credentials = json.loads(open("credentials.txt","r").read())
  startFrom = 0

  while startFrom <= credentials["search_amount"]:
    param ={
    "query":"",
    "start":startFrom,
    "count":"50",
    "dynamic_data":"", 
    "sort_by": "_ASC",
    "filter": "topsellers",
    "infinite": "1"
    }

      
    res=None
    try:
      res = requests.get("https://store.steampowered.com/search/results/", params=param)
    except:
      print("Error Occured")

    ip=res.cookies.get_dict()['steamCountry'][0:2]
    m = json.loads(res.text)
    soup = BeautifulSoup(m["results_html"],"html.parser")

    for link in soup.find_all({"a":"href"}):
      appid = ""
      try:
        appid = int(link["href"].split("/app/")[1].split("/")[0])
      except:
        continue
      data = link.find("div",attrs ={"class":"responsive_search_name_combined"})
      name = data.div.span.text
      priceSection = link.find("div",attrs ={"class":"col search_price_discount_combined responsive_secondrow"})
      
      price = priceSection.contents[3]
      discount =  priceSection.div.span
      if discount: discount = discount.text[1:]
      else: discount = "0%" 
      if price.span == None:
        price = price.text.strip()
      else:
        price = price.contents[-1].strip()

      gameInfo = {
        "name":name,
        "ip":ip,
        "price":price,
        "date":str(date.today()),
        "discount": int(discount[:-1])
      }
        
      ifExist = session.query(exists().where(db.transactions.gameid == appid)).scalar()
      if ifExist:
        session.query(db.transactions).filter(db.transactions.gameid == appid,db.transactions.discount > gameInfo["discount"]).update({
      "discount":gameInfo["discount"]
      })
      elif gameInfo["discount"] > 0:
        tr = db.transactions(appid, gameInfo["name"], gameInfo["ip"], gameInfo["price"], gameInfo["discount"], gameInfo["date"])
        session.add(tr)
    startFrom += 50
  session.commit()
  stats.startStatus()


