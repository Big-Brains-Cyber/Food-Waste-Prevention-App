"""
ZeroBite - Food Waste Prevention App: Iteration 4

This program introduces a Tkinter-based GUI, t includes all core features such as adding,
viewing, and managing kitchen and donation items, finding recipes using the Spoonacular API, and saving them.
All data is stored in text files using file management instead of dictionaries.
"""

import requests  # Used to access the Spoonacular API for recipe data
import tkinter as tk  # Tkinter used for GUI elements
from tkinter import ttk, messagebox  # For dropdowns and popups
import sys  # Used to exit the program
import webbrowser  # Opens saved recipe links in browser


# CLASS: User
"""
The User class manages all user actions such as adding kitchen items,
adding donation items, and fetching recipes from the Spoonacular API.
All data is saved in and read from text files.
"""
class User:
    def __init__(self):
        pass

    # read_items()
    """
    Reads items from a given text file and returns them as a dictionary.
    Each item in the file is stored as a key with a placeholder value.
    """
    def read_items(self, filename):
        try:
            with open(filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]  # Removes blank lines
            return {item: True for item in lines}  # Returns dict for quick lookup
        except FileNotFoundError:
            return None

    # write_items()
    """
    Writes a dictionary of items to the given file.
    Each line includes the item name and its quantity/unit.
    """
    def write_items(self, filename, items):
        with open(filename, 'w') as f:
            for item, quantity in items.items():
                f.write(f"{item} {quantity}\n")

    # kicthen_items()
    """
    Opens a Tkinter window allowing users to add kitchen items.
    The item name, quantity, and unit are entered and saved to 'kitchen_items.txt'.
    """
    def kitchen_items(self):
        root = tk.Tk()
        root.title("Configure Items")
        root.geometry('400x200')

        # Item input
        tk.Label(root, text="Item").grid(column=0, row=0)
        item_entry = tk.Entry(root)
        item_entry.grid(column=1, row=0, columnspan=2)

        # Quantity input
        tk.Label(root, text="Quantity").grid(column=0, row=1)
        quantity_entry = tk.Entry(root)
        quantity_entry.grid(column=1, row=1)

        # Units dropdown
        units = ["Cups", "Grams", "Kilograms", "Millilitres", "Litres",
                 "Tablespoons", "Teaspoons", "Pieces", "Slices", "Packs"]
        unit_combobox = ttk.Combobox(root, values=units, state='readonly', width=10)
        unit_combobox.set(units[0])
        unit_combobox.grid(column=3, row=1, padx=5)

        # Confirmation function
        def confirmation():
            item = item_entry.get().capitalize().strip()
            quantity = quantity_entry.get()
            unit = unit_combobox.get()

            # Validate numeric quantity
            try:
                quantity = float(quantity)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for quantity.")
                return

            # Append item to file
            with open("kitchen_items.txt", "a") as file:
                file.write(f"{item} {quantity} {unit}\n")

            root.destroy()
            messagebox.showinfo("Success", f"{item} added with quantity {quantity} {unit}!")

        # Confirm button
        tk.Button(root, text="Confirm", command=confirmation).grid(column=0, row=2, columnspan=3)
        root.mainloop()

    # donation_items()
    """
    Opens a Tkinter window for users to add donation items.
    Saves data to 'donation_items.txt'.
    """
    def donation_items(self):
        root = tk.Tk()
        root.title("Configure Donation Items")
        root.geometry('400x200')

        # Item input
        tk.Label(root, text="Item").grid(column=0, row=0)
        item_entry = tk.Entry(root)
        item_entry.grid(column=1, row=0, columnspan=2)

        # Quantity input
        tk.Label(root, text="Quantity").grid(column=0, row=1)
        quantity_entry = tk.Entry(root)
        quantity_entry.grid(column=1, row=1)

        # Unit selector
        units = ["Cups", "Grams", "Kilograms", "Millilitres", "Litres",
                 "Tablespoons", "Teaspoons", "Pieces", "Slices", "Packs"]
        unit_combobox = ttk.Combobox(root, values=units, state='readonly', width=10)
        unit_combobox.set(units[0])
        unit_combobox.grid(column=3, row=1, padx=5)

        # Confirmation logic
        def confirmation():
            item = item_entry.get().capitalize().strip()
            quantity = quantity_entry.get()
            unit = unit_combobox.get()

            # Validate quantity
            try:
                quantity = float(quantity)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for quantity.")
                return

            # Write donation item to file
            with open("donation_items.txt", "w") as file:
                file.write(f"{item} {quantity} {unit}\n")

            root.destroy()
            messagebox.showinfo("Success", f"{item} added with quantity {quantity} {unit}!")

        # Confirm button
        tk.Button(root, text="Confirm", command=confirmation).grid(column=0, row=2, columnspan=3)
        root.mainloop()

    # recipes()
    """
    Fetches recipes from Spoonacular API using the items in 'kitchen_items.txt'.
    Displays recipes with used/missing ingredients and allows saving recipes.
    """
    def recipes(self):
        root = tk.Tk()
        root.title("Recipes")
        root.geometry("700x700")

        # Scrollable frame setup
        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", on_configure)

        # Read kitchen items
        items = self.read_items("kitchen_items.txt")
        if not items:
            tk.Label(inner_frame, text="No kitchen items found.", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        # Prepare API request
        inventory = ','.join(items.keys())
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "apiKey": "c6d2db224d8e4f90981c17f777bb9521",
            "ingredients": inventory,
            "number": 10,
            "ranking": 1
        }

        # Send API request
        response = requests.get(url, params=params)
        if response.status_code != 200:
            tk.Label(inner_frame, text="Error fetching recipes.", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        recipes = response.json()
        if not recipes:
            tk.Label(inner_frame, text="No recipes found.", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        # Display recipe cards
        for recipe in recipes:
            card = tk.Frame(inner_frame, bd=2, relief="groove", padx=10, pady=10)
            card.pack(fill="x", pady=10, padx=20)

            tk.Label(card, text=recipe["title"], font=("Arial", 14, "bold")).pack(pady=5)

            # Show used/missing ingredients
            details_text = "Used Ingredients:\n" + "\n".join(i["original"] for i in recipe["usedIngredients"])
            details_text += "\n\nMissing Ingredients:\n" + "\n".join(i["original"] for i in recipe["missedIngredients"])
            tk.Label(card, text=details_text, justify="center").pack(pady=5)

            # Save recipe button
            def save_recipe(r=recipe):
                link = f"https://spoonacular.com/recipes/{r['title'].replace(' ', '-')}-{r['id']}"
                with open("saved_recipes.txt", "a") as f:
                    f.write(f"{r['title']} | {link}\n")
                messagebox.showinfo("Saved", f"{r['title']} saved!")

            tk.Button(card, text="Save Recipe", command=save_recipe).pack(pady=5)

        root.mainloop()


# CLASS: Info
"""
The Info class manages the navigation between sections of the app.
It displays the main menu and allows users to view kitchen items,
donations, and saved recipes.
"""
class Info:
    def __init__(self):
        pass

    # main_menu()
    """
    Displays the main menu with buttons for kitchen management,
    donations, recipes, and saved items.
    """
    def main_menu(self):
        root = tk.Tk()
        root.title("Main Menu")
        root.geometry("300x350")

        runUser = User()  # Create instance of User

        # Main menu layout
        tk.Label(root, text="Main Menu", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(root, text="Manage Kitchen", width=20, command=runUser.kitchen_items).pack(pady=5)
        tk.Button(root, text="Manage Donations", width=20, command=runUser.donation_items).pack(pady=5)
        tk.Button(root, text="View Recipes", width=20, command=runUser.recipes).pack(pady=5)
        tk.Button(root, text="View Kitchen", width=20, command=self.display_kitchen_item).pack(pady=5)
        tk.Button(root, text="View Donations", width=20, command=self.display_donation_item).pack(pady=5)
        tk.Button(root, text="View Saved Recipes", width=20, command=self.display_saved_recipes).pack(pady=5)
        tk.Button(root, text="Exit", width=20, command=sys.exit).pack(pady=5)

        root.mainloop()

    # display_kitchen_item()
    """
    Displays all items saved in 'kitchen_items.txt' inside a new window.
    """
    def display_kitchen_item(self):
        root = tk.Tk()
        root.title("Your Kitchen")
        root.geometry("300x300")

        try:
            with open("kitchen_items.txt", 'r') as f:
                lines = f.readlines()
                if not lines:
                    tk.Label(root, text="No kitchen items found.").pack()
                else:
                    for line in lines:
                        tk.Label(root, text=line.strip()).pack()
        except FileNotFoundError:
            tk.Label(root, text="No kitchen_items.txt file found.").pack()

        root.mainloop()

    # display_donation_item()
    """
    Displays all donation items saved in 'donation_items.txt'.
    """
    def display_donation_item(self):
        root = tk.Tk()
        root.title("Donations")
        root.geometry("300x300")

        try:
            with open("donation_items.txt", 'r') as f:
                lines = f.readlines()
                if not lines:
                    tk.Label(root, text="No donations found.").pack()
                else:
                    for line in lines:
                        tk.Label(root, text=line.strip()).pack()
        except FileNotFoundError:
            tk.Label(root, text="No donation_items.txt file found.").pack()

        root.mainloop()

    # display_saved_recipes()
    """
    Displays all saved recipes from 'saved_recipes.txt' with clickable links.
    """
    def display_saved_recipes(self):
        root = tk.Tk()
        root.title("Saved Recipes")
        root.geometry("500x500")

        try:
            with open("saved_recipes.txt", "r") as f:
                lines = f.readlines()
                if not lines:
                    tk.Label(root, text="No saved recipes found.").pack(pady=20)
                    root.mainloop()
                    return
        except FileNotFoundError:
            tk.Label(root, text="No saved recipes found.").pack(pady=20)
            root.mainloop()
            return

        # Display each recipe in a styled frame
        for line in lines:
            line = line.strip()
            if " | " in line:
                title, link = line.split(" | ")
            else:
                title, link = line, None

            card = tk.Frame(root, bd=2, relief="groove", padx=5, pady=5)
            card.pack(fill="x", pady=5, padx=5)

            tk.Label(card, text=title, font=("Arial", 12, "bold")).pack(anchor="w")

            # Add clickable link
            if link:
                link_label = tk.Label(card, text=link, fg="blue", cursor="hand2")
                link_label.pack(anchor="w")
                link_label.bind("<Button-1>", lambda e, url=link: webbrowser.open(url))

        root.mainloop()


# PROGRAM EXECUTION
"""
Creates an Info object and launches the main menu.
"""
user1 = Info()
user1.main_menu()
