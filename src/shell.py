import json
import os
from pathlib import Path

class Shell:
    def __init__(self, data_path=None, config_path=None):
        self.data_path = data_path
        self.config_path = config_path

    @staticmethod
    def _load_json(path_to_json):
        json_data = None
        with open(path_to_json, "r") as file:
            json_data = json.load(file)
        return json_data

    @staticmethod
    def _ls(path, glob_pattern="*") -> [str]:
        result = []
        for item in Path(path).glob(glob_pattern):
            item_name_without_extension = item.stem
            result.append(item_name_without_extension)
        return result
    
    @staticmethod
    def _is_path_taken(path):
        return os.path.exists(path)

    def _get_data_file_path(self, filename):
        return os.path.join(self.data_path, filename + ".csv")

    def _get_config_file_path(self, filename):
        return os.path.join(self.config_path, filename + ".json")