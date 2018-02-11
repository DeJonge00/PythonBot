prefix = "<"
RPGDB = 'logs/rpg.db'
WELCOMEMESSAGEFILE = "logs/welcomeMessages.db"
GOODBYEMESSAGEFILE = "logs/leaveMessages.db"
PATSDB = "logs/pats.db"
pidfile = "logs/pid.txt"

SERVICE = False

# User Id's
NYAid = "143037788969762816"
LOLIid = "182127850919428096"
WIZZid = "224620110277509120"
CATEid = "183977132622348288"
TRISTANid = "214708282864959489"
KAPPAid = "237514437194547202"

# Server id's
PRIVATESERVERid = "226010107513798656"
NINECHATid = "225995968703627265"
LEGITSOCIALid = "319581059467575297"

ytdl_options = dict(
    format="bestaudio/best",
    extractaudio=True,
    audioformat="mp3",
    noplaylist=True,
    default_search="auto",
    quiet=True,
    nocheckcertificate=True
)

ytdl_before = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

# talking to bb
qa = [
            "What are you asking me for?",
            "*sigh*, go ask your dad...",
            "Why don't you think long and hard about that yourself?",
            "*paging... anyone: we have an annoying question here*",
            "Why should I be the one to give you that kind of information?",
            "---ACCESS DENIED: User not authorized---",
            "Maybe yes, maybe no, I can't be certain.",
            "Ehm.. Ehmmm... Yes???",
            "No, no, no, no pls :sob:",
            "To be or not to be, *that's* the question!",
            "Ask that your waifu, you weeb",
            "If there is one thing I am sure of, it is that traps are gay af",
            "About a 4% chance of that...",
            "Not. Even. Close.",
            "Do not question the unquestionable"
        ]

response = [
            "Sure, sure, now go away, I'm busy.",
            "きみはばかです",
            "*Yusss, someone talked to me!*",
            "Lol, it speaks.",
            "Go talk to your imaginary friends XD",
            "Hahahahaha :heart:",
            "Why don't we do those childish things somewhere else?",
            "Shhh, the grownups are talking.",
            "How do you even words?",
            "Ehhhmmmmm.... but why though?",
            "Did you have to say that in such a weird way?",
            "Sooooooo.... Rainbows?",
            "Praise the sun!",
            "I need some good food to digest that...",
            ":heart: Praise neko-sama :heart:",
            "If that really is what you want...",
            "Go to www.ponyhorses.com for some good vids",
            "Shut up, I don't talk to virgins on the internet",
            "I don't want to talk about that right now...",
            "I dare you: clownsong.com",
            "Too soon! You have awakened me too soon!",
            "You want *me* to talk to *you*??",
            "Awwwn... such a cute voice",
            "You sound like a pretty nice person",
            "I want you to treat me like a princess, pls!",
            "You need more hugs in your life...",
            "YES YES YES YES YES",
            "DEATH TO MY ENEMIES",
            "B-b-b-baka!",
            "*embarrassment intensifies*",
            "Give me a big hug!",
            "Send hearts <3",
            "Use the knife! You can do it!",
            "<@143037788969762816> send help daddy :sob:",
            "Uhhh... uhh... *TRAPS ARE GAY AS FUCK* :smirk:",
            "*Soft singing intensifies*",
            ":sweat_drops: :sweat_drops: :sweat_drops: :smirk:",
            "uwu",
            "owo",
            "-3-",
            "Ewwwwww... Don't touch me...",
            "Praise Git like you never praised before!",
            "Code me like one of your french bots"
        ]

# random responses
compliments = [
            "{u[0]} you look lovely today <3",
            "{u[0]} your smile is contagious",
            "{u[0]} I like your style",
            "{u[0]} you are the most perfect you there is",
            "{u[0]} you're an awesome friend",
            "{u[0]} you deserve a hug right now",
            "Is that {u[0]}'s picture next to 'charming' in the dictionary?",
            "{u[0]} is a perfect 5/7",
            "{u[0]} if cartoon bluebirds were real, a bunch of them would be sitting on your shoulders singing right now",
            "{u[0]} you're like sunshine on a rainy day",
            "Everything would be better if more people were like {u[0]}!",
            "I bet {u[0]} sweats glitter",
            "Being around {u[0]} makes everything better!",
            "{u[0]} you're better than a triple-scoop ice cream cone\nWith sprinkles",
            "{u[0]} being around you is like being on a happy little vacation",
            "{u[0]} could survive a Zombie apocalypse just by smiling",
            "{u[0]} you're more fun than bubble wrap",
            "{u[0]} who raised you? They deserve a medal for a job well done",
            "{u[0]} you're gorgeous -- and that's the least interesting thing about you, too",
            "Somehow {u[0]} makes time stop and fly at the same time",
            "I bet {u[0]} does the crossword puzzle in ink",
            "{u[0]} is even better than a unicorn, because {u[0]} is real"
        ]

ded = [
            "But I am here :/",
            "No you are ded *hmpf*",
            "Then go talk about something maybe?",
            "I wish I had more friends",
            ">resurrect",
            "Ehhmm.. Talk about your day?",
            "Ehhmm.. Why don't you talk about the color blue?",
            "How about we talk about unicorns?",
            "Why don't we play a game?",
            "Sooooo... Lets do lewd stuff now?",
            "Just like your love life :smile:",
            "You look like you want to do my homework?",
            "Let's talk about your mom then!"
        ]

