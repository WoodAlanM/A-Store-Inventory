import csv
from datetime import datetime

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=30)
    product_price = IntegerField()
    product_quantity = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


def add_data(csv_name):
    with open(csv_name, newline="") as csvfile:
        inventory_reader = csv.reader(csvfile, delimiter=",")
        rows = list(inventory_reader)
        product_names = []
        product_prices = []
        product_quantities = []
        dates = []
        for row in rows:
            product_names.append(row[0])
            product_prices.append(row[1])
            product_quantities.append(row[2])
            dates.append(row[3])
        for i in range(1, len(product_names) - 1):
            # This strips the dollar sign and changes the price
            # to cents
            price_string = product_prices[i]
            price_list = list(price_string)
            del price_list[0]
            price = ""
            price = int(float(price.join(price_list)) * 100)
            # This changes the date string to a date
            date = datetime.strptime(dates[i], "%m/%d/%Y").date()
            # Changes quantity to integer
            quantity = int(product_quantities[i])
            # Creates a new entry in the database
            Product.create(product_name=product_names[i],
                           product_price=price,
                           product_quantity=quantity,
                           date_updated=date
                           )


def main():
    initialize()
    add_data("inventory.csv")









if __name__ == "__main__":
    main()