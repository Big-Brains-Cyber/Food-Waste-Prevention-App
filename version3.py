"""
ZeroBite - Food Waste Prevention App: Iteration 3

This program uses file management instead of dictionaries, it will be run in the console,
and include basic functions such as adding items, donations, and displaying them,
but now all data is saved in and read from text files and includes a recipe finder using the Spoonacular API.
"""

import requests  # Used to make HTTP requests to the Spoonacular recipe API


# CLASS: User
"""
The User class manages all user-related actions in the app.
It allows adding, updating, and removing kitchen and donation items stored in text files.
In this version, it also connects to the Spoonacular API to find recipes based on ingredients in the user’s kitchen.
"""
class User:
    def __init__(self):
        pass

    # read_items()
    """
    Reads a list of items and quantities from the given text file.
    Returns a dictionary with item names as keys and quantities as values.
    If the file doesn’t exist, it returns an empty dictionary.
    """
    def read_items(self, filename):
        items = {}
        try:
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        items[parts[0].lower()] = int(parts[1])
        except FileNotFoundError:
            pass
        return items

    # write_items()
    """
    Saves the given items dictionary to the specified file.
    Each line in the file contains an item name and its quantity.
    """
    def write_items(self, filename, items):
        with open(filename, 'w') as f:
            for item, quantity in items.items():
                f.write(f"{item} {quantity}\n")

    # add_item()
    """
    Prompts the user to add or update an item in their kitchen.
    Ensures that the quantity entered is a valid number.
    Updates the 'kitchen_items.txt' file with the new data.
    """
    def add_item(self):
        print("************************")
        print("Add New Items")
        print("************************\n")
        item = input("Enter the item: ").strip().lower()  # Get item input from user

        # Validate that the quantity is an integer
        while True:
            try:
                quantity = int(input("Enter the quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        # Read kitchen items, update, and save to file
        items = self.read_items("kitchen_items.txt")
        items[item] = quantity
        self.write_items("kitchen_items.txt", items)

        # Return to main menu
        information = Info()
        information.main_menu()

    # remove_item()
    """
    Allows the user to update or delete an item from their kitchen list.
    If the new quantity is set to 0, the item is deleted from the file.
    """
    def remove_item(self):
        print("************************")
        print("Remove Items")
        print("************************\n")

        item = input("Enter the item: ").strip().lower()

        # Validate numeric input
        while True:
            try:
                quantity = int(input("Enter the new quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        items = self.read_items("kitchen_items.txt")

        if item in items:
            if quantity == 0:
                del items[item]  # Remove item completely
            else:
                items[item] = quantity  # Update its quantity
            self.write_items("kitchen_items.txt", items)
        else:
            print(f"Item '{item}' not found.")

        information = Info()
        information.main_menu()

    # add_donation()
    """
    Prompts the user to add or update a donation item.
    Saves the updated list to 'donation_items.txt'.
    """
    def add_donation(self):
        print("************************")
        print("Add Donation Items")
        print("************************\n")

        item = input("Enter the item: ").strip().lower()

        # Validate quantity input
        while True:
            try:
                quantity = int(input("Enter the quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        # Read, update, and save donation data
        items = self.read_items("donation_items.txt")
        items[item] = quantity
        self.write_items("donation_items.txt", items)

        information = Info()
        information.main_menu()

    # remove_donation()
    """
    Lets the user remove or update a donation item.
    If the quantity entered is 0, the item is deleted from 'donation_items.txt'.
    """
    def remove_donation(self):
        print("************************")
        print("Remove Donation Items")
        print("************************\n")

        item = input("Enter the item: ").strip().lower()

        while True:
            try:
                quantity = int(input("Enter the new quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        items = self.read_items("donation_items.txt")

        if item in items:
            if quantity == 0:
                del items[item]
            else:
                items[item] = quantity
            self.write_items("donation_items.txt", items)
        else:
            print(f"Item '{item}' not found.")

        information = Info()
        information.main_menu()

    # recipes()
    """
    Uses the Spoonacular API to find recipes based on ingredients 
    currently listed in 'kitchen_items.txt'. Displays recipe names,
    used ingredients, and missing ingredients to the user.
    """
    def recipes(self):
        items = self.read_items("kitchen_items.txt")

        # Combine kitchen ingredients into a comma-separated list
        inventory = ','.join(items.keys())

        # API endpoint and parameters
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "apiKey": "c6d2db224d8e4f90981c17f777bb9521",
            "ingredients": inventory,
            "number": 5,  # Return top 5 recipes
            "ranking": 1,  # Maximise use of available ingredients
        }

        # Send request to API
        response = requests.get(url, params=params)

        # If successful, display recipe results
        if response.status_code == 200:
            recipes = response.json()

            for recipe in recipes:
                print("\n************************")
                print("Title:", recipe["title"])
                print("Used Ingredients:")
                for ingredients in recipe["usedIngredients"]:
                    print(ingredients["original"])
                print("Missing Ingredients:")
                for ingredients in recipe["missedIngredients"]:
                    print(ingredients["original"])
        else:
            print("Error:", response.status_code, response.text)

        information = Info()
        information.main_menu()


# CLASS: Info
"""
The Info class handles user interaction and navigation.
It provides the main menu, allowing users to choose between
adding, removing, viewing, and generating recipes from their items.
"""
class Info:
    def __init__(self):
        pass

    # main_menu()
    """
    Displays the main menu options and handles user selection.
    Routes each option to the corresponding function in the User class.
    """
    def main_menu(self):
        runUser = User()
        while True:
            print("\n************************")
            print(
                "Main Menu:\n1. Add Items\n2. Remove Items\n3. Add donation\n4. Remove donation\n5. View Kitchen Items\n6. View donation items\n7. View Recipes\n8. Exit")
            print("************************\n")

            try:
                option = int(input("Enter what you would like to do: "))

                if option == 1:
                    runUser.add_item()
                elif option == 2:
                    runUser.remove_item()
                elif option == 3:
                    runUser.add_donation()
                elif option == 4:
                    runUser.remove_donation()
                elif option == 5:
                    self.display_kitchen_item()
                elif option == 6:
                    self.display_donation_item()
                elif option == 7:
                    runUser.recipes()
                elif option == 8:
                    print("Goodbye!")
                    exit()
                else:
                    print("That is not an option")
            except ValueError:
                print("Please enter a number from 1 to 8.")

    # display_kitchen_item()
    """
    Reads and displays all kitchen items from 'kitchen_items.txt'.
    If the file does not exist or is empty, it notifies the user.
    """
    def display_kitchen_item(self):
        print("************************")
        print("Your Kitchen:")
        print("************************\n")
        try:
            with open("kitchen_items.txt", 'r') as f:
                lines = f.readlines()
                if not lines:
                    print("No kitchen items found.")
                for line in lines:
                    print(line.strip())
        except FileNotFoundError:
            print("No kitchen_items.txt file found.")

        information = Info()
        information.main_menu()

    # display_donation_item()
    """
    Reads and displays all donation items from 'donation_items.txt'.
    If the file does not exist or is empty, it displays a message.
    """
    def display_donation_item(self):
        print("************************")
        print("Donation Items:")
        print("************************\n")
        try:
            with open("donation_items.txt", 'r') as f:
                lines = f.readlines()
                if not lines:
                    print("No donation items found.")
                for line in lines:
                    print(line.strip())
        except FileNotFoundError:
            print("No donation_items.txt file found.")

        information = Info()
        information.main_menu()


# PROGRAM EXECUTION
# Creates the Info object and runs the main menu
user1 = Info()
user1.main_menu()