faces = [
            "(づ◔ ͜ʖ◔)づ",
            "ヾ(๑╹◡╹)ﾉ\"",
            "(:point_up:︎ ՞ਊ ՞):point_up:︎",
            "(๑･̑◡･̑๑)",
            ":v:︎('ω'):v:︎",
            "ᕦ( ͡°╭͜ʖ╮͡° )ᕤ",
            "乁( ⁰͡ Ĺ̯ ⁰͡ ) ㄏ",
            "( ͡⌐■ ͜ʖ ͡-■)",
            "( ͡° ͜ʖ ͡°)>⌐■-■",
            "( ˊ̱˂˃ˋ̱ )",
            "̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿",
            "(▀̿Ĺ̯▀̿ ̿)",
            "( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)",
            "ლ(ಠ益ಠლ)",
            "(｡◕‿‿◕｡)"
        ]

hangmanwords = [
            "This is sparta!",
            "Memequeen",
            "Extremely Autistic",
            "Puppy Power",
            "Dragon-maid",
            "xXx-pussydestroyer-xXx",
            "Praise the Sun!",
            "Anime is love, anime is life",
            "This sentence is false",
            "Send nudes please",
            "Lolicon intensifies"
    ]

hug = [
            "{u[0]} gives {u[1]} a really big hug",
            "{u[0]} teleports in to hug {u[1]}",
            "{u[0]} transforms into a pillow and hugs {u[1]}",
            "{u[0]} executes realBigHug.exe on {u[1]}",
            "{u[0]} immediately ceases doing important stuff to hug {u[1]}",
            "{u[0]} said: \"Let there be hugs\", and {u[1]} got hugs",
            "{u[0]}-chan hug hug {u[1]}",
            "{u[0]} blows {u[1]} a sweet pink kiss",
            "{u[0]} stops fapping to kpop for a hug with {u[1]}",
            "{u[0]} fabulously flies in for a hug with {u[1]}",
            "{u[0]} practices a new more cuddly type of hug on {u[1]}",
            "{u[0]} stabs a lot of people to be the only one to hug {u[1]}",
            "{u[0]} morphs into a hugmonster and attacks {u[1]}",
            "{u[0]} uses a love power-up to hug {u[1]}",
            "{u[0]} used special move \"HUG\" on {u[1]}",
            "{u[0]} orders a hug-airstrike on {u[1]}",
            "{u[1]} sprung {u[0]}'s hugtrap",
            "{u[0]} finished the moment with a super cute hug for {u[1]}",
            "{u[0]} has some cuddle-time with {u[1]}",
            "{u[0]} *hugs {u[1]} lovingly*"
        ]

kill = [
            "{u[0]}, Imma stab you so much, even the first plague of Egypt will be nothing in comparison",
            "{u[0]}, Imma torture you so hard, even the devil won't want you after",
            "{u[0]}, Imma cut off your arms and legs and burn you in lava. Then I'll make you into a robot that can only pass butter",
            "{u[0]}, Imma leave you in a musquito-cage, covered in syrup, untill you've been sucked dry",
            "{u[0]}, Imma tickle you in 'places' untill you kill yourself",
            "{u[0]}, Imma let an alien hatch in you, and when it bursts out, I'll funnel it into your mouth",
            "{u[0]}, Imma let you get eaten by a shark, limb by limb, slowly",
            "{u[0]}, SECTUMSEMPRA, CRUCIO, AVADA KEDAVRA",
            "{u[0]}, Imma write you out of the script of life, so you will be meaninglessly forgotten",
            "{u[0]}, Imma strangle you while slowly inserting burning needles in your body",
            "{u[0]}, Imma make you cum to boku no pico",
            "{u[0]}, Imma code a big bug in you",
            "{u[0]}, Imma suck your intestines out with a vacuum cleaner",
            "{u[0]}, Imma use chaos magic to suck you into the void",
            "{u[0]}, Imma put you in a room full of sweaty, greasy old people",
            "{u[0]}, Imma starve you in a completely silent room",
            "{u[0]}, Imma prepare you like I would a fish, using a lot of salt in the process",
            "{u[0]}, Imma slit your throat slowly, using a hot salted knife",
            "{u[0]}, Imma tie your limbs with a rope so tight, they will die and fall off",
            "{u[0]}, Imma insert superglue in every hole on your body I can find",
            "{u[0]}, Imma cut your leg off, take out the bone and sharpen it into a knife to slit your throat"
            "{u[0]}, Imma hang you by your ballz from the ceiling fan and use you as a pinyata"
        ]

lewd = [
            "{u[0]} rubs {u[1]}'s exposed belly",
            "{u[1]} gets a nice suprise from {u[0]}: *buttsex*",
            "{u[0]} stares like never before at {u[1]}'s chest",
            "{u[0]} is fapping to \"Boku no {u[1]}\"",
            "{u[1]} SEND NUDES TO {u[0]}!!",
            "{u[1]} was abducted by aliens to be probed on video",
            "{u[1]} was abducted by {u[0]} and some candy",
            "{u[0]} adds {u[0]} to the harem using a van and icecream",
            "{u[0]} reads some lewd fanfiction about {u[1]}",
            "All {u[0]}'s lolis are cuddling {u[1]} to death!!"
    ]

spell = [
            "Fireball",
            "Frostbolt",
            "Drain Life",
            "Infernal Gateway",
            "Raise Dead",
            "Death Curse",
            "Bonecrusher",
            "Curse of the Leper",
            "Baleful Transmogrification",
            "Ecstatic Seizures",
            "Conflagration of Doom",
            "Pit of Shades",
            "Forked lightning",
            "Level 5 Railgun",
            "Cleansing Fire",
            "Steal Soul",
            "Wind of Death",
            "Doom and Darkness",
            "Hyperbeam"
        ]

spellresult = [
            # Good results
            "It's super effective!",    
            "An accurate hit!",
            "Target annihilated!",
            "Obliterated!",
            # Bad results
            "It misfired!",
            "It missed it's target!",
            "The target was immune!",
            "It was not very effective!"
        ]