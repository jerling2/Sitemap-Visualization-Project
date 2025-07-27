import os
import json
import asyncio
from pathlib import Path
from agent import deep_crawl


class ExtractionMode():
    def __init__(self, data_path, config_path):
        self.data_path = data_path
        self.config_path = config_path
        self.config = None

    def load_config(self, path_to_config: str):
        with open(path_to_config, "r") as file:
            self.config = json.load(file)

    def _get_available_configs(self) -> [str]:
        configs = []
        for item in Path(self.config_path).glob("*.json"):
            configs.append(item.stem)
        return configs

    def _prompt_for_config(self) -> str:
        config_name = None
        available_configs = self._get_available_configs()
        while not config_name:
            user_input = input(f"Please select a config {available_configs}: ")
            if user_input not in available_configs:
                print("(error: unrecognized config)")
            else:
                config_name = user_input
        path_to_config = os.path.join(self.config_path, config_name + ".json")
        return path_to_config

    def _prompt_for_out(self) -> str:
        out_path = None
        while not out_path:
            user_input = input("Please enter a name for the output file (e.g. uoregon): ")
            temp_path = os.path.join(self.data_path, user_input + ".csv")
            if os.path.exists(temp_path) and input("(Error:) Name is taken. Overwrite [y]? ") == "y":
                out_path = temp_path
            elif not os.path.exists(temp_path):
                out_path = temp_path
        return out_path
        
    def interact(self):
        path_to_config = self._prompt_for_config()
        try:
            self.load_config(path_to_config)
        except Exception as e:
            return print(f"An unexpected error occured: {e}")
        out_path = self._prompt_for_out()
        asyncio.run(deep_crawl(self.config, out_path))
