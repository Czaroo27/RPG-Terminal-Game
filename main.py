import random
import json
import os

SAVE_FILE = "rpg_save.json"

class Character:
    def __init__(self, name, hp, mana, strength, defense, level=1, exp=0, gold=0):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mana = mana
        self.mana = mana
        self.strength = strength
        self.defense = defense
        self.level = level
        self.exp = exp
        self.gold = gold
        self.inventory = []

    def is_alive(self):
        return self.hp > 0

    def attack(self, other):
        damage = max(0, self.strength - other.defense + random.randint(-2, 2))
        other.hp -= damage
        print(f"{self.name} attacks {other.name} dealing {damage} damage!")
        if other.hp < 0:
            other.hp = 0
        return damage

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} heals for {amount} health points.")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gains {amount} experience.")
        while self.exp >= self.exp_to_next_level():
            self.level_up()

    def exp_to_next_level(self):
        return 50 + self.level * 50

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.max_mana += 5
        self.strength += 2
        self.defense += 1
        self.hp = self.max_hp
        self.mana = self.max_mana
        print(f"Congratulations! {self.name} reached level {self.level}!")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} acquires an item: {item.name}")

    def use_item(self, index):
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            item.apply(self)
        else:
            print("Invalid item index.")

class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect  

    def apply(self, character):
        self.effect(character)
        print(f"Used item {self.name}")

def potion_effect(character):
    heal_amount = 30
    character.heal(heal_amount)

def strength_potion_effect(character):
    character.strength += 5
    print(f"{character.name} gains +5 strength for the next battle.")

class Enemy(Character):
    def __init__(self, name, hp, mana, strength, defense, level, exp_reward, gold_reward):
        super().__init__(name, hp, mana, strength, defense, level)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward

    def attack(self, other):
        damage = max(0, self.strength - other.defense + random.randint(-1, 3))
        other.hp -= damage
        print(f"Enemy {self.name} attacks {other.name} and deals {damage} damage.")
        if other.hp < 0:
            other.hp = 0
        return damage

