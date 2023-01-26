
class Combo:
    def __init__(self, burger, side, drink, combos):
        self.burger = burger
        self.side = side
        self.drink = drink
        self.combos = combos
        self.combo_discount = .15

    def create_combo(self):

        price_before_discount = self.burger[-1] + self.side[-1] + self.drink[-1]
        discount = price_before_discount * self.combo_discount
        discounted_price = price_before_discount - discount
        discounted_price = round(discounted_price, 2)
        
        self.__str__(self.burger, self.side, self.drink, discounted_price, self.combos)
        return discounted_price

    def __str__(self, burger, side, drink, disc_price, combos):
        burger = burger[0]
        side_size = side[0]
        side_name = side[1]
        drink_size = drink[0]
        drink_name = drink[1]

        if combos >= 1:
            summary_statement = ""
        else:
            summary_statement = "\nHere is a summary of your order:\n\n"

        print(f"{summary_statement}"f"${disc_price} Burger Combo\n"
        f"  {burger}\n"f"  {side_size} {side_name}\n "
        f" {drink_size} {drink_name}")
        
        
        
        





