import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import Flask,request
from flask_restful import Api,Resource,reqparse
import db
from sqlalchemy.orm import sessionmaker
import re

app = Flask(__name__)
api = Api(app)

urlAgrs = reqparse.RequestParser()
urlAgrs.add_argument("searchkey",type=str,help="Enter the data you want to find (Ex: price)",required=True)
urlAgrs.add_argument("value",type=str,help="Enter the data value you want to find (Ex: 20.99)",required=True)

Session = sessionmaker(bind=db.engine)
session = Session()

def getDiscountData(discount):
  gameDataDict = {}
  for s in session.query(db.transactions).filter(db.transactions.discount == discount):
      gameDataDict[s.gameid] = {
        "name": s.name,
        "price":s.price,
        "discount": s.discount,
        "date":s.date
      }
  return gameDataDict

def getPriceData(price):
  gameDataDict = {}
  for s in session.query(db.transactions).all():
      tempPrice = re.findall('[0-9]+', s.price)
      intPrice = int(float(f'{"".join(tempPrice[0:-1])+"."+tempPrice[-1]}'))
      if intPrice == price:
        gameDataDict[s.gameid] = {
          "name": s.name,
          "price":s.price,
          "discount": s.discount,
        }
  return gameDataDict

def getDateData(date):
  gameDataDict = {}
  for s in session.query(db.transactions).filter(db.transactions.date == date):
      gameDataDict[s.gameid] = {
        "name": s.name,
        "price":s.price,
        "discount": s.discount
      }
  return gameDataDict

class HelloWorld(Resource):
  def get(self):
    args = urlAgrs.parse_args()
    if args["searchkey"] == "discount":
      value = 0
      try:
        value = int(args["value"])
      except:
        return {"message":"Value must be float or integer"}
      return getDiscountData(value)
    if args["searchkey"] == "price":
      value = 0
      try:
        value = int(args["value"])
      except:
        return {"message":"Value must be float or integer"}
      return getPriceData(value)

    if args["searchkey"] == "date":
      return getDateData(args["value"])

api.add_resource(HelloWorld,"/getinfo")


if __name__=="__main__":
  app.run(debug=True)