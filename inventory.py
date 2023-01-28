
#======== Import libraries ==========
from os.path import exists
from tabulate import tabulate

#======== Set up Shoe class and methods ==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        """ Constructor for class Shoe. """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_code(self):
        """ Return the code of the shoe in this method. """
        return (self.code)

    def get_cost(self):
        """ Return the cost of the shoe as an integer in this method. """
        return (int(self.cost))

    def get_quantity(self):
        """ Return the quantity of the shoes as an integer. """
        return (int(self.quantity))

    def __str__(self):
        """ Return a string representation of a Shoe class (detail view). """
        return (f"Country :\t{self.country}\n"
                f"Code :\t\t{self.code}\n"
                f"Product :\t{self.product}\n"
                f"Cost :\t\t{self.cost}\n"
                f"Quantity :\t{self.quantity}\n")

    def tabular_list(self):
        """ Return a list of Shoe instances to be used by tabulate function.
        Values returned as strings, with new line at end of list.
        """
        return ([self.country, self.code, self.product, 
                str(self.cost), str(self.quantity) + "\n"])

#======== Initialize global variables ==========
""" Set filepath to get inventory.txt.
Using vs code, filepath uses explicit path.
Using PyCharm, directory not required.
"""
# inventory_filepath = "./T32/inventory.txt"
inventory_filepath = "inventory.txt"

#======== Functions outside the class ==========
def read_shoes_data():
    """
    Open file inventory.txt, read data and create a shoes object and 
    append into shoe_list. Return shoe_list to main program.
    The first line of the file (index == 0) is disregarded as it contains headers.
    """
    
    # Initialize temporary list.
    content_list = []
    shoe_list = []
    # Read in values from inventory.txt and create Shoes objects in shoe_list.
    try:
        with open(inventory_filepath, "r") as inventory:
            for index, content in enumerate(inventory):
                if index == 0:
                    continue
                else:
                    content = content.strip("\n")
                    content_list = content.split(",")
                    shoe_list.append(Shoe(content_list[0], content_list[1], 
                        content_list[2], content_list[3], content_list[4]))
    except IOError:
        print("No inventory.txt file found") 
    return(shoe_list) 

def capture_shoes():
    """
    Create a new shoe object from user input; append to shoe list and 
    write to inventory.txt file.
    """

    # Get user input.
    country = input("\nInput country : ").capitalize()
    code = input("Input code : ").upper()
    product = input("Input product : ").title()
    input_string = "Input cost : "
    while True: 
        try:
            cost = int(input(input_string))
            break
        except ValueError:
            input_string = ("Cost must be an integer;  please re-enter : ")
    input_string = "Input quantity : "
    while True:
        try:
            quantity = int(input(input_string))
            break
        except ValueError:
            input_string = ("Cost must be an integer;  please re-enter : ")
    # Add new record to shoe_list and to inventory.txt file.
    shoe_list.append(Shoe(country, code, product, cost, quantity))
    add_inventory(shoe_list[-1].tabular_list())   
    return()

def view_all():
    """
    Create an on-screen table of the details of the shoes, using tabluate module.
    """

    print()
    printable_list = []
    for i in range(len(shoe_list)):
        printable_list.append(shoe_list[i].tabular_list())
    print(tabulate(printable_list, headers=["Country", "Code", 
        "Product", "Cost", "Quantity"]))
    return()

def re_stock():
    """
    Find the shoe object with the lowest quantity; ask the user if they
    want to add this quantity of shoes and then update it in shoe object and
    in inventory.txt.
    If there are multiple items with the same low quantity, this function
    presents the first item in the list.
    """

    lowest_quantity = 1000000
    for i in range(len(shoe_list)):
        if (shoe_list[i].get_quantity() < lowest_quantity):
            lowest_index = i
            lowest_quantity = shoe_list[i].get_quantity()
    print(f"\nLowest stock item : \n\n{shoe_list[lowest_index]}")
    while True:
        restock_action = input(f"Do you want to get {lowest_quantity} more (y/n)? ").lower()
        if restock_action == "y":
            shoe_list[lowest_index].quantity = int(shoe_list[lowest_index].quantity) + lowest_quantity
            update_list = shoe_list[lowest_index].tabular_list()
            update_file(lowest_index, update_list)
            print("\nRe-importing data ...\n")
            read_shoes_data()
            break
        elif restock_action == "n":
            break
        else:
            print("User selection not recognized")
    return()

