""""
ZeroBite - Food Waste Prevention App: Version 5

This program provides a Tkinter GUI to manage kitchen inventory, donations,
saved recipes, and user dietary preferences. Each user's data (including
preferences) is stored in users.json and used when fetching recipes.
"""

import json  # For reading and writing user data to JSON files
import requests  # Used to access the Spoonacular API for fetching recipe data
import tkinter as tk  # Tkinter provides GUI elements like windows, labels, and buttons
from tkinter import ttk, messagebox  # For dropdowns and popup messages
import sys  # Used to exit the program or handle system-level operations
import webbrowser  # Opens saved recipe links in the user's default web browser
from datetime import datetime, timedelta  # For expiry date handling
import os  # Used for file system operations


# Configuration
DATA_FILE = "users.json"  # Path to JSON file storing all users
API_KEY = "c6d2db224d8e4f90981c17f777bb9521"  # Spoonacular API key for recipes


# JSON Data Management

# load_all_users
"""
    Load all user records from the JSON file.
    Create an empty file if it does not exist.
"""
def load_all_users():

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f, indent=4)  # create empty JSON if missing
    with open(DATA_FILE, "r") as f:
        return json.load(f)  # return dict of users

# save_all_users
"""
    Save the provided dictionary of all users back to the JSON file.
"""
def save_all_users(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)  # persist changes


