import asyncio
from src.shell import Shell
from src.agent import deep_crawl


class ExtractionMode(Shell):
    def __init__(self, data_path, config_path):
        super().__init__(data_path=data_path, config_path=config_path)

    def _prompt_for_config(self) -> str:
        available_configs = self._ls(self.config_path, glob_pattern="*.json")
        user_input = input(f"Please select a config {available_configs}: ")
        while user_input not in available_configs:
            print("(error: unrecognized config)")
            user_input = input(f"Please select a config {available_configs}: ")
        path = self._get_config_file_path(user_input)
        return path

    def _prompt_for_out(self) -> str:
        user_input = input("Please enter a name for the output file (e.g. uoregon): ")
        path = self._get_data_file_path(user_input)
        while self._is_path_taken(path):
            if input("(Error:) Name is taken. Overwrite [y]? ") == "y":
                break
            user_input = input("Please enter a name for the output file (e.g. uoregon): ")
            path = self._get_data_file_path(user_input)
        return path
        
    def interact(self):
        path_to_config = self._prompt_for_config()
        if not path_to_config:
            return print("Uh oh, there's no configs in the configs directory.")
        try:
            config = self._load_json(path_to_config)
        except Exception as e:
            return print(f"An unexpected error occured: {e}")
        out_path = self._prompt_for_out()
        asyncio.run(deep_crawl(config, out_path))