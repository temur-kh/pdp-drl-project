import logging
from dataclasses import dataclass
from typing import List

from flask import request, jsonify
from dataclasses_json import dataclass_json

from controllers import RoutingControllerABC
from domain import Graph, Query, TransportUnit
from utils import EngineError


class RoutingEndpoint:
    def __init__(self, routing_controller: RoutingControllerABC):
        self.routing_controller = routing_controller

    @staticmethod
    def decode_request(request_json):
        routing_req: RoutingRequest = RoutingRequest.from_dict(request_json)
        queries = routing_req.queries
        transport_units = routing_req.transport_units

        graph_data = routing_req.graph_data
        graph: Graph = Graph(nodes_dict=graph_data.edges_dict,
                             node_attrs=graph_data.node_attrs,
                             origin_depot=graph_data.origin_depot,
                             destination_depot=graph_data.destination_depot)
        return graph, transport_units, queries

    @staticmethod
    def encode_response(response_data):
        return jsonify(response_data)

    def construct_routes(self):
        graph, transport_units, queries = self.decode_request(request.json)
        result = self.routing_controller.construct_routes(graph, transport_units, queries)
        response = self.encode_response(result)
        return response


@dataclass_json
@dataclass
class GraphDataRequest:
    edges_dict: dict
    node_attrs: dict
    origin_depot: str
    destination_depot: str


@dataclass_json
@dataclass
class RoutingRequest:
    graph_data: GraphDataRequest
    transport_units: List[TransportUnit]
    queries: List[Query]


class InvalidGraphDataError(EngineError):
    status_code = 400
