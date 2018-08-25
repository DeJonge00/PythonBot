# Discord Python Bot "Biribiri"
#### Notes
`words`: literally the word(s) in the brackets (choices separated by a `,`)\
`{words}`: variable string, describing any word(s) you need\
`{user}`: Mentioning the user, or giving a name in text (using only characters in a-z, A-Z or 0-9)
this second will prompt you to choose an option if multiple are found.\
\
The response message `Hahaha, no.` indicates that you lack the permissions to use the command.\
\
Biribiri is still in development, comments and improvements are welcome (`{prefix}helpserver` or message `Nya#2698` to contact me)


### Reactions to messages

|Message                                |Reaction
|---                                    |---
|`\o/`                                  |Praise the sun!
|`ded` (After a period of no messages)  |Cry about a ded chat
|`(╯°□°）╯︵ ┻━┻`                        | `┬─┬ ノ( ゜-゜ノ)`
|Mentions, `biri` or `biribiri`         |I will talk to your lonely self

### Basic commands

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|botstats       |`botstats,botinfo`                                     |Show stats of the bot in an embed
|cast        	|`cast` `{user}`                                        |Cast a spell targeted at `{user}`
|compliment  	|`compliment` `{user}`                                  |Give `{user}` a compliment
|countdown      |`countdown` `{seconds}`                                |Ping on times until the seconds run out (dms only for spam reasons)
|delete      	|`del,delete,d` `{seconds}` `{normal message}`          |Make biri delete your message after `{seconds}` seconds
|echo        	|`echo` `{text}`                                        |Biri repeats `{text}`
|emoji       	|`emoji` `{emoji}`                                      |Send a big version of `{emoji}`
|emojify     	|`emojify` `{text}`                                     |Transform `{text}` to regional indicators
|face        	|`face`                                                 |Send a random ascii face
|hug         	|`hug` `{user}`                                         |Give `{user}` a hug
|hype           |`hype`                                                 |Make hype by sending 10 random emoji from the current server
|kick        	|`kick` `{user}`                                        |Fake kick someone
|kill        	|`kill` `{user}`                                        |Wish someone a happy death (is a bit explicit)
|lenny       	|`lenny` `{message}`                                    |Send `{message}` ( ͡° ͜ʖ ͡°)
|lottery     	|`lottery` `{description}`                              |Set up a lottery, ends when creator adds the correct reaction
|pat         	|`pat` `{user}`                                         |Pat a user, keeps track of pats
|role        	|`role` `{role}` `{user}`                               |Add or remove `{role}` to `{user}` (needs permissions with exceptions of `muted` and `nsfw`)
|serverinfo  	|`serverinfo,serverstats`                               |Get the server's information
|urban       	|`urban,us,urbandictionary` `{query}`                   |Search urbandictionary for `{query}`
|userinfo    	|`userinfo,user,info` `{user}`                          |Get `{user}`'s information
|wikipedia   	|`wikipedia,wiki` `{query}`                             |Search wikipedia for `{query}`

### Image commands

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|fps         	|`fps,60`                                               |Send a high-fps gif
|biribiri    	|`biribiri,biri`                                        |Send pics of the only best girl
|cat         	|`cat`                                                  |Pictures of my cats
|cuddle      	|`cuddle`                                               |Send a cuddly gif
|ded         	|`ded`                                                  |Ded chat reminder (image)
|heresy      	|`heresy`                                               |Send images worthy of the emperor (warhammer 40k)
|happy          |`happy`                                                |Send a happy gif
|lewd           |`lewd`                                                 |Send anti-lewd gif
|nonazi      	|`nonazi`                                               |Try to persuade Lizzy with anti-nazi-propaganda!
|nyan           |`nyan`                                                 |Send an anime happy catgirl gif
|otter          |`otter`                                                |Send a cute otter picture
|plsno          |`plsno`                                                |Send a gif that expresses 'pls no'
|pp          	|`pp,avatar,picture` `{user}`                           |Show `{user}`'s profile pic, a bit larger
|sadness        |`sadness`                                              |Send a sad gif

### Hangman

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|hangman     	|`hm, hangman` `create,new` `{custom,sentence}`         |Create a new hangman game
|               |`hm, hangman` `{guess}`                                |Guess a letter/sentence in the current hangman game

### Minesweeper

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|minesweeper  	|`minesweeper,ms`                                       |Minesweeper game
|               |`minesweeper,ms` `create,new` `{height}` `{width}` `{mines}`  |Create a new minesweeper board
|               |`minesweeper,ms` `{x}` `{y}`                           |Guess a non-mine at coordinates (x,y)
|               |`minesweeper,ms` `quit`                                |Forfeit the current game