# CLASS: User
"""
    Represents a single user and provides methods to manage:
    - kitchen items
    - donation items
    - saved recipes
    - preferences
"""
class User:
    def __init__(self, username):
        self.username = username  # store username locally
        data = load_all_users()  # load all users from disk

        # If user record doesn't exist, create default structure including preferences
        if username not in data:
            data[username] = {
                "password": "",
                "kitchen_items": {},
                "donation_items": {},
                "saved_recipes": [],
                "preferences": {
                    "vegetarian": False,
                    "vegan": False,
                    "glutenFree": False,
                    "dairyFree": False,
                    "ketogenic": False
                }
            }
            save_all_users(data)

        # Load preferences into memory
        self.preferences = data[self.username].get("preferences", {
            "vegetarian": False,
            "vegan": False,
            "glutenFree": False,
            "dairyFree": False,
            "ketogenic": False
        })

    # read_items()
    """
        Read and return a specific section of the user's data from users.json.
        Use a filename-like string to determine which section to return.
    """
    def read_items(self, filename):
        data = load_all_users()  # always load fresh data
        user_data = data.get(self.username, {})
        if "kitchen" in filename:
            return user_data.get("kitchen_items", {})
        if "donation" in filename:
            return user_data.get("donation_items", {})
        if "saved_recipes" in filename or "saved" in filename:
            return user_data.get("saved_recipes", [])
        if "preferences" in filename or "prefs" in filename:
            return user_data.get("preferences", {})
        return {}

    # write_items()
    """
        Write updated items into the user's record in users.json.
        The filename string determines which section to update.
    """
    def write_items(self, filename, items):
        data = load_all_users()
        if self.username not in data:
            data[self.username] = {"password": "", "kitchen_items": {}, "donation_items": {}, "saved_recipes": [], "preferences": {}}

        # Map filename to JSON keys
        if "kitchen" in filename:
            data[self.username]["kitchen_items"] = items
        elif "donation" in filename:
            data[self.username]["donation_items"] = items
        elif "saved_recipes" in filename or "saved" in filename:
            data[self.username]["saved_recipes"] = items
        elif "preferences" in filename or "prefs" in filename:
            data[self.username]["preferences"] = items

        save_all_users(data)  # persist to disk

    # save_preferences
    """
        Save preferences to users.json under this user.
    """
    def save_preferences(self):
        self.write_items("preferences", self.preferences)  # save pref dict

    # kitchen_items()
    """
        Open a window to add a kitchen item: name, quantity, unit, expiry days.
        Validate input and save into users.json under kitchen_items.
    """
    def kitchen_items(self):
        root = tk.Tk()
        root.title("Configure Items")
        root.geometry('400x230')

        # Item input field
        tk.Label(root, text="Item").grid(column=0, row=0, padx=8, pady=6)
        item_entry = tk.Entry(root)
        item_entry.grid(column=1, row=0, columnspan=2, pady=6)

        # Quantity input field
        tk.Label(root, text="Quantity").grid(column=0, row=1, padx=8, pady=6)
        quantity_entry = tk.Entry(root)
        quantity_entry.grid(column=1, row=1, pady=6)

        # Unit selection
        tk.Label(root, text="Unit").grid(column=0, row=2, padx=8, pady=6)
        units = ["Cups", "Grams", "Kilograms", "Millilitres", "Litres", "Tablespoons", "Teaspoons", "Pieces", "Slices", "Packs"]
        unit_combobox = ttk.Combobox(root, values=units, state='readonly', width=12)
        unit_combobox.set(units[0])
        unit_combobox.grid(column=1, row=2, padx=5)

        # Expiry days input (optional)
        tk.Label(root, text="Days until expiry").grid(column=0, row=3, padx=8, pady=6)
        expiry_entry = tk.Entry(root)
        expiry_entry.grid(column=1, row=3, pady=6)

        # Save and validate input
        def confirmation():
            item = item_entry.get().capitalize().strip()
            quantity = quantity_entry.get().strip()
            unit = unit_combobox.get()
            expiry_days = expiry_entry.get().strip()

            # Basic validation
            if not item or not quantity:
                messagebox.showerror("Error", "Please enter item name and quantity.")
                return
            try:
                quantity_val = float(quantity)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number.")
                return
            try:
                expiry_int = int(expiry_days) if expiry_days else 7  # default to 7 days
            except ValueError:
                messagebox.showerror("Error", "Expiry must be an integer number of days.")
                return

            # Compute expiry date and update kitchen items
            expiry_date = (datetime.now() + timedelta(days=expiry_int)).strftime("%Y-%m-%d")
            items = self.read_items("kitchen_items.txt")
            if not isinstance(items, dict):
                items = {}
            items[item] = {"quantity": quantity_val, "unit": unit, "expiry": expiry_date}
            self.write_items("kitchen_items.txt", items)  # persist

            root.destroy()
            messagebox.showinfo("Success", f"{item} added with quantity {quantity_val} {unit} (exp {expiry_date})!")
            Info(self.username).main_menu()  # return to main menu

        tk.Button(root, text="Confirm", command=confirmation).grid(column=0, row=4, columnspan=3, pady=10)
        root.mainloop()

    # donation_items()
    """
        Open a window to add donation items (name, quantity, pickup location)
        and save them under donation_items for the user in users.json.
    """
    def donation_items(self):
        root = tk.Tk()
        root.title("Configure Donation Items")
        root.geometry('400x210')

        # Item name input
        tk.Label(root, text="Item").grid(column=0, row=0, padx=8, pady=6)
        item_entry = tk.Entry(root)
        item_entry.grid(column=1, row=0, columnspan=2, pady=6)

        # Quantity input
        tk.Label(root, text="Quantity").grid(column=0, row=1, padx=8, pady=6)
        quantity_entry = tk.Entry(root)
        quantity_entry.grid(column=1, row=1, pady=6)

        # Pickup location input
        tk.Label(root, text="Pickup Location").grid(column=0, row=2, padx=8, pady=6)
        pickup_entry = tk.Entry(root)
        pickup_entry.grid(column=1, row=2, pady=6)

        # Save donation item
        def confirmation():
            item = item_entry.get().capitalize().strip()
            quantity = quantity_entry.get().strip()
            pickup = pickup_entry.get().strip()

            # Validate inputs
            if not item or not quantity or not pickup:
                messagebox.showerror("Error", "Please fill all fields.")
                return
            try:
                quantity_val = float(quantity)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be numeric.")
                return

            donations = self.read_items("donation_items.txt")
            if not isinstance(donations, dict):
                donations = {}
            donations[item] = {"quantity": quantity_val, "pickup": pickup}
            self.write_items("donation_items.txt", donations)  # save

            root.destroy()
            messagebox.showinfo("Success", f"{item} added for donation (pickup: {pickup})!")
            Info(self.username).main_menu()

        tk.Button(root, text="Confirm", command=confirmation).grid(column=0, row=3, columnspan=3, pady=10)
        root.mainloop()

    # preferences_window()
    """
        Open the Preferences window (checkboxes + Save) so the user can set dietary preferences.
        Updates self.preferences and saves them to users.json.
    """
    def preferences_window(self):

        # Use Toplevel instead of a new Tk instance to avoid multiple roots
        pref_win = tk.Toplevel()
        pref_win.title("User Preferences")
        pref_win.geometry("320x320")

        # Heading
        tk.Label(pref_win, text="Dietary Preferences", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(pref_win, text="(Select any that apply)").pack(pady=2)

        # Checkbox variables bound to current preferences
        pref_vars = {}
        for pref_key in ["vegetarian", "vegan", "glutenFree", "dairyFree", "ketogenic"]:
            var = tk.BooleanVar(value=self.preferences.get(pref_key, False))
            chk = tk.Checkbutton(pref_win, text=pref_key.capitalize(), variable=var)
            chk.pack(anchor="w", padx=20, pady=3)
            pref_vars[pref_key] = var  # store reference

        # Save preferences back into JSON
        def save_prefs():
            # Update in-memory preferences
            for k, v in pref_vars.items():
                self.preferences[k] = bool(v.get())

            # Saving preferences
            self.save_preferences()

            messagebox.showinfo("Success", "Preferences updated successfully!")
            pref_win.destroy()  # Close this window only

        # Save button
        tk.Button(pref_win, text="Save Preferences", command=save_prefs).pack(pady=14)

    # recipes()
    """
        Fetch recipes from Spoonacular using the user's kitchen items and preferences.
        Display recipe cards and allow saving recipes into the user's saved_recipes.
    """
    def recipes(self):

        root = tk.Tk()
        root.title("Recipes")
        root.geometry("700x700")

        # Frame to hold everything
        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True)

        # Create canvas + scrollbar
        canvas = tk.Canvas(frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas for content
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Update scrollable region whenever content changes
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)

        # _on_mouse_wheel()
        """
            Allows user to scroll with touchpad or mouse
        """
        def _on_mouse_wheel(event):
            # macOS and Windows send different delta signs/magnitudes
            if event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")  # Scroll down
            elif event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")  # Scroll up


        root.bind_all("<MouseWheel>", _on_mouse_wheel)
        root.bind_all("<Button-4>", _on_mouse_wheel)  # For mac trackpad scroll up
        root.bind_all("<Button-5>", _on_mouse_wheel)  # For mac trackpad scroll down

        # Load kitchen items
        items = self.read_items("kitchen_items.txt")
        if not items:
            tk.Label(inner_frame, text="No kitchen items found.", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        # Build ingredient string for API
        inventory = ','.join(items.keys())
        url = "https://api.spoonacular.com/recipes/findByIngredients"

        # Prepare API parameters including preferences
        params = {"apiKey": API_KEY, "ingredients": inventory, "number": 10, "ranking": 1}

        # Map preferences to Spoonacular parameters
        diet = None
        if self.preferences.get("vegan"):
            diet = "vegan"
        elif self.preferences.get("vegetarian"):
            diet = "vegetarian"
        elif self.preferences.get("ketogenic"):
            diet = "ketogenic"
        if diet:
            params["diet"] = diet  # set diet filter

        # Put dairy/gluten into intolerances if requested
        intolerances = []
        if self.preferences.get("dairyFree"):
            intolerances.append("dairy")
        if self.preferences.get("glutenFree"):
            intolerances.append("gluten")
        if intolerances:
            params["intolerances"] = ",".join(intolerances)

        # Attempt request and handle errors
        try:
            response = requests.get(url, params=params, timeout=10)
        except Exception as e:
            tk.Label(inner_frame, text=f"Error fetching recipes: {e}", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        # Check for API-level errors
        if response.status_code != 200:
            tk.Label(inner_frame, text=f"API Error: {response.status_code} - {response.text}", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        recipes = response.json()
        if not recipes:
            tk.Label(inner_frame, text="No recipes found.", font=("Arial", 12)).pack(pady=20)
            root.mainloop()
            return

        # Display recipes with details and save button
        for recipe in recipes:
            card = tk.Frame(inner_frame, bd=2, relief="groove", padx=10, pady=10)
            card.pack(fill="x", pady=10, padx=20)

            tk.Label(card, text=recipe["title"], font=("Arial", 14, "bold")).pack(pady=5)

            details_text = "Used Ingredients:\n" + "\n".join(i["original"] for i in recipe["usedIngredients"])
            details_text += "\n\nMissing Ingredients:\n" + "\n".join(i["original"] for i in recipe["missedIngredients"])
            tk.Label(card, text=details_text, justify="center").pack(pady=5)

            # Save recipe to user's saved_recipes in users.json
            def save_recipe(r=recipe):
                saved = self.read_items("saved_recipes.txt")
                if not isinstance(saved, list):
                    saved = []
                link = f"https://spoonacular.com/recipes/{r['title'].replace(' ', '-')}-{r['id']}"
                if not any(s.get("title") == r["title"] for s in saved):
                    saved.append({"title": r["title"], "link": link})
                    self.write_items("saved_recipes.txt", saved)  # persist
                    messagebox.showinfo("Saved", f"{r['title']} saved!")
                else:
                    messagebox.showinfo("Info", "Recipe already saved.")

            tk.Button(card, text="Save Recipe", command=save_recipe).pack(pady=5)

        root.mainloop()
        Info(self.username).main_menu()  # return to main menu when done


# CLASS: Info
"""
    Manages the main menu and navigation. Creates a User instance for the logged-in user
    and exposes buttons to manage kitchen, donations, recipes, preferences, and saved recipes.
"""
class Info:
    def __init__(self, username):
        self.username = username
        self.user = User(username)  # create user object linked to username

    # main_menu()
    """
        Show the main menu for the logged-in user with navigation buttons.
    """
    def main_menu(self):
        root = tk.Tk()
        root.title("Main Menu")
        root.geometry("300x440")

        # Use a fresh User instance for button callbacks to ensure up-to-date data
        runUser = User(self.username)

        # Welcome label
        tk.Label(root, text=f"Welcome to ZeroBite, {self.username}!", font=("Arial", 16, "bold")).pack(pady=12)

        # Navigation buttons
        tk.Button(root, text="Manage Kitchen 🍎", width=24, command=runUser.kitchen_items).pack(pady=4)
        tk.Button(root, text="Manage Donations 🎁", width=24, command=runUser.donation_items).pack(pady=4)
        tk.Button(root, text="View Recipes 🍽", width=24, command=runUser.recipes).pack(pady=4)
        tk.Button(root, text="Set Preferences ⚙️", width=24, command=runUser.preferences_window).pack(pady=4)  # open prefs
        tk.Button(root, text="View Kitchen 🥣", width=24, command=self.display_kitchen_item).pack(pady=4)
        tk.Button(root, text="View Donations 📦", width=24, command=self.display_donation_item).pack(pady=4)
        tk.Button(root, text="View Saved Recipes 💾", width=24, command=self.display_saved_recipes).pack(pady=4)
        tk.Button(root, text="Exit ➜]", width=24, command=sys.exit).pack(pady=8)

        root.mainloop()

    # display_kitchen_item()
    """
        Display all kitchen items for the current user, showing quantity/unit/expiry.
    """
    def display_kitchen_item(self):
        root = tk.Tk()
        root.title("Your Kitchen")
        root.geometry("350x350")

        try:
            kitchen = self.user.read_items("kitchen_items.txt")
            if not kitchen:
                tk.Label(root, text="No kitchen items found.").pack(pady=20)
            else:
                # Iterate through items and display them
                for item, data in kitchen.items():
                    if isinstance(data, dict):
                        qty = data.get("quantity")
                        unit = data.get("unit", "")
                        expiry = data.get("expiry", "N/A")
                        tk.Label(root, text=f"{item} - {qty} {unit} (exp: {expiry})").pack(anchor="w", padx=10)
                    else:
                        tk.Label(root, text=f"{item} - {data}").pack(anchor="w", padx=10)
        except Exception:
            tk.Label(root, text="No kitchen_items found or invalid data.").pack(pady=20)

        # Back button returns to main menu
        tk.Button(root, text="Back", command=lambda: [root.destroy(), Info(self.username).main_menu()]).pack(pady=10)
        root.mainloop()

    # display_donation_item()
    """
        Display all donation items from ALL users (community donations)
        with item name, quantity, pickup info, and contributor username.
    """

    def display_donation_item(self):
        root = tk.Tk()
        root.title("Community Donations")
        root.geometry("400x400")

        all_data = load_all_users()
        found_any = False  # Track if there are any donations at all

        for user, info in all_data.items():
            donations = info.get("donation_items", {})
            if donations:
                found_any = True
                # Section label for this user's donations
                tk.Label(root, text=f"From: {user}", font=("Arial", 12, "bold")).pack(pady=5)
                for item, data in donations.items():
                    qty = data.get("quantity", "N/A")
                    pickup = data.get("pickup", "N/A")
                    tk.Label(root, text=f"• {item} - {qty} (Pickup: {pickup})", anchor="w", justify="left").pack(
                        anchor="w", padx=15)

        if not found_any:
            tk.Label(root, text="No community donation items found.").pack(pady=20)

        tk.Button(root, text="Back", command=lambda: [root.destroy(), Info(self.username).main_menu()]).pack(pady=12)
        root.mainloop()

    # display_saved_recipes()
    """
        Show saved recipes from the user's saved_recipes list with clickable links and delete option.
    """
    def display_saved_recipes(self):
        root = tk.Tk()
        root.title("Saved Recipes")
        root.geometry("500x500")

        saved = self.user.read_items("saved_recipes.txt")
        if not saved:
            tk.Label(root, text="No saved recipes found.").pack(pady=20)
            tk.Button(root, text="Back", command=lambda: [root.destroy(), Info(self.username).main_menu()]).pack(pady=10)
            root.mainloop()
            return

        # Display each saved recipe
        for idx, entry in enumerate(saved):
            title = entry.get("title") if isinstance(entry, dict) else str(entry)
            link = entry.get("link") if isinstance(entry, dict) else None

            card = tk.Frame(root, bd=1, relief="solid", padx=6, pady=6)
            card.pack(fill="x", padx=8, pady=6)

            tk.Label(card, text=title, font=("Arial", 12, "bold")).pack(anchor="w")
            if link:
                link_label = tk.Label(card, text=link, fg="white", cursor="hand2")
                link_label.pack(anchor="w")
                link_label.bind("<Button-1>", lambda e, url=link: webbrowser.open(url))

            # Delete saved recipe and refresh view
            def delete_saved(i=idx):
                current = self.user.read_items("saved_recipes.txt")
                if 0 <= i < len(current):
                    current.pop(i)
                    self.user.write_items("saved_recipes.txt", current)
                    messagebox.showinfo("Deleted", "Saved recipe removed.")
                    root.destroy()
                    Info(self.username).display_saved_recipes()

            tk.Button(card, text="Delete", command=delete_saved).pack(anchor="e", pady=4)

        tk.Button(root, text="Back", command=lambda: [root.destroy(), Info(self.username).main_menu()]).pack(pady=10)
        root.mainloop()


# CLASS: LoginWindow
"""
    Handles login and signup screens. Users are stored in users.json with preferences.
"""
class LoginWindow:
    def __init__(self):
        self.data = load_all_users()  # load current user database
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("320x260")

        # Username label + input
        tk.Label(self.root, text="Username").pack(pady=6)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=3)

        # Password label + input
        tk.Label(self.root, text="Password").pack(pady=6)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=3)

        # Login / Signup buttons
        tk.Button(self.root, text="Login", command=self.login).pack(pady=8)
        tk.Button(self.root, text="Sign Up", command=self.signup).pack(pady=3)
        self.root.mainloop()

    # login()
    """
        Verify credentials and open the main menu for that user.
    """
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username in self.data and self.data[username].get("password") == password:
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.root.destroy()
            Info(username).main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # signup()
    """
        Create a new user record and open main menu.
    """
    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username in self.data:
            messagebox.showerror("Error", "Username already exists.")
            return
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        # Create user record with empty items and default preferences
        self.data[username] = {
            "password": password,
            "kitchen_items": {},
            "donation_items": {},
            "saved_recipes": [],
            "preferences": {
                "vegetarian": False,
                "vegan": False,
                "glutenFree": False,
                "dairyFree": False,
                "ketogenic": False
            }
        }
        save_all_users(self.data)  # persist new user
        messagebox.showinfo("Account Created", f"Welcome, {username}!")
        self.root.destroy()
        Info(username).main_menu()


# PROGRAM EXECUTION
if __name__ == "__main__":
    LoginWindow()  # start the app at login screen