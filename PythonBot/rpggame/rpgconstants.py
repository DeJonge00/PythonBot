from rpggame import rpgshopitem as rpgsi, rpgweapon as rpgw, rpgtrainingitem as rpgti

shopitems = {"armor" : rpgsi.RPGShopItem("armor", 200, 10), "health" : rpgsi.RPGShopItem("health", 100, 10), "damage" : rpgsi.RPGShopItem("damage", 150, 5)}
trainingitems = {"health" : rpgti.RPGTrainingItem("health", 1), "weaponskill" : rpgti.RPGTrainingItem("weaponskill", 10)}


weapons = {"Training Sword" : rpgw.RPGWeapon("Training Sword", 0, {}), 
           "Axe" : rpgw.RPGWeapon("Axe", 1000, {"damage" : 1.1}),
           "Rebellious Knife" : rpgw.RPGWeapon("Rebellious Knife", -200, {"damage" : 0})}

names = {"role" : ["Undead", "Assassin", "Lancer", "Rider", "Caster", "Archer", "Berserker", "Saber"], 
         "monster" : ["Goblin", "Gretchin", "Elven Slave", "Giant Spider", "Wounded Troll", "Lone Chaos Marauder", "Black Wolf", "Evolved Fish", "Drunk Human"],
         "boss" : ["Black Ork Boss", "Yeti", "Mammoth", "Ogre Bruiser", "Chaos Demon of Khorne", "Chaos Sorcerer", "Unknown Mutation", "Young Dragon"]
         }