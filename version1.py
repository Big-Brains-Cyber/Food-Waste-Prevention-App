"""
This program is the first iteration of a food waste prevention app
It will be run in the console and include basic functions such as adding items donations and displaying the items and donations
"""


class User:
    def __init__(self, kitchen_items, donation_items):
        self.kitchen_items = kitchen_items
        self.donation_items = donation_items

    def add_item(self):
        print("************************")
        print("Add New Items")
        print("************************\n")
        item = input("Enter the item: ")
        quantity = int(input("Enter the quantity: "))
        self.kitchen_items.update({item: quantity})

        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()

    def remove_item(self):
        print("************************")
        print("Remove Items")
        print("************************\n")

        item = input("Enter the item: ")
        quantity = int(input("Enter the new quantity: "))

        if quantity == 0:
            self.kitchen_items.pop(item)
        else:
            self.kitchen_items.update({item: quantity})

        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()

    def add_donation(self):
        print("************************")
        print("Add Donation Items")
        print("************************\n")

        item = input("Enter the item: ")
        quantity = int(input("Enter the quantity: "))
        self.donation_items.update({item: quantity})

        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()

    def remove_donation(self):
        print("************************")
        print("Remove Donation Items")
        print("************************\n")

        item = input("Enter the item: ")
        quantity = int(input("Enter the new quantity: "))

        if quantity == 0:
            self.donation_items.pop(item)
        else:
            self.donation_items.update({item: quantity})

        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()


class Info:
    def __init__(self, kitchen_items, donation_items):
        self.kitchen_items = kitchen_items
        self.donation_items = donation_items
    def main_menu(self):
        print("************************")
        print("Main Menu:\n1. Add Items\n2. Remove Items\n3. Add donation\n4. Remove donation\n5. View Kitchen Items\n6. View donation items")
        print("************************\n")

        while True:
            option = int(input("Enter what you would like to do: "))

            if option == 1:
                runUser = User(kitchen_items, donation_items)
                runUser.add_item()
                break
            elif option == 2:
                runUser = User(kitchen_items, donation_items)
                runUser.remove_item()
                break
            elif option == 3:
                runUser = User(kitchen_items, donation_items)
                runUser.add_donation()
                break
            elif option == 4:
                runUser = User(kitchen_items, donation_items)
                runUser.remove_donation()
                break
            elif option == 5:
                Info.display_kitchen_item(self)
                break
            elif option == 6:
                Info.display_donation_item(self)
                break
            else:
                print("That is not an option")

    def display_kitchen_item(self):
        print("************************")
        print("Your Kitchen:")
        print("************************\n")
        for key, value in kitchen_items.items():
            print(f"{key}: {value}")

    def display_donation_item(self):
        print("************************")
        print("Donation Items:")
        print("************************\n")
        for key, value in donation_items.items():
            print(f"{key}: {value}")

kitchen_items = {}
donation_items = {}

user1 = Info(kitchen_items, donation_items)
user1.main_menu()