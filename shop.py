from item import Item, potion_effect, strength_potion_effect

class Shop:
    def __init__(self):
        self.stock = [
            ("Health Potion", 30, Item("Health Potion", potion_effect)),
            ("Strength Potion", 50, Item("Strength Potion", strength_potion_effect))
        ]

    def display_items(self):
        print("Welcome to the Shop! What would you like to buy?")
        for i, (name, price, _) in enumerate(self.stock):
            print(f"{i+1}. {name} - {price} gold")
        print("0. Exit")

    def buy(self, player):
        self.display_items()
        choice = input("> ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.stock):
                name, price, item = self.stock[idx]
                if player.gold >= price:
                    player.gold -= price
                    player.add_item(item)
                    print(f"You bought {name}!")
                else:
                    print("Not enough gold!")
