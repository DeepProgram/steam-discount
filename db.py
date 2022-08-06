from sqlalchemy import create_engine
from sqlalchemy import Column,String,Float,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sqlalchemy.sqlite.gameInfo",echo=True)
base = declarative_base()

class transactions(base):
  __tablename__ = "gameinfo"
  gameid = Column(Integer,primary_key=True)
  name = Column(String)
  ip = Column(String)
  price = Column(String)
  discount = Column(Integer)
  date = Column(String)

  def __init__(self,gameid,name,ip,price,discount,date):
    self.gameid= gameid
    self.name = name
    self.ip = ip
    self.price = price
    self.discount = discount
    self.date = date


base.metadata.create_all(engine)