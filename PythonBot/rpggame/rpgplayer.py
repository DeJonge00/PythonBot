from rpggame import rpgcharacter
from rpggame.rpgarmor import RPGArmor
from rpggame.rpgweapon import RPGWeapon
from rpggame.rpgshopitem import RPGShopItem
from rpggame import rpgconstants as rpgc
from rpggame.rpgpet import RPGPet
import math

DEFAULT_ROLE = 'Undead'


class RPGPlayer(rpgcharacter.RPGCharacter):
    def __init__(self, userid: str, username: str, exp=0, levelups=0, money=0, role=DEFAULT_ROLE, weapon=RPGWeapon(),
                 armor=RPGArmor(), pets: [RPGPet]=[], health=rpgcharacter.DEFAULT_HEALTH, maxhealth=rpgcharacter.DEFAULT_HEALTH,
                 damage=rpgcharacter.DEFAULT_DAMAGE, ws=rpgcharacter.DEFAULT_WEAPONSKILL, critical=0, bosstier=1,
                 kingtimer=0, element=rpgc.element_none, extratime=0):
        self.userid = userid
        self.role = role
        self.exp = exp
        self.levelups = levelups
        self.money = money
        self.weapon = weapon
        self.armor = armor
        self.pets = pets
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = rpgcharacter.BUSY_DESC_NONE
        self.bosstier = bosstier
        self.kingtimer = kingtimer
        self.extratime = extratime
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws, critical, element=element)

    @staticmethod
    def get_level_by_exp(exp: int):
        return math.floor(math.sqrt(exp) / 25) + 1

    def resolve_death(self):
        if self.health <= 0:
            self.exp = max(0, self.exp - 100 * self.get_level())
            self.money = int(math.floor(self.money * 0.5))
            self.busytime = 0

    def add_exp(self, n: int):
        if self.health <= 0:
            return
        lvl = self.get_level()
        self.exp += n
        self.levelups += max(0, self.get_level() - lvl)

    def add_health(self, n: int, death=True, element=rpgc.element_none):
        super().add_health(n)
        if death:
            self.resolve_death()

    def add_money(self, n: int):
        if n < 0:
            return False
        n = (1 + (self.armor.money / 100)) * n
        self.money = int(self.money + n)

    def subtract_money(self, n: int):
        if n < 0 or self.money - n < 0:
            return False
        self.money = int(math.floor(self.money - n))
        return True

    def get_max_health(self):
        return self.maxhealth + self.armor.maxhealth

    def get_element(self):
        return self.armor.element if self.armor.element else rpgc.element_none

    def buy_item(self, item: RPGShopItem, amount=1):
        if not self.subtract_money(amount * item.cost):
            return False
        self.health = min(self.get_max_health(),
                          rpgcharacter.RPGCharacter.adjust_stats(self.health, "health", item, amount=amount))
        self.set_max_health(rpgcharacter.RPGCharacter.adjust_stats(self.maxhealth, "maxhealth", item, amount=amount))
        self.damage = rpgcharacter.RPGCharacter.adjust_stats(self.damage, "damage", item, amount=amount)
        self.critical = rpgcharacter.RPGCharacter.adjust_stats(self.critical, "critical", item, amount=amount)
        return True

    def buy_training(self, item: RPGShopItem, amount=1):
        self.set_max_health(rpgcharacter.RPGCharacter.adjust_stats(self.maxhealth, "maxhealth", item, amount=amount))
        self.weaponskill = rpgcharacter.RPGCharacter.adjust_stats(self.weaponskill, "weaponskill", item, amount=amount)

    def buy_armor(self, item: RPGArmor):
        if not self.subtract_money(item.cost):
            return False
        self.money += int(math.floor(self.armor.cost * 0.25))
        self.armor = item
        self.add_health(0)
        return True

    def buy_weapon(self, item: RPGWeapon):
        if not self.subtract_money(item.cost):
            return False
        self.money += int(math.floor(self.weapon.cost * 0.25))
        self.weapon = item
        return True

    def get_level(self):
        return RPGPlayer.get_level_by_exp(self.exp)

    def get_bosstier(self):
        return self.bosstier

    def add_bosstier(self):
        self.bosstier += 1

    def set_busy(self, action: int, time: int, channel: int):
        self.busytime = time
        self.busychannel = channel
        self.busydescription = action

    def reset_busy(self):
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = rpgcharacter.BUSY_DESC_NONE

    def set_max_health(self, n: int):
        r = self.health / self.get_max_health()
        self.maxhealth = n
        self.health = int(math.ceil(r * self.get_max_health()))

    def get_damage(self, element=rpgc.element_none):
        n = super().get_damage(element=element)
        n = rpgcharacter.RPGCharacter.elemental_effect(n, self.weapon.element, element)
        return int(n + self.weapon.damage)

    def get_weaponskill(self):
        n = super().get_weaponskill()
        return int(n + self.weapon.weaponskill)

    def get_critical(self):
        n = super().get_critical()
        return int(n + self.weapon.critical)

    def do_auto_health_regen(self):
        if self.busydescription == rpgcharacter.BUSY_DESC_NONE:
            percentage = 0.02
        else:
            percentage = 0.05
        self.add_health((self.get_max_health() * percentage) + self.armor.healthregen)

    def add_pet(self, pet: RPGPet):
        if len(self.pets) >= 3:
            return False
        self.pets.append(pet)
        return True
