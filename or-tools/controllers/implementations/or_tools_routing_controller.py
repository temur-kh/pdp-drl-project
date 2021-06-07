import itertools
import logging
from typing import List

from controllers import RoutingControllerABC
from domain import Graph, TransportUnit, Query
from services import ORToolsOptimizerServiceABC, ORToolsOptimizerConfig, ORToolsOptimizerInputParams, ORToolsOutput


class ORToolsRoutingController(RoutingControllerABC):
    def __init__(self, optimizer_service: ORToolsOptimizerServiceABC):
        super().__init__(optimizer_service)

    @staticmethod
    def _union_dicts(*dicts):
        return dict(itertools.chain.from_iterable(dct.items() for dct in dicts))

    def construct_routes(self, graph: Graph, units: List[TransportUnit], queries: List[Query]):
        config = ORToolsOptimizerConfig()
        node_idx = {val: i for i, val in enumerate(graph.data.nodes)}
        idx_node = {i: val for i, val in enumerate(graph.data.nodes)}

        A = [(node_idx[o], node_idx[d]) for o, d in graph.data.edges] + \
            [(node_idx[d], node_idx[o]) for o, d in graph.data.edges] + \
            [(node_idx[n], node_idx[n]) for n in graph.data.nodes]
        P = [node_idx[q.origin_node] for q in queries]
        D = [node_idx[q.destination_node] for q in queries]
        origin_idx = node_idx[graph.origin_depot]
        destination_idx = node_idx[graph.destination_depot]
        V = [origin_idx] + P + D + [destination_idx]
        K = [i for i, _ in enumerate(units)]
        n = len(queries)
        s = {node_idx[n[0]]: n[1]['operation_time'] for n in graph.data.nodes(data=True)}
        c = {(o, d): graph.data.get_edge_data(idx_node[o], idx_node[d])['cost']
        if graph.data.has_edge(idx_node[o], idx_node[d]) else 0 for o, d in A}
        t = {(o, d): graph.data.get_edge_data(idx_node[o], idx_node[d])['time']
        if graph.data.has_edge(idx_node[o], idx_node[d]) else 0 for o, d in A}
        init_q = {node_idx[q.origin_node]: q.capacity for i, q in enumerate(queries)}  # didn't consider weight
        neg_q = {node_idx[q.destination_node]: -q.capacity for i, q in enumerate(queries)}
        q = self._union_dicts({origin_idx: 0}, init_q, neg_q, {destination_idx: 0})
        Q = {i: u.capacity for i, u in enumerate(units)}
        L = {i: u.max_working_time for i, u in enumerate(units)}
        a = {node_idx[n[0]]: n[1]['open_time'] for n in graph.data.nodes(data=True)}
        b = {node_idx[n[0]]: n[1]['close_time'] for n in graph.data.nodes(data=True)}

        params = ORToolsOptimizerInputParams(A=A, V=V, P=P, D=D, K=K, n=n, s=s, c=c, t=t, q=q, Q=Q, L=L, a=a, b=b)
        logging.info(params)
        output: ORToolsOutput = self.optimizer_service.solve(params, config)

        res_x = [{'from': idx_node[k[0]], 'to': idx_node[k[1]], 'unit_id': units[k[2]].id, 'value': v} for k, v in
                 output.x.items()]
        res_T = [{'node': idx_node[k[0]], 'unit_id': units[k[1]].id, 'value': v} for k, v in output.T.items()]
        res_Q = [{'node': idx_node[k[0]], 'unit_id': units[k[1]].id, 'value': v} for k, v in output.Q.items()]
        result = {'x': res_x, 'T': res_T, 'Q': res_Q}
        return result
