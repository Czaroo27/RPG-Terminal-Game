from character import Character, Enemy
from item import Item, potion_effect, strength_potion_effect
from shop import Shop
from quests import check_quests
from treasure import get_random_treasure
import random
import json
import os

SAVE_FILE = "rpg_save.json"

class Game:
    def __init__(self):
        self.player = None
        self.map_width = 10
        self.map_height = 10
        self.map = []
        self.player_x = 0
        self.player_y = 0

    def create_map(self):
        self.map = [[random.choice([".", ".", ".", ".", "E", "T"]) for _ in range(self.map_width)] for _ in range(self.map_height)]

    def print_map(self):
        for y in range(self.map_height):
            row = ""
            for x in range(self.map_width):
                row += "P " if (x == self.player_x and y == self.player_y) else self.map[y][x] + " "
            print(row)

    def spawn_player(self):
        self.player_x = random.randint(0, self.map_width - 1)
        self.player_y = random.randint(0, self.map_height - 1)

    def start(self):
        print("Welcome to the RPG!")
        name = input("Enter your character's name: ")
        self.player = Character.choose_class(name)
        self.create_map()
        self.spawn_player()
        self.game_loop()

    def game_loop(self):
        while True:
            print("\nMap:")
            self.print_map()
            print(f"{self.player.status()}")
            print("What do you want to do? (w/s/a/d - move, i - inventory, m - magic, shop - shop, q - quit)")
            choice = input("> ").lower()
            if choice == "q":
                self.save_game()
                print("Game saved. See you next time!")
                break
            elif choice in ["w", "s", "a", "d"]:
                self.move_player(choice)
            elif choice == "i":
                self.inventory_menu()
            elif choice == "m":
                self.player.cast_spell_menu()
            elif choice == "shop":
                shop = Shop()
                shop.buy(self.player)
            else:
                print("Unknown command.")

            check_quests(self.player)

            if not self.player.is_alive():
                print("You died! Game over.")
                break

    def move_player(self, direction):
        dx, dy = 0, 0
        if direction == "w": dy = -1
        elif direction == "s": dy = 1
        elif direction == "a": dx = -1
        elif direction == "d": dx = 1

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if 0 <= new_x < self.map_width and 0 <= new_y < self.map_height:
            self.player_x, self.player_y = new_x, new_y
            cell = self.map[new_y][new_x]
            if cell == "E":
                self.battle()
                self.map[new_y][new_x] = "."
            elif cell == "T":
                self.find_treasure()
                self.map[new_y][new_x] = "."
            else:
                self.random_event()
        else:
            print("You can't move outside the map!")

    def battle(self):
        enemy = Enemy.random_enemy()
        print(f"You encountered a {enemy.name}!")
        while enemy.is_alive() and self.player.is_alive():
            print(f"{self.player.name} HP: {self.player.hp}/{self.player.max_hp}")
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            action = input("Attack (a), Cast Spell (m), or Flee (f)? ").lower()
            if action == "a":
                self.player.attack(enemy)
                if enemy.is_alive(): enemy.attack(self.player)
            elif action == "m":
                self.player.cast_spell(enemy)
                if enemy.is_alive(): enemy.attack(self.player)
            elif action == "f":
                if random.random() < 0.5:
                    print("You fled successfully!")
                    return
                else:
                    print("Failed to flee!")
                    enemy.attack(self.player)
            else:
                print("Unknown command.")

        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.gain_exp(enemy.exp_reward)
            self.player.gold += enemy.gold_reward
            print(f"You gained {enemy.gold_reward} gold.")

    def find_treasure(self):
        get_random_treasure(self.player)

    def random_event(self):
        print(random.choice([
            "Nothing happens...",
            "You find a mysterious stone.",
            "A cool breeze blows by.",
            "You see a shadow in the distance..."
        ]))

    def inventory_menu(self):
        while True:
            print("\nInventory:")
            if not self.player.inventory:
                print("Empty.")
                return
            for i, item in enumerate(self.player.inventory):
                print(f"{i+1}. {item.name}")
            print("Choose item number to use or 0 to exit.")
            choice = input("> ")
            if choice == "0":
                return
            elif choice.isdigit():
                self.player.use_item(int(choice)-1)

    def save_game(self):
        data = self.player.to_dict()
        data.update({"player_x": self.player_x, "player_y": self.player_y, "map": self.map})
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Game saved!")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            print("No save found.")
            return False
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        self.player = Character.from_dict(data)
        self.player_x = data["player_x"]
        self.player_y = data["player_y"]
        self.map = data["map"]
        print("Game loaded!")
        return True
