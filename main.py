import asyncio
from src.config_helper import ExtractionMode


DATA_PATH = "./data"
CONFIG_PATH = "./configs" 


def main():
    GOODBYE = "Invalid input. Goodbye!"
    mode = input("Hello! Please select [1] webscrape a domain or [2] visualize sitemap: ")
    try:
        mode = int(mode)
    except:
        return print(GOODBYE)
    
    match mode:
        case 1:
            program = ExtractionMode(DATA_PATH, CONFIG_PATH)
            program.interact()
        case 2:
            print("two")
        case _:
            return print(GOODBYE)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")