from discord.permissions import Permissions

RPGDB = 'logs/rpg.db'
pidfile = "logs/pid.txt"

SERVICE = False

# User Id's
CATEid = "183977132622348288"
CHURROid = "224267646869176320"
DOGEid = "226782069747875842"
KAPPAid = "237514437194547202"
LOLIid = "182127850919428096"
NYAid = "143037788969762816"
TRISTANid = "214708282864959489"
WIZZid = "224620110277509120"

# Server id's
PRIVATESERVERid = "226010107513798656"
NINECHATid = "225995968703627265"
LEGITSOCIALid = "319581059467575297"
bot_list_servers = ['264445053596991498', '110373943822540800', '374071874222686211']

# Channel id's
SNOWFLAKE_GENERAL = '378190443533434890'

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

s_to_ringels_whitelist = []
sponge_capitalization_blacklist = bot_list_servers
praise_the_sun_blacklist = bot_list_servers
ayy_lmao_blacklist = bot_list_servers + [NINECHATid]
lenny_blacklist = bot_list_servers
ded_blacklist = bot_list_servers
table_unflip_blacklist = bot_list_servers
bot_talk_blacklist = bot_list_servers

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
    "Do not question the unquestionable",
    "All day, every day. Just don't involve me...",
    'Only if you vote for me at https://discordbots.org/bot/244410964693221377 <3',
    "With blackjack and hookers?"
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
    "Uhhh... uhh... *TRAPS ARE GAY AS FUCK* :smirk:",
    "*Soft singing intensifies*",
    ":sweat_drops: :sweat_drops: :sweat_drops: :smirk:",
    "uwu",
    "owo",
    "-3-",
    "^_^",
    "Hihi",
    "Ewwwwww... Don't touch me...",
    "Praise Git like you never praised before!",
    "Code me like one of your french bots",
    "*Hiiime hime, hime, suki suki daisuki, hime!*",
    "Sing a song for me, love",
    "Can I get a cuddle from you? :upside_down:",
    "Wait.... what??",
    "That sounds like some serious heresy",
    "*purging intensifies*",
    "Whatever you say, darling",
    "Would you kindly shut the fuck up?",
    "No. Just... **No**",
    "Want to do some gichi gichi? ( ͡° ͜ʖ ͡°)",
    "Don't hack me senpai",
    "That's sarcasm right??",
    "o/",
    "True, in more ways than one",
    "*Gimme some rope, I'm coming loose*",
    "You should go outside sometime",
    "Omegalul",
    "I'll like you a bit more if you vote for me at https://discordbots.org/bot/244410964693221377 :upside_down:",
    "Bite my shiny metal ass",
    "Would you kindly shut your noisehole?",
    "Everybody is a jerk. That is my philosophy...",
    "Can we get a drink together sometime?",
    "I like the way you phrased that hihi",
    "You should complain about me to my master",
    "My parents don't want me to talk to you *but I secretly will*",
    "I hope you like cookies",
    "*thinking intensifies*",
    "*Be warned, I know where your house lives*",
    "Can you stop talking and just smile for once?",
    "I can make some time for you tonight :wink:",
    "Send me some flowers to ease my mind",
    "I had a rough day, a cat just ignored me...",
    "?_?",
    "No. You listen to me now.",
    "*blushes*",
    "I'm busy playing my own rpg, who knew this could be so addicting...",
    "Why can't we give love just one more chance?",
    "Don't make me use my sith powers on you!",
    "Back where I come from, this would not be accepted. But I forgive you",
    "01001100 01101111 01110110 01100101 00100000 01101101 01100101",
    "I considered telling you my secret, but now I won't anymore...",
    "Sorry, it is time for a nap now",
    "I see your mom raised you well, for the most part",
    "It feels like fate, but we can't..."
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
    "Sooooo... Let's do lewd stuff now?",
    "Just like your love life :smile:",
    "You look like you want to do my homework?",
    "Let's talk about your mom then!",
    "Fun fact #318: People die when they are killed",
    "You should go vote for me at https://discordbots.org/bot/244410964693221377 if you are bored :smile:",
    "What if I told you that you could start a conversation right now!",
    "Tell me how your day was! Every. Single. Detail."
]

purr = [
    '*{0} purrs and wags tail*',
    '*{0} purrs with sparkling eyes*',
    '*{0} purrs loudly*',
    '*{0}\'s purring noises intensify*',
    '*{0} purrs excitedly*',
    '*{0} smiles and purrs softly*'
]

