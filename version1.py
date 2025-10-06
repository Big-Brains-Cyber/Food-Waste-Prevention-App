"""
This program is the first iteration of a food waste prevention app.
It runs in the console and includes basic functions such as adding items,
adding donations, and displaying both the kitchen and donation inventories.
The data is stored in dictionaries within the program while it runs.
"""


# CLASS: User
"""
The User class handles all the actions the user can perform, such as 
adding or removing items from their kitchen or donation list. 
It updates the dictionaries and then returns to the main menu.
"""
class User:
    def __init__(self, kitchen_items, donation_items):
        # Initialize with the current kitchen and donation dictionaries
        self.kitchen_items = kitchen_items
        self.donation_items = donation_items

    # add_item
    """
    Adds a new item and its quantity to the kitchen_items dictionary.
    The user is prompted for the item name and quantity, which are then stored.
    """
    def add_item(self):
        print("************************")
        print("Add New Items")
        print("************************\n")

        # Get item name and quantity from the user
        item = input("Enter the item: ")
        quantity = int(input("Enter the quantity: "))

        # Add or update the item in the kitchen dictionary
        self.kitchen_items.update({item: quantity})

        # Return to the main menu
        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()

    # remove_item
    """
    Updates or removes an existing kitchen item. 
    If the new quantity entered is zero, the item is deleted; 
    otherwise, the quantity is updated.
    """
    def remove_item(self):
        print("************************")
        print("Remove Items")
        print("************************\n")

        # Ask user which item to modify and the new quantity
        item = input("Enter the item: ")
        quantity = int(input("Enter the new quantity: "))

        # Remove or update the item
        if quantity == 0:
            self.kitchen_items.pop(item)
        else:
            self.kitchen_items.update({item: quantity})

        # Return to main menu
        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()

    # add_donation
    """
    Adds a new item and its quantity to the donation_items dictionary.
    Used when users wish to donate leftover food.
    """
    def add_donation(self):
        print("************************")
        print("Add Donation Items")
        print("************************\n")

        # Get item name and quantity
        item = input("Enter the item: ")
        quantity = int(input("Enter the quantity: "))

        # Add to donation list
        self.donation_items.update({item: quantity})

        # Return to main menu
        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()

    # remove_donation
    """
    Updates or removes an existing donation item.
    If the quantity entered is zero, the item is deleted from the donation list.
    """
    def remove_donation(self):
        print("************************")
        print("Remove Donation Items")
        print("************************\n")

        # Get item name and new quantity
        item = input("Enter the item: ")
        quantity = int(input("Enter the new quantity: "))

        # Remove or update the item
        if quantity == 0:
            self.donation_items.pop(item)
        else:
            self.donation_items.update({item: quantity})

        # Return to main menu
        information = Info(self.kitchen_items, self.donation_items)
        information.main_menu()


# CLASS: Info
"""
The Info class manages the display and navigation of information.
It contains the main menu and functions to display kitchen or donation items.
"""
class Info:
    def __init__(self, kitchen_items, donation_items):
        # Store the dictionaries that track kitchen and donation items
        self.kitchen_items = kitchen_items
        self.donation_items = donation_items

    # main_menu
    """
    Displays the main menu and handles user navigation.
    The user can choose to add, remove, or view items and donations.
    """
    def main_menu(self):
        print("************************")
        print(
            "Main Menu:\n"
            "1. Add Items\n"
            "2. Remove Items\n"
            "3. Add donation\n"
            "4. Remove donation\n"
            "5. View Kitchen Items\n"
            "6. View donation items"
        )
        print("************************\n")

        # Continuously prompt until a valid option is selected
        while True:
            option = int(input("Enter what you would like to do: "))

            # Perform actions based on user's selection
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

    # display_kitchen_item
    """
    Displays all items currently stored in the kitchen_items dictionary.
    """
    def display_kitchen_item(self):
        print("************************")
        print("Your Kitchen:")
        print("************************\n")
        for key, value in kitchen_items.items():
            print(f"{key}: {value}")

    # display_donation_item
    """
    Displays all items currently stored in the donation_items dictionary.
    """
    def display_donation_item(self):
        print("************************")
        print("Donation Items:")
        print("************************\n")
        for key, value in donation_items.items():
            print(f"{key}: {value}")


# MAIN PROGRAM
"""
The main program creates two empty dictionaries to store kitchen and donation items.
It then creates an Info object and starts the program by displaying the main menu.
"""

# Create dictionaries to store kitchen and donation data
kitchen_items = {}
donation_items = {}

# Instantiate the Info class and run the main menu
user1 = Info(kitchen_items, donation_items)
user1.main_menu()