def seach_shoe():
    """
     Search for a shoe from the list using the shoe code and 
     return this object so that it will be printed.
    """

    input_string = f"\nType in shoe code to search for : "
    while True:
        selected_code = input(input_string).upper()
        for index in range(len(shoe_list)):
            if selected_code == (shoe_list[index].get_code()):
                return(f"\n{shoe_list[index]}")
        else:
            input_string = "\nSelected shoe code not found; please re-enter : "
    return(None)

def value_per_item():
    """
    Calculate the total value for each item using value = cost * quantity.
    Sort into descending order and print to console.
    """

    printable_list = []
    sorted_printable_list = []
    for i in range(len(shoe_list)):
        printable_list.append([shoe_list[i].country, shoe_list[i].code, 
            shoe_list[i].product, shoe_list[i].cost, shoe_list[i].quantity, 
            shoe_list[i].get_cost()*shoe_list[i].get_quantity()])
    sorted_printable_list = sorted(printable_list, key=lambda x: int(x[5]), reverse=True)
    print()
    print(tabulate(sorted_printable_list, headers=["Country", "Code", "Product", "Cost", 
        "Quantity", "Value per item"]))
    print()
    return()

def highest_qty():
    """
    Find the product with the highest quantity and suggest it's put on sale.
    """

    highest_quantity = 0
    for i in range(len(shoe_list)):
        if (shoe_list[i].get_quantity() > highest_quantity):
            highest_index = i
            highest_quantity = shoe_list[i].get_quantity()
    print(f"\nMark this shoe as on sale : \n\n{shoe_list[highest_index]}")
    return()

def update_file(index, update_list):
    """ Write updated data from update_list back to inventory.txt at position
        index + 1 (as first line in file is headings). """

    with open(inventory_filepath, "r") as source :
        data = source.readlines()
        data[index + 1] = (",").join(update_list)
    with open(inventory_filepath, "w") as update :
        update.writelines(data)          
    print("\nFile updated")

def add_inventory(update_list):
    """ Write new data to inventory.txt """

    with open(inventory_filepath, "r") as source :
        data = source.readlines()
        # Make sure the last existing line ends in \n.
        data[-1] = f"{data[-1].strip()}\n"
        # Add the new line to the end of data list.
        data.append((",").join(update_list))
    with open(inventory_filepath, "w") as update :
        # Save the updated content back into inventory.txt.
        update.writelines(data)          
    print("\nFile updated")

#======== Main Menu ==========
"""
Initialize shoe_list from inventory.txt.  Display menu of user actions; get
response and call functions as required.
"""
print()
shoe_list = read_shoes_data()
view_all()
menu_selection = ""
menu_text = ("\nPlease select option : \n"
            "\n1 View all shoes"
            "\n2 Show inventory value per shoe item"
            "\n3 Manually add shoes"
            "\n4 Search for specific shoe code"
            "\n5 Re-stock lowest quantity"
            "\n6 Show suggested on-sale item"
            "\n7 Quit")
while True:
    print(menu_text)
    input_string = "\nSelect your action : "
    menu_selection = input(input_string)
    if menu_selection == "1":
        view_all()
    elif menu_selection == "2":
        value_per_item()
    elif menu_selection == "3":
        capture_shoes()
    elif menu_selection == "4":
        print(seach_shoe())
    elif menu_selection == "5":
        re_stock()
    elif menu_selection == "6":
        highest_qty()
    elif menu_selection == "7":
        print(f"\nExiting program ...\n")
        break
    else:
        print("\nIllegal menu selection")

