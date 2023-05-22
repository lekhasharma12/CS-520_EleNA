from flask import Flask
from flask_cors import CORS
from routes.blueprint import blueprint

elena = Flask(__name__)
CORS(elena)
elena.register_blueprint(blueprint, url_prefix='/elena')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # for server run
    elena.run(host='127.0.0.1', port=5000, debug=True)
