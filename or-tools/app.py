import logging

from flask import Flask, jsonify
from flask.logging import default_handler

from controllers import ORToolsRoutingController
from endpoints import RoutingEndpoint
from services import ORToolsOptimizerService
from utils import EngineError, ResponseBuilder

logging.basicConfig(level=logging.INFO)
root = logging.getLogger()
root.handlers[0].setFormatter(default_handler.formatter)

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

or_tools_optimizer_service = ORToolsOptimizerService()
routing_controller = ORToolsRoutingController(or_tools_optimizer_service)
routing_endpoint = RoutingEndpoint(routing_controller)
app.add_url_rule('/routing/json', methods=['POST'], view_func=routing_endpoint.construct_routes)

response_builder = ResponseBuilder()


@app.errorhandler(EngineError)
def handle_error(error):
    response, status_code = response_builder(error=error)
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(debug=True)
