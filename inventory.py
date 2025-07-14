from tabulate import tabulate
import re
#========The beginning of the class==========
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """Return the cost of the shoe."""
        return self.cost

    def get_quantity(self):
        """Return the quantity of the shoe in stock."""
        return self.quantity

    def __str__(self):
        """String representation of the Shoe object."""
        return (
            f"{self.country} | {self.code} | {self.product} | "
            f"R{self.cost} | Qty: {self.quantity}"
        )

#=============Shoe list===========

shoe_list = []
#==========Functions outside the class==============

def read_shoes_data():
    try:
        with open ("inventory.txt","r") as file:
            for count,lines in enumerate(file):
                if count > 0:
                    line = lines.strip().split(",")
                    shoe_list.append(Shoe(line[0], line[1], line[2], line[3], line[4]))
    except FileNotFoundError:
        print("Error: 'inventory.txt' file not found")

def capture_shoes():
    print("Please capture the following details:")

    # Country input
    info_coun = input("The country:\n")
    while info_coun.strip() == "":
        print("You have not entered anything. Please try again:")
        info_coun = input()

    # Product code input

    # Extract all product codes from the shoe list for validation
    codes = [shoe.code for shoe in shoe_list]

    while True:
        info_code = input("Enter the product code (e.g. SKU44386): ").strip().upper()

        # Validate format: must start with 'SKU' followed by digits
        if re.fullmatch(r'SKU\d+', info_code):
            if info_code in codes:
                # code already in the system
                print("This product code already exists, please try again.")
                continue
            # Valid and found — break the loop
            break
        else:
            # Format is invalid — prompt user again
            print(
                "Invalid code. Please enter a code in the format 'SKU' "
                "followed by numbers (e.g. SKU12345)."
            )

    # Product name input
    info_prod = input("The product name:\n")

    # Cost input with validation
    while True:
        try:
            info_cost = int(input("The cost:\n"))
            if info_cost <= 0:
                print("Cost cannot be zero or negative. Please try again.")
                continue
            break
        except ValueError:
            print("Input error. Please enter a valid number.")

    # Quantity input with validation
    while True:
        try:
            info_quant = int(input("Product quantity:\n"))
            if info_quant <= 0:
                print("Quantity cannot be less than or equal to zero. Please try again.")
                continue
            break
        except ValueError:
            print("Input error. Please enter a valid whole number.")
    shoe_list.append(Shoe(info_coun,info_code, info_prod,
                           info_cost, info_quant))
    with open("inventory.txt","a") as file :
        file.write(f"\n{info_coun},{info_code},{info_prod},{info_cost},{info_quant}")
    print("Inventory file and list has been updates!")


def view_all():
    """Prints each product in table form"""

    headings =["Country", "Code", "Product", "Cost", "Quantity"]

    # Creaing a list by interating through shoe_list as shoe and pulling each attribute
    data = [[shoe.country, shoe.code, shoe.product,
            shoe.cost, shoe.quantity ] for shoe in shoe_list ]
    # Printing in table formate
    print((tabulate(data, headers = headings, tablefmt = "fancy_grid")))


def re_stock():


    # Create list of all quantities
    quantities = [int(shoe.quantity) for shoe in shoe_list]

    # Determine minimum quantity
    low_quantity = min(quantities)

    for shoe in shoe_list:
        if int(shoe.quantity) == low_quantity:
            print("The shoe with the lowest quantity is:")
            print(shoe)

            print("Would you like to add more stock? Yes or No")

            while True:
                choice = input().lower()
                if choice not in ["yes", "no"]:
                    print("Please answer Yes or No")
                    continue
                break

            if choice == "yes":
                print("How much product would you like to add?")
                while True:
                    try:
                        add_prod = int(input())

                        if add_prod <= 0:
                            print("Quantity cannot be less than or equal to zero. Please try again.")
                            continue

                        shoe.quantity = int(shoe.quantity) + add_prod
                        break

                    except ValueError:
                        print("Input error. Please enter a valid whole number.")


    with open("inventory.txt","w") as w:
        w.write(f"Country,Code,Product,Cost,Quantity")
        for shoe in shoe_list:
            w.write(f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}")
    print("Restock complete!!")



def search_shoe():

    # Extract all product codes from the shoe list for validation
    codes = [shoe.code for shoe in shoe_list]


    while True:
        search_code = input("Enter the product code (e.g. SKU44386): ").strip().upper()

        # Validate format: must start with 'SKU' followed by digits
        if re.fullmatch(r'SKU\d+', search_code):
            if search_code not in codes:
                # Format is valid but code doesn't exist in the system
                print("Code not in system, please enter a valid code.")
                continue
            # Valid and found — break the loop
            break
        else:
            # Format is invalid — prompt user again
            print(
                "Invalid code. Please enter a code in the format 'SKU' "
                "followed by numbers (e.g. SKU12345)."
            )

    # Search for the matching shoe and print its details
    for shoe in shoe_list:
        if shoe.code == search_code:
            print(shoe)  # Assumes __str__ is defined in the Shoe class


def value_per_item():
    print("Product Value:\n")
    
    processed = set()  # To track which products we already calculated

    for shoe in shoe_list:
        if shoe.product in processed:
            continue

        total_value = 0

        # Sum value for all shoes with the same product name
        for item in shoe_list:
            if item.product == shoe.product:
                total_value += float(item.cost) * int(item.quantity)

        # Display total value for this product
        print(f"{shoe.product:<25} R{total_value:.2f}")
        print("_____________________________")

        processed.add(shoe.product)


def highest_qty():

    print("The following shoe(s) is/are marked for sale (highest quantity):\n")

    # Determine the maximum quantity
    max_quantity = max(int(shoe.quantity) for shoe in shoe_list)

    # Print all shoes that match the max quantity
    for shoe in shoe_list:
        if int(shoe.quantity) == max_quantity:
            print(f"{shoe.product:<30} Quantity: {shoe.quantity}")


#==========Main Menu=============
read_shoes_data()  # Data to be stored in shoe_list

print("""
Please select the action you would like to take:

Menu options:
    c  - Capture data
    v  - View all product data
    r  - Restock
    s  - Search for a product
    vs - Print the value of each item in stock
    sa - Determine which product must go on sale
    e  - Exit
""")

menu = input(": ").lower()

while menu not in ["c", "v", "r", "s", "vs", "sa", "e"]:
    menu = input("Invalid input, please try again: ").lower()

while menu != "e":
    if menu == "c":
        capture_shoes()
    elif menu == "v":
        view_all()
    elif menu == "r":
        re_stock()
    elif menu == "s":
        search_shoe()
    elif menu == "vs":
        value_per_item()
    elif menu == "sa":
        highest_qty()

    print()
    menu = input("Which action would you like to take next? ").lower()
    while menu not in ["c", "v", "r", "s", "vs", "sa", "e"]:
        menu = input("Invalid input, please try again: ").lower()

print("Goodbye!")
