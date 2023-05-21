from flask import Flask
from flask_cors import CORS
from routes.blueprint import blueprint
from utils.utils import make_graph
from controllers.route_controller import shortest_path

elena = Flask(__name__)
CORS(elena)
elena.register_blueprint(blueprint, url_prefix='/elena')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    src = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
    # dest = "University of Massachusetts Amherst, Mullins Way, Hadley, Hampshire County, Massachusetts, 01003"
    dest = "Puffers Pond, Amherst"
    shortest_path(src, dest, 'min', 25, 'walk', "Amherst", "Massachusetts")

    # # for server run
    # elena.run(host='127.0.0.1', port=5000, debug=True)
