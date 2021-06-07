from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined
import networkx as nx


@dataclass_json(undefined=Undefined.RAISE)
@dataclass
class Graph:
    data: nx.Graph  # attributes: time, cost, start_time, close_time
    origin_depot: str
    destination_depot: str

    def __init__(self, **kwargs):
        self.data = nx.Graph(kwargs['nodes_dict'])
        nx.set_node_attributes(self.data, kwargs['node_attrs'])
        self.origin_depot = kwargs['origin_depot']
        self.destination_depot = kwargs['destination_depot']
