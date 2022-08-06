import re
import db
from sqlalchemy.orm import sessionmaker
import sys
from datetime import datetime,timedelta

class Stats():
  def __init__(self,session,db):
    self.session = session
    self.db = db

  def getTodaysData(self):
    gameDataDict = {}
    today = str(datetime.now().date())
    for s in self.session.query(self.db.transactions).filter(self.db.transactions.date == today):
      gameDataDict[s.gameid] = {
        "name": s.name,
        "price":s.price,
        "discount": s.discount,
        "date":s.date
      }
    return gameDataDict
    
  def getMonthlyData(self):
    gameDataDict = {}
    today = datetime.now()
    previousMonth = str((today.replace(day=1) - timedelta(days=1)).replace(day=today.day).date())
    for s in self.session.query(self.db.transactions).filter(self.db.transactions.date >= previousMonth,
                                                             self.db.transactions.date <= str(today.date()) ):
      gameDataDict[s.gameid] = {
        "name": s.name,
        "price":s.price,
        "discount": s.discount,
        "date":s.date
      }
    return gameDataDict

  def getDataFromDatabase(self):
    gameDataDict = {}
    for s in self.session.query(self.db.transactions).all():
      gameDataDict[s.gameid] = {
        "name": s.name,
        "price":s.price,
        "discount": s.discount,
        "date":s.date
      }
    return gameDataDict

  def getAllCurrentStats(self,gameDataDict):
    currentMaxDiscount,currentHighestPrice,currenLowestPrice = 0,0,sys.maxsize
    freeGame = []
    for key,value in gameDataDict.items():
      if value["discount"] != 100:
        tempPrice = re.findall('[0-9]+', value["price"])
        floatPrice = float(f'{"".join(tempPrice[0:-1])+"."+tempPrice[-1]}')
        if floatPrice > currentHighestPrice:currentHighestPrice = floatPrice
        if floatPrice < currenLowestPrice:currenLowestPrice = floatPrice
        if value["discount"] > currentMaxDiscount:currentMaxDiscount = value["discount"]
      else: freeGame.append(value["name"])
    return [currentMaxDiscount,currenLowestPrice,currentHighestPrice,freeGame]

  def generateStatsDictionary(self,gameDataDict):
    #Getting all current max discount,highest price,lowest price and free games from database
    currentMaxDiscount,currenLowestPrice,currentHighestPrice,freeGame = self.getAllCurrentStats(gameDataDict)
    # Now counting the individual category app of maxdicount,lowest price and highest price and returning
    # a dictionarys
    countMaxDiscount,countHighestPrice,countLowestPrice = 0,0,0
    for key,value in gameDataDict.items():
      if value["discount"] != 100:
        tempPrice = re.findall('[0-9]+', value["price"])
        newPrice = float(f'{"".join(tempPrice[0:-1])+"."+tempPrice[-1]}')
        if currentMaxDiscount == value["discount"]: countMaxDiscount += 1
        if int(currentHighestPrice) == int(newPrice): countHighestPrice += 1
        if int(currenLowestPrice) == int(newPrice): countLowestPrice += 1

    return {
    "Max_Discount":{"Count":countMaxDiscount,"Discount":currentMaxDiscount},
    "Lowest_Price":{"Count":countLowestPrice,"Price":currenLowestPrice},
    "Highest_Price":{"Count":countHighestPrice,"Price":currentHighestPrice},
    "Free_Games":{"Count": len(freeGame),"Game_Names":freeGame}
    }

  def getOverallStats(self):
    return self.generateStatsDictionary(self.getDataFromDatabase())


  def getTodaysStats(self):
    return self.generateStatsDictionary(self.getTodaysData())

  def getMonthlyStats(self):
    return self.generateStatsDictionary(self.getMonthlyData())

