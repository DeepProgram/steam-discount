import re
import sys
from datetime import datetime, timedelta


class Stats:
    def __init__(self, session, db):
        self.session = session
        self.db = db

    def get_today_data(self) -> dict:
        game_data_dict = {}
        today = str(datetime.now().date())
        for s in self.session.query(self.db.Transactions).filter(self.db.Transactions.date == today):
            game_data_dict[s.gameid] = {
                "name": s.name,
                "price": s.price,
                "discount": s.discount,
                "date": s.date
            }
        return game_data_dict

    def get_monthly_data(self) -> dict:
        game_data_dict = {}
        today = datetime.now()
        previous_month = str((today.replace(day=1) - timedelta(days=1)).replace(day=today.day).date())
        for s in self.session.query(self.db.Transactions).filter(self.db.Transactions.date >= previous_month,
                                                                 self.db.Transactions.date <= str(today.date())):
            game_data_dict[s.gameid] = {
                "name": s.name,
                "price": s.price,
                "discount": s.discount,
                "date": s.date
            }
        return game_data_dict

    def get_all_data_from_database(self) -> dict:
        game_data_dict = {}
        for s in self.session.query(self.db.Transactions).all():
            game_data_dict[s.gameid] = {
                "name": s.name,
                "price": s.price,
                "discount": s.discount,
                "date": s.date
            }
        return game_data_dict

    @staticmethod
    def get_all_current_stats(game_data_dict: dict) -> list:
        current_max_discount, current_highest_price, current_lowest_price = 0, 0, sys.maxsize
        free_game_list = []
        for key, value in game_data_dict.items():
            if value["discount"] != 100:
                temp_price = re.findall('[0-9]+', value["price"])
                float_price = float(f'{"".join(temp_price[0:-1]) + "." + temp_price[-1]}')
                if float_price > current_highest_price:
                    current_highest_price = float_price
                if float_price < current_lowest_price:
                    current_lowest_price = float_price
                if value["discount"] > current_max_discount:
                    current_max_discount = value["discount"]
            else:
                free_game_list.append(value["name"])
        return [current_max_discount, current_lowest_price, current_highest_price, free_game_list]

    def generate_stats_dictionary(self, game_data_dict: dict) -> dict:
        # Getting all current max discount,highest_price,lowest_price and free games from database
        current_max_discount, current_lowest_price, current_highest_price, free_game_list = self.get_all_current_stats(
            game_data_dict)
        # Now counting the individual category app of maxamount,lowest_price and highest price and returning
        # a dictionary's
        count_max_discount, count_highest_price, count_lowest_price = 0, 0, 0
        for key, value in game_data_dict.items():
            if value["discount"] != 100:
                temp_price = re.findall('[0-9]+', value["price"])
                new_price = float(f'{"".join(temp_price[0:-1]) + "." + temp_price[-1]}')
                if current_max_discount == value["discount"]:
                    count_max_discount += 1
                if int(current_highest_price) == int(new_price):
                    count_highest_price += 1
                if int(current_lowest_price) == int(new_price):
                    count_lowest_price += 1

        return {
            "Max_Discount": {"Count": count_max_discount, "Discount": current_max_discount},
            "Lowest_Price": {"Count": count_lowest_price, "Price": current_lowest_price},
            "Highest_Price": {"Count": count_highest_price, "Price": current_highest_price},
            "Free_Games": {"Count": len(free_game_list), "Game_Names": free_game_list}
        }

    def get_overall_stats(self) -> dict:
        return self.generate_stats_dictionary(self.get_all_data_from_database())

    def get_today_stats(self) -> dict:
        return self.generate_stats_dictionary(self.get_today_data())

    def get_monthly_stats(self) -> dict:
        return self.generate_stats_dictionary(self.get_monthly_data())
 
