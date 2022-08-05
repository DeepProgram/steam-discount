import re,json
import db
from sqlalchemy.orm import sessionmaker
import sys

def startStatus():
  print("\n\n\t\t**** CREATING STATS ****\n\n")
  Session = sessionmaker(bind=db.engine)
  session = Session()
  mainDict = {}
  for s in session.query(db.transactions).all():
    mainDict[s.gameid] = {
      "name": s.name,
      "price":s.price,
      "discount": s.discount,
      "date":s.date
    }


  tempMaxDiscount,temphighest,tempLowewstPrice = 0,0.0,sys.maxsize
  freeGame = []
  for key,value in mainDict.items():
    if value["discount"] != 100:
      tempData = re.findall('[0-9]+', value["price"])
      newPrice = float(f'{"".join(tempData[0:-1])+"."+tempData[-1]}')
      if newPrice > temphighest:temphighest = newPrice
      if newPrice < tempLowewstPrice:tempLowewstPrice = newPrice
      if value["discount"] > tempMaxDiscount:tempMaxDiscount = value["discount"]
    else: freeGame.append(value["name"])

  
  countMaxDiscount,countHighestPrice,countLowestPrice = 0,0,0
  for key,value in mainDict.items():
    if value["discount"] != 100:
      tempData = re.findall('[0-9]+', value["price"])
      newPrice = float(f'{"".join(tempData[0:-1])+"."+tempData[-1]}')
      if tempMaxDiscount == value["discount"]: countMaxDiscount += 1
      if int(temphighest) == int(newPrice): countHighestPrice += 1
      if int(tempLowewstPrice) == int(newPrice): countLowestPrice += 1

  stastDict = {
    "Max_Discount":{"Count":countMaxDiscount,"Discount":tempMaxDiscount},
    "Lowest_Price":{"Count":countLowestPrice,"Price":tempLowewstPrice},
    "Highest_Price":{"Count":countHighestPrice,"Price":temphighest},
    "Free_Games":freeGame
  }

  with open("saved.txt","w") as f:
    f.write(json.dumps(stastDict,indent=4))

