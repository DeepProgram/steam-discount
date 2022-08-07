import requests
from bs4 import BeautifulSoup
import json
from datetime import date
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
import db


class ScrapData:
    def __init__(self, passed_session: sessionmaker(), passed_db: db, passed_credentials: dict):
        self.session = passed_session
        self.db = passed_db
        self.credentials = passed_credentials

    def if_already_exist_in_database(self, appid: int) -> bool:
        return self.session.query(exists().where(self.db.Transactions.gameid == appid)).scalar()

    def update_in_database(self, appid: int, discount: int):
        self.session.query(self.db.Transactions).filter(self.db.Transactions.gameid == appid,
                                                        self.db.Transactions.discount != discount).update(
            {"discount": discount})

    def insert_in_database(self, appid: int, game_info: dict):
        tr = self.db.Transactions(appid, game_info["name"], game_info["ip"], game_info["price"], game_info["discount"],
                                  game_info["date"])
        self.session.add(tr)

    def scrap_data(self):
        start_from = 0
        while start_from <= self.credentials["search_amount"]:
            param = {
                "query": "",
                "start": start_from,
                "count": "50",
                "dynamic_data": "",
                "sort_by": "_ASC",
                "filter": "topsellers",
                "infinite": "1"
            }
            res = None
            try:
                res = requests.get("https://store.steampowered.com/search/results/", params=param)
            except Exception as e:
                print(f"Error Occurred On Requesting.. {e}")

            ip = res.cookies.get_dict()['steamCountry'][0:2]
            m = json.loads(res.text)
            soup = BeautifulSoup(m["results_html"], "html.parser")

            for link in soup.find_all({"a": "href"}):
                try:
                    appid = int(link["href"].split("/app/")[1].split("/")[0])
                except IndexError:
                    continue
                name = link.find("div", attrs={"class": "responsive_search_name_combined"}).div.span.text
                price_section = link.find("div",
                                          attrs={"class": "col search_price_discount_combined responsive_secondrow"})

                price = price_section.contents[3]
                discount = price_section.div.span
                if discount:
                    discount = int(discount.text[1:-1])
                else:
                    continue
                if price.span is None:
                    price = price.text.strip()
                else:
                    price = price.contents[-1].strip()

                game_info = {
                    "name": name,
                    "ip": ip,
                    "price": price,
                    "date": str(date.today()),
                    "discount": discount
                }

                if_game_exist = self.if_already_exist_in_database(appid)  # Checking if the game id already exist or not
                if if_game_exist:
                    self.update_in_database(appid, game_info[
                        "discount"])  # If exist calling a function to update that in database
                # If game don't exist then check discount is greater than zero
                # and if true add it in database by calling another function
                elif game_info["discount"] > 0:
                    self.insert_in_database(appid, game_info)

            start_from += 50
        self.session.commit()  # Saving the changes in the database

 
