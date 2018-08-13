from rpggame import rpgcharacter as rpgc, rpgarmor as rpga, rpgweapon as rpgw, rpgshopitem as rpgsi
import math

DEFAULT_ROLE = 'Undead'


class RPGPlayer(rpgc.RPGCharacter):
    def __init__(self, userid: str, username: str, exp=0, levelups=0, money=0, role=rpgc.DEFAULT_ROLE,
                 weapon=rpgw.defaultweapon, armor=rpga.defaultarmor, pet=None, health=rpgc.HEALTH,
                 maxhealth=rpgc.HEALTH, damage=rpgc.DAMAGE,
                 ws=rpgc.WEAPONSKILL, critical=0, bosstier=1, kingtimer=0, element=rpgc.element_none):
        self.userid = userid
        self.role = role
        self.exp = exp
        self.levelups = levelups
        self.money = money
        self.weapon = weapon
        self.armor = armor
        self.pet = pet
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = rpgc.NONE
        self.bosstier = bosstier
        self.kingtimer = kingtimer
        super(RPGPlayer, self).__init__(username, health, maxhealth, damage, ws, critical, element=element)

    def resolve_death(self):
        if self.health <= 0:
            self.exp = max(0, self.exp - 100 * self.get_level())
            self.money = int(math.floor(self.money * 0.5))
            self.busytime = 0

    def add_exp(self, n: int):
        if self.health <= 0:
            return
        lvl = self.get_level()
        self.add_money(n)
        self.exp += n
        self.levelups += min(0, self.get_level() - lvl)

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

    def get_maxhealth(self):
        return self.maxhealth + self.armor.maxhealth

    def get_element(self):
        return self.armor.element if self.armor.element else rpgc.element_none

    def buy_item(self, item: rpgsi.RPGShopItem, amount=1):
        if not self.subtract_money(amount * item.cost):
            return False
        self.health = min(self.get_maxhealth(),
                          rpgc.RPGCharacter.adjustStats(self.health, "health", item, amount=amount))
        self.set_maxhealth(rpgc.RPGCharacter.adjustStats(self.maxhealth, "maxhealth", item, amount=amount))
        self.damage = rpgc.RPGCharacter.adjustStats(self.damage, "damage", item, amount=amount)
        self.critical = rpgc.RPGCharacter.adjustStats(self.critical, "critical", item, amount=amount)
        return True

    def buy_training(self, item: rpgsi.RPGShopItem, amount=1):
        self.set_maxhealth(rpgc.RPGCharacter.adjustStats(self.maxhealth, "maxhealth", item, amount=amount))
        self.weaponskill = rpgc.RPGCharacter.adjustStats(self.weaponskill, "weaponskill", item, amount=amount)

    def buy_armor(self, item: rpga.RPGArmor):
        if not self.subtract_money(item.cost):
            return False
        self.money += int(math.floor(self.armor.cost * 0.25))
        self.armor = item
        self.add_health(0)
        return True

    def buy_weapon(self, item: rpgw.RPGWeapon):
        if not self.subtract_money(item.cost):
            return False
        self.money += int(math.floor(self.weapon.cost * 0.25))
        self.weapon = item
        return True

    def get_level(self):
        return rpgc.RPGCharacter.getLevelByExp(self.exp)

    def get_bosstier(self):
        return self.bosstier

    def add_bosstier(self):
        self.bosstier += 1

    def set_busy(self, action: int, time: int, channel: int):
        if self.busytime > 0:
            return False
        if action == rpgc.ADVENTURE and not (rpgc.minadvtime <= time <= rpgc.maxadvtime):
            return False
        if action == rpgc.TRAINING and not (rpgc.mintrainingtime <= time <= rpgc.maxtrainingtime):
            return False
        if action == rpgc.WANDERING and not (rpgc.minwandertime <= time <= rpgc.maxwandertime):
            return False

        self.busytime = time
        self.busychannel = channel
        self.busydescription = action
        return True

    def reset_busy(self):
        self.busytime = 0
        self.busychannel = 0
        self.busydescription = rpgc.NONE

    def set_maxhealth(self, n: int):
        r = self.health / self.get_maxhealth()
        self.maxhealth = n
        self.health = int(math.ceil(r * self.get_maxhealth()))

    def get_damage(self, element=rpgc.element_none):
        n = super().get_damage(element=element)
        n = rpgc.RPGCharacter.elementalEffect(n, self.weapon.element, element)
        return int(n + self.weapon.damage)

    def get_weaponskill(self):
        n = super().get_weaponskill()
        return int(n + self.weapon.weaponskill)

    def get_critical(self):
        n = super().get_critical()
        return int(n + self.weapon.critical)

    def do_auto_health_regen(self):
        self.add_health((self.get_maxhealth() * 0.05) + self.armor.healthregen)
