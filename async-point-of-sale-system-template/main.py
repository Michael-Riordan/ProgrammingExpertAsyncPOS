import asyncio
from order import Order
from inventory import Inventory


"""As of right now project does not add items back to stock if user decides not to confirm order.
Was not asked for in prompt but
Will go back eventually and add that for functionality"""

#display catalogue was given to me by ALGOEXPERT

def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------\n")

def confirm_order(total_price):
    if total_price != None:

        place_order = input(f"Would you like to purchase this order for {total_price} (yes/no)?").lower()
        if place_order == "yes":
            print("Thank you for your order!")
        if place_order == "no":
            print("No problem, please come again!")

    order_again = input("Would you like to make another order (yes/no)?").lower()
    if order_again == "yes":
        return order_again
    if order_again == "no":
        return order_again

async def get_order(inventory):
    order = Order()
    print('Please enter the number of the item you would like to add to your order. Enter "q" to complete your order.')
    tasks = []
    item_id = None
    while item_id != "q":

        item_id = input("Enter an item number: ")
        if item_id == "q":
            print("Placing order...")
            break

        elif not item_id.isdigit():
            print("Please enter a valid number.")

        elif int(item_id) <= 0:
            print("Please enter a valid number.")

        elif int(item_id) > 20:
            print("Please enter a number below 21.")

        else:

            item_id = int(item_id)
            task = asyncio.create_task(order.add_item(item_id, inventory)) 
            """creating this task will allow user to input orders concurrently to 
            the execution of add_item method. add_item will validate item is in stock
            then add to the items_by_cat dictionary of the order class while user is still inputting item id's
            """ 
            tasks.append(task)
               
    for task in tasks: 
        await task 
        """in order to execute all tasks
        you must use await keyword. Acts on all tasks stored in tasks[]"""

    total_price = order.check_for_combo() 
    """no need for arguments as order.add_item will add to initialized dictionary
       will return total price of combo and remaining items"""
    return total_price

async def main():
    print("Welcome to the ProgrammingExpert Burger Bar!")

    inventory = Inventory()
    print("Loading catalogue...")
    catalogue = await inventory.get_catalogue()
    display_catalogue(catalogue)

    total_price = await get_order(inventory)
    
    order_again = confirm_order(total_price)

    while order_again == "yes":
        print("")
        total_price = await get_order(inventory)
        order_again = confirm_order(total_price)

    if order_again == "no":
        print("Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
