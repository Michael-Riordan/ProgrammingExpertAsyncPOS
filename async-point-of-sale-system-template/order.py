import asyncio
from combo import Combo

class Order:
    def __init__(self):
        self.items_by_cat = {
            "Burgers": [],
            "Sides": [],
            "Drinks": [],
        }

    def check_for_combo(self):
        combos = 0
        combination_subtotal = 0
        while len(self.items_by_cat["Burgers"]) and len(self.items_by_cat["Sides"]) and len(self.items_by_cat["Drinks"]) > 0:
            combo = {}
            
            burger = self.items_by_cat["Burgers"].pop()
            
            side = self.items_by_cat["Sides"].pop()
    
            drink = self.items_by_cat["Drinks"].pop()

            combo["Burger"] = burger
            combo["Side"] = side
            combo["Drink"] = drink

            new_combo = Combo(combo["Burger"], combo["Side"], combo["Drink"], combos)
            subtotal = new_combo.create_combo()
            combination_subtotal += subtotal
            combos += 1

        if len(self.items_by_cat["Burgers"]) or len(self.items_by_cat["Sides"]) or len(self.items_by_cat["Drinks"]) >= 1:
            remaining_subtotal = self.__str__(self.items_by_cat, combos) 
            total_price = self.total_price(combination_subtotal, remaining_subtotal)
        else:
            total_price = self.total_price(combination_subtotal)

        return total_price

    async def add_item(self, item_id, inventory):
        item, stock_level = await asyncio.gather(inventory.get_item(item_id), inventory.get_stock(item_id))

        success = await inventory.decrement_stock(item["id"])
        item_num = item["id"]
        if not success:
            print(f"Unfortunately, item number {item_num} is not in stock and has been removed from your order. Sorry!")

        if success:
            if item["category"] == "Burgers":
                self.items_by_cat["Burgers"].append([item["name"], item["price"]])
            if item["category"] == "Sides":
                self.items_by_cat["Sides"].append([item["size"], item["subcategory"], item["price"]]) 
            if item["category"] == "Drinks":
                self.items_by_cat["Drinks"].append([item["size"], item["subcategory"], item["price"]])
        
        
        for item in self.items_by_cat.values():
        
            if len(item) == 0:
                continue
            item.sort(key=lambda x: x[-1])

        return self.items_by_cat

    def total_price(self, combo_subtotal, remaining_subtotal= 0):
        subtotal = combo_subtotal + remaining_subtotal
        subtotal = round(subtotal, 2)
        tax = subtotal * .05 #.05 = sales tax
        tax = round(tax, 2)
        total = round(tax + subtotal, 2)
        if total > 0:

            print(f"\nSubtotal: ${subtotal}\nTax: ${tax}\nTotal: ${total}")

            return total
        
    def __str__(self, remaining_items, combos):
        remaining_items_subtotal = 0

        summary_statement = "Here is a summary of your order: "
        if combos == 0:
            print(f"\n{summary_statement}\n")

        if len(remaining_items["Burgers"]) > 0:
            for burger in remaining_items["Burgers"]:
                remaining_items_subtotal += burger[-1]
                print(f"${burger[-1]} {burger[0]}")

        if len(remaining_items["Sides"]) > 0:
            for side in remaining_items["Sides"]:
                side_size = side[0]
                side_name = side[1]
                side_price = side[-1]
                remaining_items_subtotal += side_price
                print(f"${side_price} {side_size} {side_name}")

        if len(remaining_items["Drinks"]) > 0:
            for drink in remaining_items["Drinks"]:
                drink_size = drink[0]
                drink_name = drink[1]
                drink_price = drink[-1]
                remaining_items_subtotal += drink_price
                print(f"${drink_price} {drink_size} {drink_name}")

        return remaining_items_subtotal

            
                
        
