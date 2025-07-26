import asyncio
import os
from crawl4ai import AsyncWebCrawler
from crawl4ai import BrowserConfig, CrawlerRunConfig, CrawlResult, BFSDeepCrawlStrategy, LXMLWebScrapingStrategy
from datetime import datetime


DATA_PATH = "./data" 
VERSION = 1  #< Record keeping.


def _helper_format_preamble(url, max_depth, max_pages) -> str:
    current_date = datetime.now().strftime("%m-%d-%y %H:%M")
    line = ""
    line += f"% (created {current_date}) V.{VERSION}\n"
    line += f"% url: {url}\n"
    line += f"% LIMIT depth to {max_depth}\n"
    line += f"% LIMIT pages to {max_pages}\n"
    return line
    

def _helper_format_crawl_result(result: CrawlResult) -> str:
    line = ""
    line += result.url + ","
    for link in result.links["internal"]:
        line += link["href"] + ","
    line = line.rstrip(",") + "\n"
    return line


async def deep_crawl(url: str, max_depth: int, max_pages: int, out_file: str):
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=max_depth, 
            max_pages=max_pages,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )
    with open(out_file, "w") as file:
        async with AsyncWebCrawler() as crawler:
            results: List[CrawlResult] = await crawler.arun(
                url=url,
                config=config
            )
            file.write(
                _helper_format_preamble(url, max_depth, max_pages)
            )
            file.write(f'{len(results)}\n')
            for result in results:
                if result.success:
                    file.write(
                        _helper_format_crawl_result(result)
                    )


async def extraction_mode():
    filename = input("Enter name for the out file (e.g. 'uoregon_edu'): ")
    out_file = os.path.join(DATA_PATH, filename + '.csv')
    while os.path.exists(out_file):
        if input('Warning: the name is taken. Overwrite [y]? ') == 'y':
            break
        filename = input("Enter name for the out file (e.g. 'uoregon_edu'): ")
        out_file = os.path.join(DATA_PATH, filename + '.csv')
    domain = input("Enter domain (e.g. 'uoregon.edu'): ")
    url = 'https://' + domain
    max_depth = input("Enter max depth (e.g. 2): ")
    while True:
        try:
            max_depth = int(max_depth)
            break
        except:
            max_depth = input("(invalid input): Enter max depth (e.g. 2):" )
    max_pages = input("Enter max pages (e.g. 1000): ")
    while True:
        try:
            max_pages = int(max_pages)
            break
        except:
            max_pages = input("(invalid input): Enter max pages (e.g. 1000): ")
    await deep_crawl(url, max_depth, max_pages, out_file)


def main():
    GOODBYE = "Invalid input. Goodbye!"
    mode = input("Hello! Please select [1] webscrape a domain or [2] visualize sitemap: ")
    try:
        mode = int(mode)
    except:
        return print(GOODBYE)
    
    match mode:
        case 1:
            asyncio.run(extraction_mode())
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