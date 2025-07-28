import json
from pyvis.network import Network as VisNetwork


VIS_NETWORK_OPTIONS = {
    "physics": {
        "repulsion": {
        "centralGravity": 1,
        "springLength": 5,
        "springConstant": 0.025,
        "nodeDistance": 510,
        "damping": 1
        },
        "minVelocity": 0.75,
        "solver": "repulsion"
    }
}


class Network:

    @staticmethod
    def _populate_network(node_set, edge_set):
        network = VisNetwork()
        network.set_options(json.dumps(VIS_NETWORK_OPTIONS))
        for node in node_set:
            network.add_node(node)
        for n1, n2 in edge_set:
            network.add_edge(n1, n2)
        return network

    def create(self, node_set, edge_set, path):
        network = self._populate_network(node_set, edge_set)
        network.show(path, notebook=False)    #< Writes a html file with the graph.