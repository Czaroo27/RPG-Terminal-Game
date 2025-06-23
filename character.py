import random
from item import Item, potion_effect, strength_potion_effect
from spells import Spell, fireball, heal

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
        self.spells = []

    @staticmethod
    def choose_class(name):
        print("Choose class: 1) Warrior 2) Mage 3) Thief")
        choice = input("> ")
        if choice == "1":
            player = Character(name, 120, 20, 15, 8)
        elif choice == "2":
            player = Character(name, 80, 60, 8, 4)
        elif choice == "3":
            player = Character(name, 90, 30, 12, 6)
        else:
            print("Defaulting to Warrior.")
            player = Character(name, 120, 20, 15, 8)
        player.learn_spell(fireball)
        player.learn_spell(heal)
        return player

    def status(self):
        return f"{self.name} | HP: {self.hp}/{self.max_hp} | MP: {self.mana}/{self.max_mana} | LVL: {self.level} | EXP: {self.exp}/{self.exp_to_next_level()} | Gold: {self.gold}"

    def is_alive(self):
        return self.hp > 0

    def attack(self, other):
        damage = max(0, self.strength - other.defense + random.randint(-2, 2))
        other.hp -= damage
        print(f"{self.name} attacks {other.name} for {damage} damage!")

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{self.name} heals for {amount} HP!")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gains {amount} EXP!")
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
        print(f"{self.name} leveled up to {self.level}!")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} acquired {item.name}!")

    def use_item(self, index):
        if 0 <= index < len(self.inventory):
            item = self.inventory.pop(index)
            item.apply(self)
        else:
            print("Invalid item index.")

    def learn_spell(self, spell):
        self.spells.append(spell)

    def cast_spell_menu(self):
        if not self.spells:
            print("You don't know any spells!")
            return
        print("Choose a spell:")
        for i, spell in enumerate(self.spells):
            print(f"{i+1}. {spell.name} (Cost: {spell.mana_cost})")
        choice = input("> ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.spells):
                self.cast_spell(None, idx)

    def cast_spell(self, target, idx=None):
        if not self.spells:
            print("You don't know any spells!")
            return
        if idx is None:
            self.cast_spell_menu()
            return
        spell = self.spells[idx]
        if self.mana >= spell.mana_cost:
            self.mana -= spell.mana_cost
            spell.effect(self, target)
        else:
            print("Not enough mana!")

    def to_dict(self):
        return {
            "player": {
                "name": self.name,
                "hp": self.hp,
                "max_hp": self.max_hp,
                "mana": self.mana,
                "max_mana": self.max_mana,
                "strength": self.strength,
                "defense": self.defense,
                "level": self.level,
                "exp": self.exp,
                "gold": self.gold,
                "inventory": [item.name for item in self.inventory]
            }
        }

    @staticmethod
    def from_dict(data):
        p = data["player"]
        char = Character(p["name"], p["max_hp"], p["max_mana"], p["strength"], p["defense"], p["level"], p["exp"], p["gold"])
        char.hp = p["hp"]
        char.mana = p["mana"]
        char.inventory = [Item(name, potion_effect) for name in p["inventory"]]
        char.learn_spell(fireball)
        char.learn_spell(heal)
        return char

class Enemy(Character):
    @staticmethod
    def random_enemy():
        options = [
            ("Goblin", 30, 0, 6, 2, 1, 20, 10),
            ("Orc", 50, 10, 10, 4, 2, 40, 25),
            ("Dragon", 120, 50, 18, 10, 5, 120, 150)
        ]
        name, hp, mana, strg, defn, lvl, exp, gold = random.choice(options)
        enemy = Enemy(name, hp, mana, strg, defn, lvl)
        enemy.exp_reward = exp
        enemy.gold_reward = gold
        return enemy

    def __init__(self, name, hp, mana, strength, defense, level):
        super().__init__(name, hp, mana, strength, defense, level)
        self.exp_reward = 0
        self.gold_reward = 0
