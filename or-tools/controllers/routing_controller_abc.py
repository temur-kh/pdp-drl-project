from typing import List

from domain import Graph, TransportUnit, Query
from services import ORToolsOptimizerServiceABC


class RoutingControllerABC:
    def __init__(self, optimizer_service: ORToolsOptimizerServiceABC):
        self.optimizer_service = optimizer_service

    def construct_routes(self, graph: Graph, units: List[TransportUnit], queries: List[Query]):
        pass

# OutputType
