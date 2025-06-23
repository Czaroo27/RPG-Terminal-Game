from item import Item, potion_effect, strength_potion_effect
import random

def get_random_treasure(player):
    treasure = random.choice(["gold", "health potion", "strength potion"])
    print(f"You found a treasure: {treasure}!")
    if treasure == "gold":
        amount = random.randint(10, 100)
        player.gold += amount
        print(f"You got {amount} gold.")
    elif treasure == "health potion":
        player.add_item(Item("Health Potion", potion_effect))
    elif treasure == "strength potion":
        player.add_item(Item("Strength Potion", strength_potion_effect))