### Misc

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|inviteme    	|`inviteme`                                             |Invite me to your own server
|helpserver  	|`helpserver`                                           |Join my masters discord server if questions need answering

### Mod

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|setwelcome  	|`setwelome` `{message}`                                |Sets a welcome message
|setgoodbye  	|`setgoodbye` `{message}`                               |Sets a goodbye message
|nickname    	|`nickname,nn` `{user}` `{new_name}`                    |Nickname a person
|banish      	|`banish` `{user}`                                      |Ban `{user}`
|purge       	|`purge` `{amount}` `{user}`                            |Remove `{user}`'s messages (all if user is not given) from the past `{amount}` messages

### Config
|Name			        |Command, aliases and usage					            |Description
|---			        |---										            |---
|toggledeletecommands   |`toggledeletecommands,tdc`                             |Toggles whether commands will be deleted. Commands are deleted by default
|togglecommand          |`togglecommand,tc` `server,channel` `{command name}`   |Toggles whether the command `{command name}` can be used in the current `server,channel`. All commands are enabled by default


### MusicPlayer

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|music          |`music,m`                                              |All music commands start with ``{prefix}`music` or ``{prefix}`m`
|reset          |`music,m` `reset`                                      |Reset the player for this server
|leave          |`music,m` `leave,l`                                    |Let Biri leave voice chat
|skip           |`music,m` `skip,s` `{number}`                          |Vote to skip a song, or just skip it if you are the requester
|               |                                                       |No number given means voting to skip the current song
|queue          |`music,m` `queue,q`                                    |Show the queue 
|               |`music,m` `queue,q` `{songname,url}`                   |Add a song to the queue
|repeat         |`music,m` `repeat,r`                                   |Repeat the current song
|volume         |`music,m` `volume,v`                                   |Change the volume of the songs
|current        |`music,m` `current,c`                                  |Show information about the song currently playing
|stop           |`music,m` `stop`                                       |Empty the queue and skip the current song, then leave the voice channel
|play           |`music,m` `play,p`                                     |Pause or resume singing 
|               |`music,m` `play,p` `{songname,url}`                    |Add a song to the queue
|join           |`music,m` `join,j`                                     |Let Biri join a voice channel

### RPGGame

|Name			|Command, aliases and usage					            |Description
|---			|---										            |---
|rpg            |`rpg,b&d,bnd` `help`                                   |Show the info for the RPG game
|role           |`rpg,b&d,bnd` `r,role` `rolename`                      |Assign yourself a role (required to start the game)
|adventure      |`rpg,b&d,bnd` `a,adventure` `{time}`                   |Go on an adventure to slay monsters
|wander         |`rpg,b&d,bnd` `w,wander` `{time}`                      |Go wandering, its a less costly adventuring
|battle         |`rpg,b&d,bnd` `b,battle` `{user}`                      |Battle another player of the game
|info           |`rpg,b&d,bnd` `i,info` `{user}`                        |View a user's battlestats
|               |`rpg,b&d,bnd` `i,info` `weapon,w,armor,a` `{user}`     |View a user's weapon/armor stats
|party          |`rpg,b&d,bnd` `p,party`                                |Show the current party that will challenge the boss at the hour mark
|join           |`rpg,b&d,bnd` `j,join`                                 |Join the upcoming bossfight
|king           |`rpg,b&d,bnd` `k,king`                                 |Show who is the server's current king
|               |`rpg,b&d,bnd` `k,king` `c,b,challenge,battle`          |Challenge the king (level 10 required)
|levelup        |`rpg,b&d,bnd` `levelup,lvlup,lvl`                      |Claim your levelup rewards
|top            |`rpg,b&d,bnd` `top` `exp,money,bosstier`               |Show the top players of the game
|pet            |`rpg,b&d,bnd` `pet,pets`                               |Show the pets you own
|               |`rpg,b&d,bnd` `pet,pets` `r,release,remove` `{pet number}` |Release a pet to make room for a different one
|train          |`t,train` `ws,weapon,weaponskill`                      |Train your weaponskill
|               |`t,train` `h,hp,health,maxhealth`                      |Train your maximum healthpool
|shop           |`s,shop` `armor`                                       |Show shop armor inventory
|               |`s,shop` `armor` `{itemnumber}`                        |Buy armor number `{itemnumber}`
|               |`s,shop` `item`                                        |Show shop item inventory
|               |`s,shop` `item` `{itemnumber}`                         |Buy item number `{itemnumber}`
|               |`s,shop` `weapon`                                      |Show shop weapon inventory
|               |`s,shop` `weapon` `{itemnumber}`                       |Buy weapon number `{itemnumber}`

[![Discord Bots](https://discordbots.org/api/widget/244410964693221377.svg)](https://discordbots.org/bot/244410964693221377)