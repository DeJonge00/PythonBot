from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from secret.secrets import api_username, api_password, APIAddress, APIPort
from database import general

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


# ----- /containers -----
@api.route(route_start + '/commands', methods=['GET'])
@auth.login_required
def get_containers():  # Returns one instance for every id, sorted by timestamp
    r = general.get_table(general.COMMAND_COUNTER_TABLE).find({}, {'_id': 0}).sort({'timestamp': DESC}).limit(100)
    return jsonify(r)


# ----- Standard errors -----
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({f'Error 404': 'Resource could not be found'}), 404)


if __name__ == '__main__':
    api.run(host=APIAddress, port=APIPort, debug=False)
