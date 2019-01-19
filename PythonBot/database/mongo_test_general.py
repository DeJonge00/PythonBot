from general import *
from pprint import pprint


def test_welcome_goodbye():
    print(get_message(WELCOME_TABLE, 'serverid'))
    set_message(WELCOME_TABLE, 'serverid', 'channelid', 'Welcome message {} uwu')
    print(get_message(WELCOME_TABLE, 'serverid'))

    get_table(WELCOME_TABLE).drop()

    print(get_message(GOODBYE_TABLE, 'serverid'))
    set_message(GOODBYE_TABLE, 'serverid', 'channelid', 'Goodbye message {} uwu')
    print(get_message(GOODBYE_TABLE, 'serverid'))

    get_table(GOODBYE_TABLE).drop()


def test_do_not_delete():
    print(get_delete_commands('serverid'))
    print(toggle_delete_commands('serverid'))
    print(get_delete_commands('serverid'))
    print(toggle_delete_commands('serverid'))
    print(get_delete_commands('serverid'))

    get_table(DO_NOT_DELETE_TABLE).drop()

def test_banned_command():
    print(get_banned_command(SERVER_ID, 'server_id_1', 'commandname'))
    print(toggle_banned_command(SERVER_ID, 'server_id_1', 'commandname'))
    print(get_banned_command(SERVER_ID, 'server_id_1', 'commandname'))
    print(toggle_banned_command(SERVER_ID, 'server_id_1', 'commandname'))
    print(get_banned_command(SERVER_ID, 'server_id_1', 'commandname'))

def test_roles():
    print(get_roles('server_id_1', 'role_id_1'))
    print(toggle_role('server_id_1', 'role_id_1'))
    print(get_roles('server_id_1', 'role_id_1'))
    print(toggle_role('server_id_1', 'role_id_1'))
    print(get_roles('server_id_1', 'role_id_1'))


if __name__ == '__main__':
    # test_welcome_goodbye()
    # test_do_not_delete()
    # test_banned_command()
    test_roles()