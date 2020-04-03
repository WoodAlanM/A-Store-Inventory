import csv

from peewee import *

db = SqliteDatabase("inventory.db")


class Entry(Model):
    product_name = CharField(max_length=30)
    product_price = IntegerField()
    product_quantity = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables(Entry, safe=True)


def link_to_csv(csv_name):
    with open(csv_name, newline="") as csvfile:
        inventory_reader = csv.reader(csvfile, delimiter=",")
        rows = list(inventory_reader)
        for row in rows:
            print(row)


def main():

    link_to_csv("inventory.csv")









if __name__ == "__main__":
    main()