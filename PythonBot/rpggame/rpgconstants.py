from rpggame.rpgshopitem import RPGShopItem

element_none = 1
element_lightning = 2
element_air = -2
element_dark = 3
element_holy = -3
element_ice = 4
element_fire = -4
elementnames = {
    element_none: ("Normal", "Plain"),
    element_lightning: ("Lightning", "Thunder"),
    element_air: ("Air", "Aerial"),
    element_dark: ("Dark", "Dark"),
    element_holy: ("Holy", "Divine"),
    element_ice: ("Ice", "Frozen"),
    element_fire: ("Fire", "Flaming")
}

shopitems = {
    "health": RPGShopItem("health", 100, {"health": ("+", 25)}),
    "maxhealth": RPGShopItem("maxhealth", 500, {"maxhealth": ("+", 10)}),
    "damage": RPGShopItem("damage", 250, {"damage": ("+", 1)}),
    "critical": RPGShopItem("critical", 4000, {"critical": ("+", 1)})
}

trainingitems = {
    "maxhealth": RPGShopItem("maxhealth", 0.25, {"maxhealth": ("+", 1)}),
    "weaponskill": RPGShopItem("weaponskill", 10, {"weaponskill": ("+", 1)})
}

weapons = [
    'Axe',
    'Boomerang', 'Bow',
    'Club', 'Crossbow',
    'Dual Daggers', 'Dagger',
    'Glaive', 'Greatsword',
    'Hammer', 'Halberd',
    'Katana',
    'Mace', 'Magic',
    'Pike',
    'Rapier',
    'Spear', 'Slingshot', 'Scourge', 'Scythe', 'Sorcery', 'Staff', 'Sword',
    'Twin Glaives'
]

armors = [
    'Brigandine',
    'Chainmail', 'Cuirass',
    'Dō',
    'Keikō', 'Kusari Katabira',
    'Lamellar Armor', 'Laminar Armor',
    'Plate Armor', 'Plated Mail',
    'Robes',
    'Scale Armor',
    'Tankō'
]

prefixes = [
    'Cursed',
    'Possesed',
    'Rusty',
    'Old',
    'Used',
    'Antic',
    'Ancient',
    'Common',
    'Forgotten',
    'New',
    'Rare',
    'Epic',
    'Legendary',
    'Incredible',
    'Haunted',
    'Great'
]

suffixes = [
    'Stolen from a Kid',
    'Fallen off a Tumbrel',
    'Forged in Dafaq\'s Tears',
    'Bought from the Local Dealer',
    'gifted by the Emperor',
    'blessed by Kappa',
    'of Dankness',
    'Infused with the Power of Love',
    'of Power',
    'of Doom',
    'of Power of Doom of Apoc..',
    'that Lived under a Rock',
    'of Old Tales',
    'from a Happy Meal',
    'Scavenged on a Weeb\'s Corpse',
    'used to Clean Dragon Teeth',
    'that can Talk but not to You',
    'from Angel\'s Forge',
    'of a Forgotten Hero',
    'used by Kings',
    'Larger than a Man',
    'Infused with a Greater Soul',
    'Wished into Existence',
    'Created by the God of War',
    'Given as a Blessing',
    'of the Chosen One',
    'for That Special Someone',
    'for the Warrior',
    'Gifted in Time of Peace',
    'Known for its Unusual Stance',
    'Known by All',
    'the First of its Name',
    'of a Thousand Pains',
    'made from Meteors',
    'made with Magic',
    'Once Broken, Now Reforged'
]

