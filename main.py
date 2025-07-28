import asyncio
from src.config_helper import ExtractionMode
from src.data_helper import VisualizationMode


DATA_DIR = "./data"
CONFIG_DIR = "./configs" 
GRAPH_DIR = "./graphs"


def main():
    GOODBYE = "Invalid input. Goodbye!"
    mode = input("Hello! Please select [1] webscrape a domain or [2] visualize sitemap: ")
    try:
        mode = int(mode)
    except:
        return print(GOODBYE)
    
    match mode:
        case 1:
            program = ExtractionMode(DATA_DIR, CONFIG_DIR)
            program.interact()
        case 2:
            program = VisualizationMode(DATA_DIR, GRAPH_DIR)
            program.interact()
        case _:
            return print(GOODBYE)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")