class Spell:
    def __init__(self, name, mana_cost, effect):
        self.name = name
        self.mana_cost = mana_cost
        self.effect = effect

def fireball(caster, target):
    if target:
        damage = 30 + caster.level * 2
        target.hp -= damage
        print(f"🔥 {caster.name} casts Fireball on {target.name}, dealing {damage} damage!")

def heal(caster, _):
    amount = 25 + caster.level * 2
    caster.heal(amount)
    print(f"✨ {caster.name} casts Heal and restores {amount} HP!")

fireball = Spell("Fireball", 15, fireball)
heal = Spell("Heal", 10, heal)