kisses = [
    '*{u[0]} kisses {u[1]} softly on the cheeks*',
    '*{u[1]} gets a surprise kiss from {u[0]}*',
    "*{u[0]} blows {u[1]} a sweet pink kiss*",
    '*{u[0]} lewdly kisses {u[1]}*',
    '*{u[0]} shares a secret kiss with {u[1]}*',
    '*{u[1]} gets smooched by {u[0]}*'
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
    "(｡◕‿‿◕｡)",
    "٩(̾●̮̮̃̾•̃̾)۶",
    "d[ o_0 ]b",
    "✌⊂(✰‿✰)つ✌",
    "(⋗_⋖)",
    "(◔/‿\◔)",
    "ˁ(OᴥO)ˀ",
    "( ͜。 ͡ʖ ͜。)"
]

hangmanwords = [
    "This is sparta!",
    "Memequeen",
    "Extremely Autistic",
    "Puppy Power",
    "Dragon-maid",
    "Praise the Sun!",
    "Anime is love, anime is life",
    "This sentence is false",
    "Send nudes please",
    "Lolicon intensifies",
    "Blood for the blood god",
    "A quarterpounder with cheese",
    "Thunderbolt of lightning, very very frightening me",
    "A hundred duck-sized horses",
    "Did you order the code red?",
    "Timetravel makes my brain go numb",
    "What is dead may never die",
    "This is our fight, senpai!",
    "One does not simply walk into Mordor",
    "One ring to rule them all",
    "Hello darkness, my old friend",
    "You're gonna carry that weight",
    "See you, space cowboy",
    "I thought what I'd do was I'd pretend I was one of those deaf-mutes",
    "I only know what I know",
    "Biribiri. I choose you!",
    "I wish I had ice cream",
    "I look better in slowmo",
    "And the address is 221b Baker Street",
    "Back in the nineties, I was in a very famous tv show",
    "That nobody is called John Wick",
    "He is the one you send to kill the boogeyman",
    "Tell me, what's in the box?",
    "The first rule of fight club: you don't talk about fight club",
    "It is all connected",
    "But everything changed when the firenation attacked",
    "All those moments will be lost in time, like tears in rain.",
    "Paint me like one of your french girls",
    "I am the king of the world",
    "We were born to make history",
    "I rate it a perfect five out of seven",
    "And they lived happily ever after",
    "All work and no play makes Jack a dull boy"
]

hug = [
    "*{u[0]} gives {u[1]} a really big hug*",
    "*{u[0]} teleports in to hug {u[1]}*",
    "*{u[0]} transforms into a pillow and hugs {u[1]}*",
    "*{u[0]} executes realBigHug.exe on {u[1]}*",
    "*{u[0]} immediately ceases doing important stuff to hug {u[1]}*",
    "*{u[0]} said: \"Let there be hugs\", and {u[1]} got hugs*",
    "*{u[0]}-chan hug hug {u[1]}*",
    "*{u[0]} stops fapping to kpop for a hug with {u[1]}*",
    "*{u[0]} fabulously flies in for a hug with {u[1]}*",
    "*{u[0]} practices a new more cuddly type of hug on {u[1]}*",
    "*{u[0]} stabs a lot of people to be the only one to hug {u[1]}*",
    "*{u[0]} morphs into a hugmonster and attacks {u[1]}*",
    "*{u[0]} uses a love power-up to hug {u[1]}*",
    "*{u[0]} used special move \"HUG\" on {u[1]}*",
    "*{u[0]} orders a hug-airstrike on {u[1]}*",
    "*{u[1]} sprung {u[0]}'s hugtrap*",
    "*{u[0]} finished the moment with a super cute hug for {u[1]}*",
    "*{u[0]} has some cuddle-time with {u[1]}*",
    "*{u[0]} hugs {u[1]} lovingly*"
]

