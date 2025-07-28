from src.shell import Shell
from src.network import Network
import json


COMMENT_SYMBOL = "%"


class VisualizationMode(Shell):
    def __init__(self, data_path, graph_path):
        super().__init__(data_path=data_path, graph_path=graph_path)
        self.network = Network()

    @staticmethod
    def __skip_comment_lines(file_ptr) -> str:
        """ Returns the first non-commented line if it exists. """
        for line in file_ptr:
            if not line.startswith(COMMENT_SYMBOL):
                return line
        return ""
    
    @staticmethod
    def __process_url_line(raw_line: str) -> (str, [str]):
        urls = raw_line.split(',')
        clean_urls = [url.rstrip("/\n") for url in urls]
        source, rest = None, []
        if clean_urls:
            source = clean_urls[0]
            rest = clean_urls[1:]
        return (source, rest)

    def _read_csv(self, path: str) -> [(str, [str])]:
        adjacency_list = []
        with open(path, "r") as f:
            _ = self.__skip_comment_lines(f)  #< I'm not using the 'size' line.
            for line in f:
                link_adjacency = self.__process_url_line(line)
                adjacency_list.append(link_adjacency)
        return adjacency_list

    @staticmethod
    def _generate_nodes_and_edges(adjacency_list):
        node_set = set()
        edge_set = set()
        for item in adjacency_list:
            source, rest = item
            if source in node_set:
                continue                #< This source is a duplicate, so skip.
            node_set.add(source)
            for url in rest:
                if (url, source) in edge_set:
                    continue                   #< Edge already exists, so skip.
                node_set.add(url)
                edge_set.add((source, url))
        return (node_set, edge_set)

    def _prompt_for_data(self):
        available_data = self._ls(self.data_path, glob_pattern="*.csv")
        if not available_data:
            return None
        user_input = input(f"Please select a dataset {available_data}: ")
        while user_input not in available_data:
            print("(error: unrecognized dataset)")
            user_input = input(f"Please select a dataset {available_data}: ")
        path = self._get_data_file_path(user_input)
        return path

    def _prompt_for_graph(self) -> str:
        user_input = input("Please enter a name for the output graph (e.g. my_graph): ")
        path = self._get_graph_file_path(user_input)
        while self._is_path_taken(path):
            if input("(Error:) Name is taken. Overwrite [y]? ") == "y":
                break
            user_input = input("Please enter a name for the output graph (e.g. my_graph): ")
            path = self._get_graph_file_path(user_input)
        return path

    def interact(self):
        data_path = self._prompt_for_data()
        if not data_path:
            return print("Uh oh, there's no data to visualize. Try again later.")
        adjacency_list = self._read_csv(data_path)
        node_set, edge_set = self._generate_nodes_and_edges(adjacency_list)
        graph_path = self._prompt_for_graph()
        self.network.create(node_set, edge_set, graph_path)
