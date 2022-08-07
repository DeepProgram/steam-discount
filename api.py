from flask import Flask
from flask_restful import Api, Resource, reqparse
import db
from sqlalchemy.orm import sessionmaker
import re

app = Flask(__name__)
api = Api(app)

url_args = reqparse.RequestParser()
url_args.add_argument("search key", type=str, help="Enter the data you want to find (Ex: price)", required=True)
url_args.add_argument("value", type=str, help="Enter the data value you want to find (Ex: 20.99)", required=True)

Session = sessionmaker(bind=db.engine)
session = Session()


def get_discount_data(discount: int, table: db) -> dict:
    game_data_dict = {}
    for s in session.query(table).filter(table.discount == discount):
        game_data_dict[s.gameid] = {
            "name": s.name,
            "price": s.price,
            "discount": s.discount,
            "date": s.date
        }
    return game_data_dict


def get_price_data(price: int, table: db) -> dict:
    game_data_dict = {}
    for s in session.query(table).all():
        temp_price = re.findall('[0-9]+', s.price)
        int_price = int(float(f'{"".join(temp_price[0:-1]) + "." + temp_price[-1]}'))
        if int_price == price:
            game_data_dict[s.gameid] = {
                "name": s.name,
                "price": s.price,
                "discount": s.discount,
            }
    return game_data_dict


def get_date_data(date: str, table: db) -> dict:
    game_data_dict = {}
    # my_database_table = table
    for s in session.query(table).filter(table.date == date):
        game_data_dict[s.gameid] = {
            "name": s.name,
            "price": s.price,
            "discount": s.discount
        }
    return game_data_dict


class HelloWorld(Resource):
    @staticmethod
    def get() -> dict:
        args = url_args.parse_args()
        if args["search key"] == "discount":
            try:
                value = int(args["value"])
            except ValueError:
                return {"message": "Value must be float or integer"}
            return get_discount_data(value, db.Transactions)
        if args["search key"] == "price":
            try:
                value = int(args["value"])
            except ValueError:
                return {"message": "Value must be float or integer"}
            return get_price_data(value, db.Transactions)

        if args["search key"] == "date":
            return get_date_data(args["value"], db.Transactions)


api.add_resource(HelloWorld, "/getinfo")

if __name__ == "__main__":
    app.run(debug=True)
 