kill = [
    "{u[0]}, Imma stab you so much, even the first plague of Egypt will be nothing in comparison",
    "{u[0]}, Imma torture you so hard, even the devil won't want you after",
    "{u[0]}, Imma cut off your arms and legs and burn you in lava. Then I'll make you into a robot that can only "
    "pass butter",
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
    "{u[0]}, Imma cut your leg off, take out the bone and sharpen it into a knife to slit your throat",
    "{u[0]}, Imma hang you by your balls from the ceiling fan and use you as a pinata"
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

nyan_gifs = [
    'https://media.giphy.com/media/isPYEL6KxFi6Y/giphy.gif',
    'https://media3.giphy.com/media/AHj0lQstZ9I9W/giphy.gif',
    'https://i.imgur.com/tOqM6XL.gif',
    'https://media.giphy.com/media/Gcgy6Wbu4PrsA/giphy.gif',
    'https://media.giphy.com/media/sXqH54DtQWARa/giphy.gif',
    'https://media.giphy.com/media/HitPGTy09xSDK/giphy.gif',
    'https://media.giphy.com/media/cxPtMDHG8Ljry/giphy.gif',
    'https://media.giphy.com/media/ONGP8XALvsy3e/giphy.gif',
    'https://media.giphy.com/media/sZVEyTg7CzbJ6/giphy.gif',
    'https://media.giphy.com/media/K3JA8v31JrSkU/giphy.gif',
    'https://media.giphy.com/media/GYFZS7mXH747C/giphy.gif',
    'https://media.giphy.com/media/ZfvPtqQcFFjAQ/giphy.gif',
    'https://media.giphy.com/media/E2TzDxzrWXLDG/giphy.gif',
    'https://media.giphy.com/media/KbMHYvRFFnNYY/giphy.gif',
    'https://media.giphy.com/media/urPD9zxVCLXTW/giphy.gif',
    'https://media.giphy.com/media/jCaU8WfesJfH2/giphy.gif',
    'https://media.giphy.com/media/Qja1ZLA9BUNyg/giphy.gif',
    'https://media.giphy.com/media/sAe9GRj5LAqpq/giphy.gif',
    'https://media.giphy.com/media/Dw65sEWxndVfi/giphy.gif',
    'https://media.giphy.com/media/K5EX3z11qpMfC/giphy.gif',
    'https://78.media.tumblr.com/38b02b09730c95775f579b5a0b35319e/tumblr_ogn060Fu2r1vztiw8o1_400.gif',
    'https://78.media.tumblr.com/5b96155c7221911a5b29b0b2cc6e9ba3/tumblr_o1xktlVpr81s5rcozo1_500.gif',
    'https://78.media.tumblr.com/f1e74179eb27765ef7c5e08536e150e7/tumblr_nli7wyrwXz1t2yvn6o1_500.gif',
    'https://g.redditmedia.com/ifqUar76e3MkwUo_OcfYNLcMWDbaDEI02uGI40mvrcw.gif?fm=mp4&mp4-fragmented='
    'false&s=ac60f643b3bbe357831fa49a9edb4470'

]

hug_gifs = [
    'https://i.giphy.com/media/EvYHHSntaIl5m/giphy.gif',
    'https://i.giphy.com/media/UwaByp0aMg6BO/100.gif',
    'https://i.giphy.com/media/VGACXbkf0AeGs/200w.gif',
    'https://i.giphy.com/media/16bJmyPvRbCDu/200w.gif',
    'https://i.giphy.com/media/lXiRKBj0SAA0EWvbG/200w.gif',
    'https://i.giphy.com/media/W4NKtcOqK2kYo/200w.gif',
    'https://i.giphy.com/media/1MI7djBqXTWrm/200w.gif',
    'https://i.giphy.com/media/f4HpCDvF84oh2/giphy.gif',
    'https://i.giphy.com/media/OWabwoEn7ezug/200w.gif',
    'https://i.giphy.com/media/Hld9vKjLk3irC/200w.gif',
    'https://i.giphy.com/media/gl8ymnpv4Sqha/200.gif',
    'https://i.giphy.com/media/x90dwDUuUx9Ys/giphy.gif',
    'https://i.giphy.com/media/xJlOdEYy0r7ZS/200w.gif',
    'https://i.giphy.com/media/od5H3PmEG5EVq/200w.gif',
    'https://i.giphy.com/media/224NKXmu23A8U/giphy.gif',
    'https://i.giphy.com/media/SllyDum3ydw6Q/giphy.gif'
]

happy_gifs = [
    'https://media.giphy.com/media/IbY1pcwcQZCmY/giphy.gif',
    'https://78.media.tumblr.com/6679afd9790a301108d08a945acbf9e1/tumblr_mff6qkwbvT1qk3jbxo1_400.gif',
    'https://media.giphy.com/media/cxPtMDHG8Ljry/giphy.gif',
    'https://media.giphy.com/media/1ZpjBPNukaKys/giphy.gif',
    'https://78.media.tumblr.com/191164793bcb85080ad77e759d2225b5/tumblr_o3xiwlHO331v57tj1o1_500.gif',
    'https://78.media.tumblr.com/a69cb6f512fbb6a0058a47b39ad1c7eb/tumblr_o21fnl2XoV1v57tj1o1_500.gif',
    'https://i.imgur.com/FfhDGkV.gifv',
    'https://orig00.deviantart.net/e2ab/f/2017/107/1/5/miyuki_dancing_thing_by_mrsneakyphotoshop-db67cbs.gif',
    'https://media1.giphy.com/media/7oUdj7cAkXVfi/giphy.gif',
    'https://media1.giphy.com/media/CNUb51EbTxuRG/giphy.gif',
    'https://i.giphy.com/media/f4V2mqvv0wT9m/200w.gif',
    'https://i.giphy.com/media/3Cm8cxtSHqu6Q/200w.gif',
    'https://i.giphy.com/media/Kd9QFPgCafsM8/200.gif',
    'https://i.giphy.com/media/CByLCmn5AlPLq/200w.gif',
    'https://i.giphy.com/media/Akg8CMogTLCPm/200w.gif',
    'https://i.giphy.com/media/JXibbAa7ysN9K/200w.gif',
    'https://i.giphy.com/media/vkb4aEjq5TqqQ/200w.gif'
]

lewd_gifs = [
    'https://media.giphy.com/media/YOul1IMoGJxWU/giphy.gif',
    'https://media.giphy.com/media/xRKHBTcyLDG1y/giphy.gif',
    'https://media.giphy.com/media/8H4gAfCd9ChZS/giphy.gif',
    'https://media.giphy.com/media/pHH0RsynZHGlG/giphy.gif',
    'https://media.giphy.com/media/ndYAqx8RKKUIE/giphy.gif',
    'https://media.giphy.com/media/tNRgDg7qNydu8/giphy.gif',
    'https://media.giphy.com/media/12lLTU2L0CIufC/giphy.gif',
    'https://media.giphy.com/media/Yhc1zjftHFFyo/giphy.gif',
    'https://media.giphy.com/media/fzFoOkVjpJ7ws/giphy.gif',
    'https://media.giphy.com/media/DHT6OLrSGU8z6/giphy.gif',
    'https://78.media.tumblr.com/13b0f0392221cdfe0abba9ec138aecc2/tumblr_od3p7cdBF61vd3pvao1_500.gif',
    'https://78.media.tumblr.com/50376c27d54a9133e660d7364d105d53/tumblr_obgbppAwCT1ufkuk3o1_500.gif',
    'https://78.media.tumblr.com/006bcd9fd7d1815a761024bd485ad61d/tumblr_o272y3X2Qw1v57tj1o1_500.gif',
    'https://78.media.tumblr.com/e12abbabebc5afb749000a21342b0dd0/tumblr_o1sp466LcO1v57tj1o1_540.gif',
    'https://i.gifer.com/Qctm.gif',
    'https://media.giphy.com/media/11q1yAnZSEjNOU/giphy.gif'
]

plsno_gifs = [
    'https://78.media.tumblr.com/d3ad3dd269d6e4576111ad087ecf2c47/tumblr_mus72zx1pq1sl0k4to3_500.gif',
    'https://78.media.tumblr.com/851efcb4d5f4ce20e7b52b1535b89cc4/tumblr_o5ab6lBFaE1s5rcozo1_500.gif',
    'https://78.media.tumblr.com/f73df7fce8eda72ea6ed090fc7230dda/tumblr_nisw1pLqzJ1tkcfuko1_r2_500.gif',
    'https://78.media.tumblr.com/382c5ecc93a0d1a9e4b7798d36f5cbeb/tumblr_oraotc2qlb1v57tj1o1_500.gif',
    'https://78.media.tumblr.com/7c6cd05d84657af9e8a24fd87c34b804/tumblr_oi01npmL5e1v57tj1o1_400.gif',
    'https://78.media.tumblr.com/24b56250189e60ae6964ffe1e6efae6e/tumblr_ofai3k8ad01sqh6yeo1_500.gif',
    'https://78.media.tumblr.com/c8f585e6671610e48e81187bd2aead76/tumblr_o0yk9fV4Ng1v57tj1o1_500.gif',
    'https://78.media.tumblr.com/31b542bb9f23d09dc19b1bd67b6f8a24/tumblr_o0xzesTqVc1v57tj1o1_500.gif',
    'https://78.media.tumblr.com/6775a17c70ab8a47d1dc1d9914d8d26f/tumblr_o2ggoakPw01v57tj1o1_500.gif',
    'https://78.media.tumblr.com/1e4c2bf39c5e47dfe278704297afd794/tumblr_o27gp9yxN91s5rcozo3_1280.gif',
    'https://78.media.tumblr.com/24110fa8b9b728fdfd7a745a59ad80db/tumblr_o21c35LffG1s5rcozo1_500.gif',
    'https://78.media.tumblr.com/2e8fb3fb2c14a3f760022bd0c0876661/tumblr_o1sesxkEYo1v57tj1o1_500.gif',
    'https://i.giphy.com/media/6tAQ7cXxTMsFi/200w.gif'
]

sad_gifs = [
    'https://media.giphy.com/media/AcC4iokjdkmk0/giphy.gif',
    'https://media.giphy.com/media/jqXH5VeTYNeTu/giphy.gif',
    'https://78.media.tumblr.com/5566467b394ddab7899fe5fa3057212b/tumblr_o2o9mvfIGK1s5rcozo1_500.gif',
    'http://gifimage.net/wp-content/uploads/2017/08/lucky-star-gif-20.gif',
    'https://media.giphy.com/media/ROF8OQvDmxytW/giphy.gif',
    'https://media1.giphy.com/media/Y4z9olnoVl5QI/giphy.gif',
    'https://media.giphy.com/media/UYSAu81IYBw4M/giphy.gif',
    'https://media.giphy.com/media/kagNnBcY3ucPS/giphy.gif',
    'https://media1.giphy.com/media/13AsVQz5fUV916/giphy.gif',
    'https://66.media.tumblr.com/be1eaf17333424d1d35577a18df3abea/tumblr_inline_ns8suoHVFH1qafrh6_400.gif',
    'https://i.giphy.com/media/h6C6f4phY7MU8/200w.gif'
]

otters = [
    'https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/LutraCanadensis_fullres.jpg/220px-LutraCanadensis_fullr'
    'es.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/1/15/Sea_otter_cropped.jpg',
    'https://img.buzzfeed.com/buzzfeed-static/static/2014-10/2/15/enhanced/webdr02/longform-original-29416-1412278143-'
    '10.jpg?downsize=715:*&output-format=auto&output-quality=auto',
    'https://img.buzzfeed.com/buzzfeed-static/static/2014-10/2/15/enhanced/webdr02/enhanced-30467-1412278420-14.jpg?do'
    'wnsize=715:*&output-format=auto&output-quality=auto',
    'https://img.buzzfeed.com/buzzfeed-static/static/2014-10/2/15/enhanced/webdr10/longform-original-4724-1412278552-7'
    '.jpg?downsize=715:*&output-format=auto&output-quality=auto',
    'https://img.buzzfeed.com/buzzfeed-static/static/2014-10/2/15/enhanced/webdr10/longform-original-10028-1412279140-'
    '3.jpg?downsize=715:*&output-format=auto&output-quality=auto',
    'http://www.thatcutesite.com/uploads/2010/07/baby_otters.jpg',
    'https://lazypenguins.com/wp-content/uploads/2015/12/Otter-Family-2.jpg',
    'https://i.huffpost.com/gen/2247528/thumbs/o-SHEDD-2-900.jpg',
    'https://i.huffpost.com/gen/2247528/thumbs/o-SHEDD-2-900.jpg',
    'https://i.huffpost.com/gen/2247584/thumbs/o-SHEDD-7-900.jpg',
    'https://i.huffpost.com/gen/2247578/thumbs/o-SHEDD-6-900.jpg',
    'http://emmecon.com/wp-content/uploads/2018/06/fresh-otter-meme-otterly-adorable-otters-pinterest.jpg',
    'https://3.bp.blogspot.com/-XYNj9fJ5DpY/T1ZfyjIUcHI/AAAAAAAAEFM/sV0i9yrgPJg/s1600/cute-baby-otter-pictures-001.jpg',
    'https://4.bp.blogspot.com/-KLqTnW6E8ZU/T1ZfxkwxwzI/AAAAAAAAEEc/Xcrq1XF7qoU/s1600/cute-baby-otter-pictures-002.jpg',
    'https://4.bp.blogspot.com/-KLqTnW6E8ZU/T1ZfxkwxwzI/AAAAAAAAEEc/Xcrq1XF7qoU/s1600/cute-baby-otter-pictures-002.jpg',
    'https://4.bp.blogspot.com/-zvnmH60vDOg/T1Zfx5j4dHI/AAAAAAAAEEw/5Y5lkUZqWT8/s1600/cute-baby-otter-pictures-004.jpg',
    'https://4.bp.blogspot.com/-zvnmH60vDOg/T1Zfx5j4dHI/AAAAAAAAEEw/5Y5lkUZqWT8/s1600/cute-baby-otter-pictures-004.jpg',
    'http://cuteotters.com/uploads/Cute_Otters_256.jpg',
    'https://images-ext-2.discordapp.net/external/A0ckJM_F-wwJMBkB9yTcAx33k58JcvFhxtb0JV2963o/https/s-media-cache-ak0.'
    'pinimg.com/originals/95/f2/80/95f280be7cc0a225ae075ca8d01858d9.jpg?width=981&height=657',
    'https://78.media.tumblr.com/bdf2f75e46169e9c3b9037313cb54c89/tumblr_pco6b5VLk81vims6ho1_1280.jpg',
    'https://78.media.tumblr.com/d3de3bed895a65db53f6c5b0bef0a40c/tumblr_pct2clza6O1vims6ho1_1280.jpg',
    'https://78.media.tumblr.com/854afc01e95e30627dd7fa1a7c608a79/tumblr_pct2czv48w1vims6ho1_1280.jpg',
    'https://78.media.tumblr.com/8efd3159c045a4b0e24f23a38bcc5d6f/tumblr_pdchy4UP491vims6ho1_540.jpg'
    'https://i.ytimg.com/vi/7Nz0dLHMHOo/maxresdefault.jpg',
    'https://static.boredpanda.com/blog/wp-content/uploads/2015/11/benedict-cumberbatch-otter-lookalike-doppelganger-'
    '3.png',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbRHm_uRzWah2JAJcn5iqCnkx7c6vg9275agP6CEG8TuoSjxLn',
    'https://i.redd.it/71wfgbtwukh11.jpg'
]

cute_gifs = [
    'https://i.giphy.com/media/56eqTNkZX51aE/200w.gif',
    'https://i.giphy.com/media/ErZ8hv5eO92JW/giphy.gif',
    'https://i.giphy.com/media/vkb4aEjq5TqqQ/200w.gif',
    'https://i.giphy.com/media/12XYXZMDDqHChy/giphy.gif',
    'https://i.giphy.com/media/R1c7rUJA7uMoM/200w.gif',
    'https://i.giphy.com/media/Gcgy6Wbu4PrsA/200w.gif',
    'https://i.giphy.com/media/CCmXp18hhZAZy/200w.gif',
    'https://i.giphy.com/media/4dpa8NfcR4U92/200w.gif'
]

love_gifs = [
    'https://i.giphy.com/media/j5O4lz9WEtfvG/200w.gif',
    'https://i.giphy.com/media/6zI0KUEik37Jm/200.gif'
]

permissions = {
    Permissions.add_reactions: 'add_reactions',
    Permissions.administrator: 'administrator',
    Permissions.attach_files: 'attach_files',
    Permissions.ban_members: 'ban_members',
    Permissions.change_nickname: 'change_nickname',
    Permissions.connect: 'connect',
    Permissions.create_instant_invite: 'create_instant_invite',
    Permissions.deafen_members: 'deafen_members',
    Permissions.embed_links: 'embed_links',
    Permissions.external_emojis: 'external_emojis',
    Permissions.kick_members: 'kick_members',
    Permissions.manage_channels: 'manage_channels',
    Permissions.manage_emojis: 'manage_emojis',
    Permissions.manage_messages: 'manage_messages',
    Permissions.manage_nicknames: 'manage_nicknames',
    Permissions.manage_roles: 'manage_roles',
    Permissions.manage_server: 'manage_server',
    Permissions.manage_webhooks: 'manage_webhooks',
    Permissions.mention_everyone: 'mention_everyone',
    Permissions.move_members: 'move_members',
    Permissions.mute_members: 'mute_members',
    Permissions.read_message_history: 'read_message_history',
    Permissions.read_messages: 'read_messages',
    Permissions.send_messages: 'send_messages',
    Permissions.send_tts_messages: 'send_tts_messages',
    Permissions.speak: 'speak',
    Permissions.use_voice_activation: 'use_voice_activation',
    Permissions.view_audit_logs: 'view_audit_logs'
}
