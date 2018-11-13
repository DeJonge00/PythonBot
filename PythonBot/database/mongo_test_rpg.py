from database import rpg, pats, common
from rpgplayer import RPGPlayer, BUSY_DESC_BOSSRAID, BUSY_DESC_ADVENTURE
from rpgpet import RPGPet
from random import randint


def test_rpg_channel():
    server = '1'
    channel = '2'
    rpg.set_rpg_channel(server, channel)
    channel = rpg.get_rpg_channel(server)
    print('Setchannel/getchannel', channel, channel == channel)

    channel = '3'
    rpg.set_rpg_channel(server, channel)
    channel = rpg.get_rpg_channel(server)
    print('Setchannel/getchannel', channel, channel == channel)

    rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_rpg_player():
    player = RPGPlayer(userid='1', picture_url='', username='owo', health=10)

    try:
        rpg.get_player(player.userid, player.name)
    except ValueError:
        print('No user successful')

    rpg.update_player(player)
    print(player.name)
    for k, v in rpg.get_player(player.userid, player.name).as_dict().items():
        print(k, v)

    rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_top_list():
    players = [RPGPlayer(userid=str(x), picture_url='', username=str(x), exp=x).as_dict() for x in range(400)]
    rpg.get_table(rpg.RPG_PLAYER_TABLE).insert_many(players)

    print('0-10')
    for i in rpg.get_top_players(group='exp', start=0, amount=10):
        print(i)

    print('11-20')
    for i in rpg.get_top_players(group='exp', start=300, amount=10):
        print(i)

        rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_boss_parties():
    players = [RPGPlayer(userid=str(x), picture_url='', username=str(x)) for x in range(400)]
    for p in players:
        p.set_busy(BUSY_DESC_BOSSRAID, 10, randint(0, 10))
    rpg.get_table(rpg.RPG_PLAYER_TABLE).insert_many([x.as_dict() for x in players])

    for k, v in rpg.get_boss_parties().items():
        print(k, len(v))

    rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_add_stat():
    player = RPGPlayer(userid='1', picture_url='', username='owo', pets=[RPGPet(name=str(x)) for x in range(2)])
    rpg.update_player(player)
    exp = player.exp
    rpg.add_stats(player.userid, 'exp', 10)
    print('Player exp from-to', exp, rpg.get_player(player.userid, player.name).exp)

    exp = [p.exp for p in rpg.get_player(player.userid, player.name).pets]
    rpg.add_pet_stats(player.userid, 'exp', 10)
    print('Pet exp from-to', exp, [p.exp for p in rpg.get_player(player.userid, player.name).pets])

    rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_decrement_busy_counters():
    players = [RPGPlayer(userid=str(x), picture_url='', username=str(x)) for x in range(10)]
    for p in players:
        p.set_busy(BUSY_DESC_ADVENTURE, 20, randint(0, 10))
    rpg.get_table(rpg.RPG_PLAYER_TABLE).insert_many([x.as_dict() for x in players])

    rpg.decrement_busy_counters()
    for x in rpg.get_table(rpg.RPG_PLAYER_TABLE).find():
        print(x.get('busy').get('time'))

    rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_get_done_players():
    players = [RPGPlayer(userid=str(x), picture_url='', username=str(x)) for x in range(10)]
    for p in players:
        p.set_busy(BUSY_DESC_ADVENTURE, randint(0, 2), '1')
    rpg.get_table(rpg.RPG_PLAYER_TABLE).insert_many([x.as_dict() for x in players])

    print('Done players', len(list(rpg.get_done_players())))
    print('Player busytimes', [x.get('busy').get('time') for x in rpg.get_table(rpg.RPG_PLAYER_TABLE).find()])

    rpg.get_table(rpg.RPG_PLAYER_TABLE).drop()


def test_pats():
    r = pats.increment_pats('1', '2')
    print(r)

    common.get_table(pats.PAT_DATABASE, pats.PAT_TABLE).drop()
