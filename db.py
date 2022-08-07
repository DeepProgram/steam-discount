from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///sqlalchemy.sqlite.gameInfo", echo=True)
base = declarative_base()


class Transactions(base):
    __tablename__ = "gameinfo"
    gameid = Column(Integer, primary_key=True)
    name = Column(String)
    ip = Column(String)
    price = Column(String)
    discount = Column(Integer)
    date = Column(String)

    def __init__(self, gameid, name, ip, price, discount, date, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.game_id = gameid
        self.name = name
        self.ip = ip
        self.price = price
        self.discount = discount
        self.date = date


base.metadata.create_all(engine)
 
