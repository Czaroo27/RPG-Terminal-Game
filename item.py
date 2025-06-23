class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def apply(self, character):
        self.effect(character)
        print(f"Used item: {self.name}")

def potion_effect(character):
    heal_amount = 30
    character.heal(heal_amount)

def strength_potion_effect(character):
    character.strength += 5
    print(f"{character.name} feels stronger! (+5 STR)")
