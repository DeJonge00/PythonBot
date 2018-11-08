from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from secret.secrets import api_username, api_password, APIAddress, APIPort
from database import general, rpg

route_start = ''
ASC = 1
DESC = -1

api = Flask(__name__)
auth = HTTPBasicAuth()
CORS(api)


@auth.get_password
def get_password(username):
    if username == api_username:
        return api_password
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# ----- /commands -----
@api.route(route_start + '/commands', methods=['GET'])
@auth.login_required
def get_command_counters():
    r = general.get_table(general.COMMAND_COUNTER_TABLE).find({}, {'_id': 0}).sort('timestamp', DESC).limit(100)
    return jsonify(list(r))


# ----- /rpg -----
@api.route(route_start + '/rpg/players', methods=['GET'])
@auth.login_required
def get_rpg_players():
    r = rpg.get_table(rpg.RPG_PLAYER_TABLE).find({}, {'_id': 0}).sort('exp', DESC).limit(25)
    return jsonify(list(r))


@api.route(route_start + '/rpg/players/<str:name>', methods=['GET'])
@auth.login_required
def get_rpg_player(name: str):
    r = rpg.get_table(rpg.RPG_PLAYER_TABLE).find({'name': name}, {'_id': 0}).sort('exp', DESC).limit(25)
    return jsonify(list(r))


# ----- Standard errors -----
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({f'Error 404': 'Resource could not be found'}), 404)


if __name__ == '__main__':
    api.run(host=APIAddress, port=APIPort, debug=False)
