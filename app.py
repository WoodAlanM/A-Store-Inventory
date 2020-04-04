import csv
from datetime import datetime

from peewee import *

db = SqliteDatabase("inventory.db")


class Product(Model):
    product_id = AutoField()
    product_name = CharField(max_length=30, unique=True)
    product_price = IntegerField(default=0)
    product_quantity = IntegerField(default=0)
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
    for i in range(1, len(product_names)):
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
        try:
            Product.create(product_name=product_names[i],
                           product_price=price,
                           product_quantity=quantity,
                           date_updated=date
                           )
        except IntegrityError:
            continue


def menu_loop():
    menu_is_open = True

    while menu_is_open:
        print("Please choose from the following options.")
        print("\n")
        print("v) View single item.")
        print("a) Add item to the database.")
        print("b) Backup the database to csv.")
        print("q) Quit.")
        print("\n")
        choice = input("Please make a selection: ")
        if not choice.isalpha():
            print("Please only choose from the menu.")
            continue
        elif choice == "V" or choice == "v":
            print("\n")
            getting_entries = True
            while getting_entries:
                id_number = input("Please enter a product ID number (0 to quit): ")
                if not id_number.isdigit():
                    print("\n")
                    print("Please only enter numbers.")
                    continue
                elif id_number == "0":
                    getting_entries = False
                else:
                    print("Checking the database...")
                    print("\n")
                    query = get_entries(id_number.strip())
                    if not query:
                        print("No such entry in the database.")
                        print("\n")
                        continue
                    else:
                        query_id = query[0]
                        query_name = query[1]
                        query_price = query[2]
                        query_quantity = query[3]
                        query_date = query[4]
                        print("ID number: {}".format(query_id))
                        print("Name: {}".format(query_name))
                        print("Price: {}".format(query_price))
                        print("Quantity: {}".format(query_quantity))
                        print("Date Updated: {}".format(query_date))
                        print("\n")
                        continue
        elif choice == "A" or choice == "a":
            entering = True
            while entering:
                name = input("Please enter a product name: ")
                if name.isalpha():
                    price = input("Please enter the product price in cents: ")
                    if price.isdigit():
                        quantity = input("Please enter the quantity of the item: ")
                        if quantity.isdigit():
                            print("Thank you, your product has been added.")
                            Product.create(product_name=name,
                                           product_price=price,
                                           product_quantity=quantity,
                                           date_updated=datetime.strftime(datetime.now(), "%Y-%m-%d")
                                           )
                            entering = False
                            print("\n")
                        else:
                            print("Please only enter a number.")
                            continue
                    else:
                        print("Please only enter a number.")
                        continue
                else:
                    print("Please only enter letters.")
                    continue
        elif choice == "B" or choice == "b":
            print("Backing up database to csv...")
            backup_to_csv()
        elif choice == "Q" or choice == "q":
            menu_is_open = False
        else:
            print("Please only choose from the menu.")


def backup_to_csv():
    list_of_products = Product.select().order_by(Product.product_id)

    with open("backup.csv", "a", newline="") as csvfile:
        field_names = ["product_name", "product_price", "product_quantity", "date_updated"]
        backup_writer = csv.writer(csvfile)
        backup_writer.writerow(field_names)
        for product in list_of_products:
            write_list = [product.product_name, product.product_price, product.product_quantity, product.date_updated]
            backup_writer.writerow(write_list)


def get_entries(search):
    return_list = []
    products = Product.select().order_by(Product.product_id)
    try:
        products = products.where(Product.product_id == search)
        for product in products:
            return_list.append(product.product_id)
            return_list.append(product.product_name)
            return_list.append(product.product_price)
            return_list.append(product.product_quantity)
            return_list.append(datetime.strftime(product.date_updated, "%B %d %Y"))
        return return_list
    except:
        return False


if __name__ == "__main__":
    initialize()
    add_data("inventory.csv")
    menu_loop()
    db.close()
