"""
ZeroBite - Food Waste Prevention App: Iteration 2

This program uses file management instead of dictionaries, tt will be run in the console,
and include basic functions such as adding items, donations, and displaying them,
but now all data is saved in and read from text files to make it more persistent between sessions.
"""

# CLASS: User
"""
The User class manages all user actions related to kitchen and donation items.
It allows reading and writing data from files, adding new items, updating quantities, 
and removing items when quantities reach zero. 
This class replaces in-memory storage with file-based management for data persistence.
"""
class User:
    def __init__(self):
        pass

    # read_items()
    """
    Reads all items and their quantities from a specified file.
    Returns a dictionary where keys are item names and values are quantities.
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
            # If the file doesn't exist yet, it just returns an empty dictionary
            pass
        return items

    # write_items()
    """
    Writes all items and their quantities from a dictionary into a text file.
    This overwrites the existing file, ensuring the latest data is always saved.
    """
    def write_items(self, filename, items):
        with open(filename, 'w') as f:
            for item, quantity in items.items():
                f.write(f"{item} {quantity}\n")

    # add_item()
    """
    Prompts the user to add a new kitchen item or update its quantity.
    Input is validated to ensure the quantity is a number.
    The updated data is then written to 'kitchen_items.txt'.
    """
    def add_item(self):
        print("************************")
        print("Add New Items")
        print("************************\n")
        item = input("Enter the item: ").strip().lower()  # Get item name from user

        # Validate that quantity is an integer
        while True:
            try:
                quantity = int(input("Enter the quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        # Read, update, and save kitchen items
        items = self.read_items("kitchen_items.txt")
        items[item] = quantity
        self.write_items("kitchen_items.txt", items)

        # Return to main menu
        information = Info()
        information.main_menu()

    # remove_item()
    """
    Allows the user to update or remove a kitchen item.
    If the new quantity is 0, the item will be deleted from the file.
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

        # Update or remove item if it exists
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
    Prompts the user to add new donation items and quantities.
    Saves or updates this data in 'donation_items.txt'.
    """
    def add_donation(self):
        print("************************")
        print("Add Donation Items")
        print("************************\n")

        item = input("Enter the item: ").strip().lower()

        # Validate numeric input
        while True:
            try:
                quantity = int(input("Enter the quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        # Read, update, and write donation items
        items = self.read_items("donation_items.txt")
        items[item] = quantity
        self.write_items("donation_items.txt", items)

        information = Info()
        information.main_menu()

    # remove_donation()
    """
    Allows the user to update or remove donation items.
    If quantity is set to 0, the item will be deleted from 'donation_items.txt'.
    """
    def remove_donation(self):
        print("************************")
        print("Remove Donation Items")
        print("************************\n")

        item = input("Enter the item: ").strip().lower()

        # Validate numeric input
        while True:
            try:
                quantity = int(input("Enter the new quantity: "))
                break
            except ValueError:
                print("Please enter a number for the quantity")

        items = self.read_items("donation_items.txt")

        if item in items:
            if quantity == 0:
                del items[item]  # Delete donation item
            else:
                items[item] = quantity  # Update quantity
            self.write_items("donation_items.txt", items)
        else:
            print(f"Item '{item}' not found.")

        information = Info()
        information.main_menu()


# CLASS: Info
"""
The Info class handles user navigation and displaying stored data.
It provides the main menu interface, allowing users to choose actions 
like adding, removing, or viewing kitchen and donation items.
"""
class Info:
    def __init__(self):
        pass

    # main_menu()
    """
    Displays the main menu options and directs the user to the chosen function.
    Includes input validation to ensure correct choices.
    """
    def main_menu(self):
        print("************************")
        print("Main Menu:\n1. Add Items\n2. Remove Items\n3. Add donation\n4. Remove donation\n5. View Kitchen Items\n6. View donation items")
        print("************************\n")

        while True:
            try:
                option = int(input("Enter what you would like to do: "))
                runUser = User()  # Create a new User object

                # Handle each menu option
                if option == 1:
                    runUser.add_item()
                    break
                elif option == 2:
                    runUser.remove_item()
                    break
                elif option == 3:
                    runUser.add_donation()
                    break
                elif option == 4:
                    runUser.remove_donation()
                    break
                elif option == 5:
                    self.display_kitchen_item()
                    break
                elif option == 6:
                    self.display_donation_item()
                    break
                else:
                    print("That is not an option")
            except ValueError:
                print("Please enter a number from 1 to 6.")

    # display_kitchen_item()
    """
    Reads and displays all kitchen items from 'kitchen_items.txt'.
    If the file doesn’t exist or is empty, it notifies the user.
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

    # display_donation_item()
    """
    Reads and displays all donation items from 'donation_items.txt'.
    Notifies the user if the file doesn’t exist or is empty.
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


# PROGRAM EXECUTION
# Create an Info object and start the main menu
user1 = Info()
user1.main_menu()