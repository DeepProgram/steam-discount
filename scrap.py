import requests
from bs4 import BeautifulSoup
import json
from datetime import date
import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists


class ScrapData():
  def __init__(self,session,db,credentials):
    self.session = session
    self.db = db
    self.credentials = credentials

  def ifAlreadyExistInDatabase(self,appid):
    return self.session.query(exists().where(self.db.transactions.gameid == appid)).scalar()

  def updateInDatabase(self,appid,discount):
    self.session.query(self.db.transactions).filter(self.db.transactions.gameid == appid,self.db.transactions.discount != discount).update({
      "discount":discount
      })

  def insertInDatabase(self,appid,gameInfo):
    tr = self.db.transactions(appid, gameInfo["name"], gameInfo["ip"], gameInfo["price"], gameInfo["discount"], gameInfo["date"])
    self.session.add(tr)

  def scrapData(self):
    startFrom = 0
    while startFrom <= self.credentials["search_amount"]:
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

      ip = res.cookies.get_dict()['steamCountry'][0:2]
      m = json.loads(res.text)
      soup = BeautifulSoup(m["results_html"],"html.parser")

      for link in soup.find_all({"a":"href"}):
        appid = 0
        try:
          appid = int(link["href"].split("/app/")[1].split("/")[0])
        except:
          continue
        name = link.find("div",attrs ={"class":"responsive_search_name_combined"}).div.span.text
        priceSection = link.find("div",attrs ={"class":"col search_price_discount_combined responsive_secondrow"})
        
        price = priceSection.contents[3]
        discount =  priceSection.div.span
        if discount: discount = int(discount.text[1:-1])
        else: discount = 0
        if discount == 0: continue
        if price.span == None:
          price = price.text.strip()
        else:
          price = price.contents[-1].strip()

        gameInfo = {
          "name":name,
          "ip":ip,
          "price":price,
          "date":str(date.today()),
          "discount": discount
        }
        
        ifGameExist = self.ifAlreadyExistInDatabase(appid) #Checking if the game id already exist or not
        if ifGameExist: self.updateInDatabase(appid, gameInfo["discount"]) #If exist calling a function to update that in database
        elif gameInfo["discount"] > 0: self.insertInDatabase(appid, gameInfo) #If dont exist then check discount is greather than zero
                                                                              #and if true add it in database by calling another function
      
      startFrom += 50
    self.session.commit() #Saving the changes in the database

