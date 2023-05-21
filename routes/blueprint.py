from flask import Blueprint
from controllers.route_controller import shortest_path, index

blueprint = Blueprint('elena', __name__)

blueprint.route('/', methods=['GET'])(index)
blueprint.route('/shortestpath', methods=['POST'])(shortest_path)