names = {
    "role": [
        # >work: money *= 1.15
        ("Peasant", "A humble peasant works hard and earns even more"),
        # .get_damage(): damage *= 1.3, .get_max_health(): maxhealth *= 0.85
        ("Sorcerer", "A mighty sorcerer cannot take hits very well, but excels in powerful offensive magical attacks"),
        # Pet exp *= 1.3
        ("Hunter", "An adventurous hunter loves and is loved by pets"),
        # .get_max_health() hmaxhealth *= 1.2
        ("Samurai", "A battle-hardened samurai can withstand a great deal of damage done by any man or beast"),
        # do-auto_health_regen 0.025 -> 0.01, 0.035 -> 0.06
        ("Priest", "A holy priest is skilled in using healing and protection magic"),
        # No death penalty, max health == DEFAULT_HEALTH, weaponskill == 1, money *= 0
        ("Kitten", "A kitten cannot fight, cannot work, cannot train, but.. Wow! It is so adorable!")
    ]
}

monsters = [
    ("Armored Orc", element_none,
     "https://cdna.artstation.com/p/assets/images/images/002/689/366/large/ignacio-lazcano-orc-warhammer-fan-art.jpg?1464617720"),
    ("Boar", element_none,
     "https://vignette.wikia.nocookie.net/swordartonlineroleplay/images/4/4a/Frenzy_Boar.png/revision/latest?cb=20121115182555"),
    ("Black Wolf", element_none,
     "https://s-media-cache-ak0.pinimg.com/originals/40/80/39/40803940ed534c4b396a43a270e66e57.jpg"),
    ("Desert Raider", element_none,
     "https://i.pinimg.com/736x/71/ca/fb/71cafb5cb719b0336547694db1038d3d--fantasy-warrior-character-ideas.jpg"),
    ("Drunk Dwarf", element_none,
     "https://fc06.deviantart.net/fs70/f/2011/234/c/b/party_dwarf_by_capprotti-d47g5pt.jpg"),
    ("Dwarf Hunter and Companion", element_none,
     "https://i.pinimg.com/736x/a3/bf/2d/a3bf2de2d2a4e6fee2bb0f600c3bd8b1--world-of-warcraft-wallpaper-dwarf.jpg"),
    ("Dwarf Monster Slayer", element_none,
     "https://i.pinimg.com/736x/50/7a/63/507a63e542c3abe8e0d90df9e8fd1a9f--fantasy-dwarf-sci-fi-fantasy.jpg"),
    ("Elven Ranger", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/7/75/Warhammer_Wood_Elf.png/revision/latest?cb=20130519024532"),
    ("Greatsword Champion", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/8/85/Capture22233232.png/revision/latest?cb=20140206193843"),
    ("Gretchin", element_none,
     "http://wh40k.lexicanum.com/mediawiki/images/thumb/e/eb/SM_Gretchin.png/250px-SM_Gretchin.png"),
    ("Giant Spider", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/3/3f/Warhammer_Giant_Spiders.png/revision/latest?cb=20170809014204"),
    ("Honourable Samurai", element_none, "https://wallscover.com/images/samurai-wallpaper-7.jpg"),
    ("Hungry Spirit", element_none,
     "https://res.cloudinary.com/teepublic/image/private/s--VAXY9TGW--/t_Preview/b_rgb:191919,c_limit,f_jpg,h_630,q_90,w_630/v1458926376/production/designs/458030_1.jpg"),
    ("Runaway Warbeast", element_none,
     "http://wh40k.lexicanum.com/mediawiki/images/thumb/6/6e/Cruorian_War_Beast.jpg/300px-Cruorian_War_Beast.jpg"),
    ("Malicious Chopper", element_none,
     "https://vignette.wikia.nocookie.net/villains/images/c/c9/Barry-0.png/revision/latest?cb=20150810173740"),
    ("Nya's Little Brother", element_none,
     "http://wh40k.lexicanum.com/mediawiki/images/thumb/a/a0/ChaosSpawn2.jpg/225px-ChaosSpawn2.jpg"),
    ("Savage Armored Goblin", element_none,
     "https://i.pinimg.com/736x/24/23/e1/2423e1955cf7e40b20d40bedbe16a392--warhammer-fantasy-warhammer-k.jpg"),
    ("Stalking Elven Archer", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/0/0c/Warhammer_Wood_Elves_Waystalker.jpg/revision/latest?cb=20160909032654"),
    ("Something Disguised as a Tree", element_none,
     "http://statici.behindthevoiceactors.com/behindthevoiceactors/_img/chars/treebeard-the-lord-of-the-rings-the-two-towers-68.6.jpg"),
    ("Sepulchural Stalker", element_none,
     "https://s-media-cache-ak0.pinimg.com/originals/f5/6d/2d/f56d2d38d427d25a610ac7e4365f1bcf.jpg"),
    ("Tomb King Chosen", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/d/da/Warhammer_Tomb_Kings_Settra.png/revision/latest?cb=20160911222902"),
    ("Wounded Troll", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/2/20/Trolls_-_Stone_Troll_%28Old_Art%29.jpg/revision/latest?cb=20160708133949"),

    ("Elemental Shaman", element_lightning,
     "https://i.pinimg.com/736x/f8/5c/f6/f85cf681c7465967fedfe89bfb6caf0d--the-wizard-lightning.jpg"),
    ("Doomsayer", element_lightning,
     "https://2dbdd5116ffa30a49aa8-c03f075f8191fb4e60e74b907071aee8.ssl.cf1.rackcdn.com/3065298_1421697249.5094_funddescription.jpg"),
    ("Thunder Knight", element_lightning,
     "https://s-media-cache-ak0.pinimg.com/originals/78/de/77/78de777c2411214e0b61eb22ba25c985.jpg"),
    ("Scissor Knight", element_lightning,
     "https://i.pinimg.com/736x/41/32/b7/4132b7423da75a1d5f9bed5d467072d2--kill-la-kill-anime-art.jpg"),
    ("Storm Elemental", element_lightning,
     "https://i.pinimg.com/736x/87/c7/8e/87c78eb9801fb248f91844881259e0ac--guild-wars--medieval-fantasy.jpg"),
    ("Enraged God", element_lightning,
     "https://myanimelist.cdn-dena.com/s/common/uploaded_files/1447535700-090b256b01362465f295aa3f8aca6080.jpeg"),

    ("A Birdperson", element_air,
     "https://vignette.wikia.nocookie.net/rickandmorty/images/9/9d/BirdpersonTransparent.png/revision/latest?cb=20161223222905"),
    ("Angry Griffin", element_air, "http://www.dododex.com/media/creature/griffin.png"),
    ("Awakened Being", element_air,
     "https://vignette.wikia.nocookie.net/claymore/images/2/20/PriscillaAwakened.gif/revision/latest?cb=20080815194603"),
    ("Enraged Spiritual Guide", element_air,
     "https://bravenewmoe.files.wordpress.com/2013/08/monogatari20second20season20-200520-20large2018.jpg"),
    ("Fallen Friend", element_air, "https://pm1.narvii.com/6351/867f04184d535dedf5d2062f7c7cac46f94776bd_hq.jpg"),
    ("Little Witch", element_air,
     "https://pre00.deviantart.net/c2bd/th/pre/i/2017/103/f/6/shiny_arc_by_moonflower20000-db5qf30.jpg"),
    ("Little Loli Dragon", element_air,
     "https://vignette.wikia.nocookie.net/vsbattles/images/d/d4/Blue_Eyes.png/revision/latest?cb=20160201020306"),
    ("Lone Air Nomad", element_air,
     "https://orig08.deviantart.net/f3a9/f/2016/119/4/f/aang_about_web_by_dynamo1212-da0ox4c.jpg"),

    ("Angry Goblin", element_dark,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/b/b4/Goblin_Warrior.png/revision/latest?cb=20160508093347"),
    ("Dullahan", element_dark, "https://pre00.deviantart.net/6c54/th/pre/f/2010/068/f/7/durarara___dusk_by_yumera.jpg"),
    ("Hekatonkheires", element_dark,
     "https://vignette.wikia.nocookie.net/akamegakill/images/6/64/Coro.png/revision/latest?cb=20140803220237"),
    ("Khone Juggernaut", element_dark,
     "https://vignette.wikia.nocookie.net/warhammer40k/images/5/56/Juggernaut_of_Khorne.png/revision/latest?cb=20151215222741"),
    ("Lone Chaos Marauder", element_dark,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/7/7f/Chaos_Marauder.png/revision/latest?cb=20151106043446"),
    ("Mutated Monster Monkey", element_dark,
     "https://orig00.deviantart.net/07df/f/2013/119/d/5/rainy_devil_cosplay___bakemonogatari_by_kohimebashiri-d63k393.jpg"),
    ("Skaven Assassin in Training", element_dark, "https://us.v-cdn.net/5022456/uploads/editor/tr/lllm5fvwginz.jpg"),
    ("Horrifying Swamp Monster", element_dark, "http://batrock.net/animeimages/mushi05-01.JPG"),
    ('Shirt and Scarf Combo', element_dark, "https://foregroundnoises.files.wordpress.com/2013/12/kill091.jpg"),

    ("Awoken Spirit", element_holy,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/4/41/WAR_CA_00806_07.jpg/revision/latest/scale-to-width-down/251?cb=20171119134426"),
    ("Disgraced Samurai", element_holy,
     "https://pre00.deviantart.net/0ec9/th/pre/i/2015/162/8/8/fast_art____ghost_samurai_by_killbiro-d8wyee9.jpg"),
    ("Elven Slave", element_holy, "http://whfb.lexicanum.com/mediawiki/images/thumb/4/44/DEW.JPG/293px-DEW.JPG"),
    ("Elven Wanderer", element_holy,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/2/26/Warhammer_Aenarion.png/revision/latest?cb=20161029054605"),
    ("Justice", element_holy, "http://www.1zoom.me/big2/39/207534-SweetAngel.jpg"),
    ("Mounted Priest", element_holy,
     "https://i.pinimg.com/564x/4f/eb/a5/4feba5830be778ddfe52cb7cb7db71b7--war-hammer-warriors.jpg"),
    ("Saint of a Lost Faith", element_holy,
     "https://img00.deviantart.net/7081/i/2013/103/4/f/saint_celestine__warhammer_40_000__by_phallseanghell-d61lry2.jpg"),
    ("Tired Pilgrim", element_holy,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/2/2d/Warhammer_Human_Nagash.jpg/revision/latest?cb=20170422040305"),
    ("Wandering Angel", element_holy,
     "https://i.pinimg.com/736x/42/92/59/429259b04d9825ec546cda7ae11095f4--fantasy-art-angels-fallen-angels.jpg"),
    ('Mischievous Angel', element_holy, "https://i.pinimg.com/originals/b3/f1/78/b3f178548031613133515cb9028d7257.jpg"),

    ("Lava Crocodile", element_fire,
     "https://vignette.wikia.nocookie.net/creaturequest/images/4/4f/246_LavaCrocodile.png/revision/latest?cb=20170316003052"),
    ("Lava Salamander", element_fire,
     "http://4.bp.blogspot.com/-UEZJNqRarg0/T_H4FbsjPwI/AAAAAAAABK0/GxEgvp3qcqk/s1600/Fire_Lizard_by_bcook972001.jpeg"),
    ("Magma Slime", element_fire,
     "https://d1u5p3l4wpay3k.cloudfront.net/minecraft_gamepedia/thumb/c/c8/Magma_Cube_Jumping.png/150px-Magma_Cube_Jumping.png?version=745959687f245bc782a68f16eead18cc"),
    ("Molten Troll", element_fire,
     "https://img00.deviantart.net/79de/i/2014/039/1/c/lava_monster__cherufe__by_jubjubjedi-d56j69f.jpg"),
    ("High Elf Phoenix Guard", element_fire,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/7/7d/Finubar.jpg/revision/latest?cb=20160120000131"),
    ("Wild Cursed Campfire", element_fire,
     "http://www.rachelhtmendell.com/wp-content/uploads/2017/07/fire-2197606_1920.jpg"),

    ("Crystal Lizard", element_ice, "http://darksouls3.wiki.fextralife.com/file/Dark-Souls-3/ravenous_liz.jpg"),
    ("Dwarf of the Northern Mountains", element_ice,
     "http://4.bp.blogspot.com/-5N1fMna0eOk/VAacUxkXs9I/AAAAAAAADks/ViQVG9mUREY/s1600/dwarf_by_armandeo64-d4sfgvm.jpg"),
    ("Evolved Fish", element_ice,
     "https://s-media-cache-ak0.pinimg.com/originals/4d/0f/8d/4d0f8d96222ee1840c2c388dc8997aea.jpg"),
    ("Frost Sorcerer Apprentice", element_ice,
     "https://i.pinimg.com/736x/e4/23/c3/e423c34e957a90ecf14e8dcacccaa92b.jpg"),
    ("Frozen Golem", element_ice,
     "https://i.pinimg.com/236x/a6/2d/f3/a62df3326559cb9ed161df2c6817fdb5--ice-magic-golem.jpg"),
    ("Lizardman with Magic Frost Weapon", element_ice,
     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRxmqhxYgUX30N8lidVmhS93NUaQjB-_ILTfNEqNKKUrEr-hr7Xg"),
    ("Northern High Elf", element_ice,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/6/64/Warhammer_High_Elf_Swordmasters_of_Hoeth.png/revision/latest?cb=20161205023222"),
    ("Snow Giant", element_ice,
     "https://orig00.deviantart.net/6cbb/f/2012/233/e/d/frost_giant_by_catherine_oc-d5bvjz1.jpg"),
    ("Cursed Ice Princess", element_ice,
     "https://cdna.artstation.com/p/assets/images/images/001/758/500/large/rafael-teruel-ice-queen-by-rafater-2.jpg?1452293194")
]

bosses = [
    ("Ogre Bruiser", element_none,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/2/2d/Warhammer_Ogre_Bruiser.png/revision/latest?cb=20170111040334"),
    ("Barbarian Chieftain", element_none,
     "https://s-media-cache-ak0.pinimg.com/originals/49/76/90/497690027055ec7531ab471f99d57426.jpg"),
    ("Kittycat", element_none,
     "https://78.media.tumblr.com/6c1510df7ab453cba61e892788d816e7/tumblr_inline_nzzow7CQuc1t77pl6_540.jpg"),

    ("Lord of Change", element_air, "https://spikeybits.com/wp-content/uploads/2014/11/fateweaver.jpg"),
    ("Valkia the Bloody", element_air,
     "https://s-media-cache-ak0.pinimg.com/originals/33/ac/2a/33ac2abb16e80727180259f8b05beb61.jpg"),
    ("Bloodthirsty Mosquito", element_air,
     "http://www.nma-fallout.com/data/photos/l/4/4582-1360416482-d0c43bc4f9ecaee2a7afa572444d9ad0.jpg"),

    ("Biribiri Herself", element_lightning, "https://i.imgur.com/2AhCKgV.png"),
    ("Dragon Ogre Shaggoth", element_lightning,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/0/0b/Kolek.png/revision/latest?cb=20160623213433"),
    ("Thunder Demi-god", element_lightning, "https://1d4chan.org/images/thumb/f/f8/SigThor.jpg/850px-SigThor.jpg"),

    ("Black Ork Boss", element_dark,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/d/d2/Untitled3232.jpg/revision/latest?cb=20131002023457"),
    ("Demon Prince", element_dark, "https://spikeybits.com/wp-content/uploads/2017/03/Demon-Prince.jpg"),
    ("Unknown Mutation", element_dark,
     "https://i.pinimg.com/736x/60/34/88/603488c24a5a10662ad451738afe2cec--warhammer-fantasy-warhammer-k.jpg"),
    ("Vampire Count", element_dark,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/7/74/Mannfred_von_Carstein.PNG/revision/latest?cb=20150724201838"),

    ("Experienced Dwarf King", element_holy,
     "https://vignette.wikia.nocookie.net/warhammerfb/images/f/fc/Thorgrim.jpg/revision/latest?cb=20160418145644"),
    ("Spear of the Holy Church", element_holy, "http://www.postavy.cz/foto/halflight-spear-of-the-church-foto.jpg"),
    ("Young Dragon", element_holy,
     "https://cdnb.artstation.com/p/assets/images/images/005/275/043/large/john-stone-holy-dragon-by-john-stone-art-db2ox97.jpg?1489830207"),

    ("Chaos Demon of Khorne", element_fire,
     "https://vignette.wikia.nocookie.net/warhammer40k/images/1/17/Bloodthirster_by_columbussage-d47j02l.jpg/revision/latest?cb=20120117042500"),
    ("Phoenix", element_fire, "http://i90.photobucket.com/albums/k276/starry1_night/phoenixskyJPG.jpg"),
    ("Pyrese Dragon", element_fire,
     "https://vignette.wikia.nocookie.net/risingdawn/images/c/c1/Pyrese.jpg/revision/latest?cb=20131222230556"),

    ("Mammoth", element_ice, "https://i.ytimg.com/vi/ilr_CRV9MQ4/maxresdefault.jpg"),
    ("Yeti", element_ice, "https://img00.deviantart.net/b76e/i/2006/316/5/a/yeti_by_andreauderzo.jpg")
]
adventureSecrets = [
    ("you saw something shiny when you followed a bird", "Money", 100),
    ("a strange creature you saved gave you his thanks", "Money", 100),
    ("you cought a thief for a nearby shopowner", "Money", 150),
    ("you killed a running skaven thief", "Money", 150),
    ("you found a treasure chest", "Money", 200),
    ("you found a naked guy in a cave and stole his ring", "Money", 200),
    ("you sold some junk at a salesman near the road", "Money", 250),
    ("you freed a wealthy nobleman from his bindings", "Money", 100),
    ("someone thought you were a jester and gave you something out of pity", "Money", 50),
    ("you turned some old iron into gold", "Money", 200),
    ("you sold some spoils of war", "Money", 90),
    ("you earned some money by delivering a bounty", "Money", 180),
    ("you got a reward for destroying a demon", "Money", 220),
    ("you earned a medal, but sold it immediately", "Money", 140),

    ("an old lady shared a meal with you", "Health", 100),
    ("you got lost and rested at a small lake", "Health", 200),
    ("a nice old lady gave you a red apple", "Health", 150),

    ("you found a nest of little griffins and made the wise decision to run", "Exp", 100),
    ("you sparred with an old friend", "Exp", 100),
    ("you listened to another adventurer's tales", "Exp", 150),
    ("you got through the scary part of nearby woods", "Exp", 150),
    ("you talked to some strange travellers", "Exp", 200),
    ("you saw big creatures fighting in the distance and learned some moves", "Exp", 250),
    ("your mom read you an interesting bed-time-story", "Exp", 50),
    ("you slaughtered and ate some ferocious white rabbits", "Exp", 100),
    ("you assisted a fat mom by capturing her cat", "Exp", 120),
    ("you watched some wise people play an intense game of chess", "Exp", 180),
    ("you entertained the village orphans", "Exp", 160),

    ("you fell off the road and climbed back up", "Weaponskill", 1),
    ("you learned some new combat skills in a barfight", "Weaponskill", 2),

    ("a blacksmith in a small village tought you some tricks", "Damage", 2),
    ("you found a spell that could increase your weapon's effectiveness", "Damage", 1),

    ("you got distracted by nature", "A good feeling", 1),
    ("a fluffy little creature gave you a hug", "A good feeling", 1)
]