class Game:
    def __init__(self):
        self.player = None
        self.map_width = 10
        self.map_height = 10
        self.map = []
        self.player_x = 0
        self.player_y = 0

    def create_map(self):
        self.map = []
        for _ in range(self.map_height):
            row = []
            for _ in range(self.map_width):
                cell = random.choice([".", ".", ".", ".", "E", "T"])  # E=enemy, T=treasure
                row.append(cell)
            self.map.append(row)

    def print_map(self):
        for y in range(self.map_height):
            row = ""
            for x in range(self.map_width):
                if x == self.player_x and y == self.player_y:
                    row += "P "
                else:
                    row += self.map[y][x] + " "
            print(row)

    def spawn_player(self):
        self.player_x = random.randint(0, self.map_width - 1)
        self.player_y = random.randint(0, self.map_height - 1)

    def start(self):
        print("Welcome to the RPG!")
        name = input("Enter your character's name: ")
        self.player = Character(name, hp=100, mana=30, strength=10, defense=5)
        self.create_map()
        self.spawn_player()
        self.game_loop()

    def game_loop(self):
        while True:
            print("\nMap:")
            self.print_map()
            print(f"HP: {self.player.hp}/{self.player.max_hp}  Mana: {self.player.mana}/{self.player.max_mana}  Level: {self.player.level}  Exp: {self.player.exp}/{self.player.exp_to_next_level()}  Gold: {self.player.gold}")
            print("What do you want to do? (w/s/a/d - move, i - inventory, q - quit)")
            choice = input("> ").lower()
            if choice == "q":
                self.save_game()
                print("Game saved. See you next time!")
                break
            elif choice in ["w", "s", "a", "d"]:
                self.move_player(choice)
            elif choice == "i":
                self.inventory_menu()
            else:
                print("Unknown command.")

            if not self.player.is_alive():
                print("You died! Game over.")
                break

    def move_player(self, direction):
        dx, dy = 0, 0
        if direction == "w":
            dy = -1
        elif direction == "s":
            dy = 1
        elif direction == "a":
            dx = -1
        elif direction == "d":
            dx = 1

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if 0 <= new_x < self.map_width and 0 <= new_y < self.map_height:
            self.player_x = new_x
            self.player_y = new_y
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
        enemy = self.generate_enemy()
        print(f"You encountered a {enemy.name}!")
        while enemy.is_alive() and self.player.is_alive():
            print(f"{self.player.name} HP: {self.player.hp}/{self.player.max_hp}")
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            action = input("Attack (a) or flee (f)? ").lower()
            if action == "a":
                self.player.attack(enemy)
                if enemy.is_alive():
                    enemy.attack(self.player)
            elif action == "f":
                if random.random() < 0.5:
                    print("You fled successfully!")
                    break
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

    def generate_enemy(self):
        types = [
            ("Goblin", 30, 0, 7, 2, 1, 20, 10),
            ("Orc", 50, 0, 10, 5, 2, 40, 20),
            ("Dragon", 120, 50, 20, 10, 5, 150, 100)
        ]
        name, hp, mana, strength, defense, level, exp, gold = random.choice(types)
        return Enemy(name, hp, mana, strength, defense, level, exp, gold)

    def find_treasure(self):
        treasure = random.choice(["gold", "health potion", "strength potion"])
        print(f"You found a treasure: {treasure}!")
        if treasure == "gold":
            amount = random.randint(10, 100)
            self.player.gold += amount
            print(f"You got {amount} gold.")
        elif treasure == "health potion":
            self.player.add_item(Item("Health Potion", potion_effect))
        elif treasure == "strength potion":
            self.player.add_item(Item("Strength Potion", strength_potion_effect))

    def random_event(self):
        events = [
            "Nothing happens...",
            "You meet a wanderer, but have no interaction.",
            "You find an interesting stone.",
            "You feel a slight vibration under your feet.",
            "A mysterious fog is visible in the distance."
        ]
        print(random.choice(events))

    def inventory_menu(self):
        while True:
            print("\nInventory:")
            if not self.player.inventory:
                print("Empty.")
                break
            for i, item in enumerate(self.player.inventory):
                print(f"{i+1}. {item.name}")
            print("Choose an item number to use or 0 to exit.")
            choice = input("> ")
            if choice == "0":
                break
            elif choice.isdigit():
                idx = int(choice) - 1
                self.player.use_item(idx)
            else:
                print("Invalid choice.")

    def save_game(self):
        data = {
            "player": {
                "name": self.player.name,
                "hp": self.player.hp,
                "max_hp": self.player.max_hp,
                "mana": self.player.mana,
                "max_mana": self.player.max_mana,
                "strength": self.player.strength,
                "defense": self.player.defense,
                "level": self.player.level,
                "exp": self.player.exp,
                "gold": self.player.gold,
                "inventory": [item.name for item in self.player.inventory]
            },
            "player_x": self.player_x,
            "player_y": self.player_y,
            "map": self.map
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Game saved!")

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            p = data["player"]
            self.player = Character(
                p["name"], p["max_hp"], p["max_mana"], p["strength"], p["defense"],
                p["level"], p["exp"], p["gold"]
            )
            self.player.hp = p["hp"]
            self.player.mana = p["mana"]
            # NOTE: For simplicity, all potions apply same effect here
            self.player.inventory = [Item(name, potion_effect) for name in p["inventory"]]
            self.player_x = data["player_x"]
            self.player_y = data["player_y"]
            self.map = data["map"]
            print("Game loaded!")
            return True
        else:
            print("No saved game found.")
            return False

if __name__ == "__main__":
    game = Game()
    print("1. New Game\n2. Load Game")
    choice = input("> ")
    if choice == "2":
        if not game.load_game():
            print("Starting new game.")
            game.start()
        else:
            game.game_loop()
    else:
        game.start()
