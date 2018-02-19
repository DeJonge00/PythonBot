from rpggame import rpgshopitem as rpgsi, rpgweapon as rpgw, rpgtrainingitem as rpgti, rpgarmor as rpga

element_none = 1
element_lightning = 2
element_nature = -2
element_dark = 3
element_holy = -3
element_ice = 4
element_fire = -4
elementnames = {element_none : "None", 
                element_lightning : "Lightning", 
                element_nature : "Nature", 
                element_dark : "Dark", 
                element_holy : "Holy", 
                element_ice : "Ice", 
                element_fire : "Fire"}

shopitems = {"plates" : rpgsi.RPGShopItem("armorplates", 200, {"armor" : ("+", 10)}), 
             "health" : rpgsi.RPGShopItem("health", 100, {"health" : ("+", 10)}), 
             "damage" : rpgsi.RPGShopItem("damage", 150, {"damage" : ("+", 1)}),
             "critical" : rpgsi.RPGShopItem("critical", 5000, {"critical" : ("+", 1)})
             }
trainingitems = {"maxhealth" : rpgsi.RPGShopItem("maxhealth", 0.5, {"maxhealth" : ("+", 1)}), 
                 "weaponskill" : rpgsi.RPGShopItem("weaponskill", 10, {"weaponskill" : ("+", 1)})
                 }

# Note to self: Weapons can only get negative effects with multipliers
weapons = {"training sword" : rpgsi.RPGInvItem("Training Sword", 0, {}, element_none), 
           "axe" : rpgsi.RPGInvItem("Axe", 1000, {"damage" : ("+", 10)}, element_none),
           #"rebellious knife" : rpgsi.RPGInvItem("Rebellious Knife", -200, {"damage" : ("*", 0)}, element_none),
           "thunderhammer" : rpgsi.RPGInvItem("Thunderhammer", 2000, {"damage" : ("+", 25), "weaponskill" : ("-", 5)}, element_lightning),
           "bisshop's scepter" : rpgsi.RPGInvItem("Bisshop's Scepter", 2200, {"damage" : ("+", 32), "weaponskill" : ("*", 0.8)}, element_holy),
           "slaanesh' katana" : rpgsi.RPGInvItem("Slaanesh' Katana", 3500, {"damage" : ("+", 20), "weaponskill" : ("+", 5)}, element_dark),
           "shadow dual blades" : rpgsi.RPGInvItem("Shadow Dual Blades", 5000, {"weaponskill" : ("+", 18)}, element_dark),
           "yeti's lower legbone" : rpgsi.RPGInvItem("Yeti's Lower Legbone", 10000, {"damage" : ("+", 25), "weaponskill" : ("-", 5)}, element_ice),
           "demonic greatsword" : rpgsi.RPGInvItem("Demonic Greatsword", 4000, {"damage" : ("+", 30), "weaponskill" : ("-", 3)}, element_dark),
           "chosen of tzeentch" : rpgsi.RPGInvItem("Chosen of Tzeentch", 8000, {"damage" : ("+", 66), "weaponskill" : ("-", 11)}, element_lightning),
           "silver serpent sword" : rpgsi.RPGInvItem("Silver Serpent Sword", 10000, {"damage" : ("*", 0.8), "critical" : ("+", 5)}, element_holy),
           "world tree shurikens" : rpgsi.RPGInvItem("World Tree Shurikens", 2000, {"critical" : ("+", 1)}, element_nature),
           "sonic chidori" : rpgsi.RPGInvItem("Sonic Chidori", 1000, {"damage" : ("*", 0.75), "weaponskill" : ("+", 5)}, element_lightning)
           }

armor = {"training robes" : rpgsi.RPGInvItem("Training Robes", 0, {"absorption" : ("*", 1.0)}, element_none),
         "wizard robes" : rpgsi.RPGInvItem("Wizard Robes", 2000, {"absorption" : ("*", 0.95)}, element_lightning)
         }

names = {"role" : ["Undead", "Assassin", "Lancer", "Rider", "Caster", "Archer", "Berserker", "Saber"], 
         "monster" : [("Drunk Human", element_none),
                      ("Gretchin", element_none),
                      ("Nya's Little Brother", element_none),
                      ("Something Disguised as a Tree", element_none),
                      ("Wounded Troll", element_none),
                      ("Storm Elemental", element_lightning),
                      ("Black Wolf", element_nature), 
                      ("Evolved Fish", element_nature),
                      ("Giant Spider", element_nature),
                      ("Angry Goblin", element_dark),
                      ("Lone Chaos Marauder", element_dark),
                      ("Goblin", element_dark), 
                      ("Elven Slave", element_holy),
                      ("Wandering Angel", element_holy),
                      ("Lizardman with Magic Frost Weapon", element_ice),
                      ("Magma Slime", element_fire),
                      ("Wild Cursed Campfire", element_fire)
                      ],
         "boss" : [("Ogre Bruiser", element_none),
                   ("Biribiri Herself", element_lightning),
                   ("Chaos Sorcerer", element_lightning),
                   ("Black Ork Boss", element_dark),
                   ("Chaos Demon of Khorne", element_dark),
                   ("Unknown Mutation", element_dark),
                   ("Young Dragon", element_holy),
                   ("Mammoth", element_ice),
                   ("Yeti", element_ice)
                   ]
         }

adventureSecrets = [("you found a treasure chest", "Money", 200),
                    ("you fell off the road and climbed back up", "Weaponskill", 1),
                    ("you got lost and rested at a small lake", "Health", 100),
                    ("you talked to some strange travellers", "Exp", 200),
                    ("you sold some junk at a salesman near the road", "Money", 250),
                    ("you saw something shiny when you followed a bird", "Money", 100),
                    ("you got distracted by nature", "A good feeling", 1),
                    ("a strange creature you saved gave you his thanks", "Money", 100),
                    ("you saw big creatures fighting in the distance and learned some moves", "Exp", 250),
                    ("a blacksmith in a small village tought you some tricks", "Damage", 2),
                    ("you listened to another adventurer's tales", "Exp", 150),
                    ("you found a nest of little griffins and made the wise decision to run", "Exp", 100)
                    ]