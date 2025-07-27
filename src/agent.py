from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CrawlResult, BFSDeepCrawlStrategy, LXMLWebScrapingStrategy, FilterChain, ContentTypeFilter, URLPatternFilter, DomainFilter
from datetime import datetime
import json


async def deep_crawl(config, out_path):
    bfs_deep_crawl_strategy_kwargs = {}
    filters = []
    if 'url' not in config:
        raise Exception('Missing url in config.')
    if 'url_pattern_filter' in config:
        filters.append(URLPatternFilter(
            patterns=config['url_pattern_filter']
        ))
    if 'content_type_filter' in config:
        filters.append(ContentTypeFilter(
            allowed_types=config['content_type_filter']
        ))
    if 'domain_filter' in config:
        filters.append(DomainFilter(
            allowed_domains=config['domain_filter'].get('allowed_domains', []),
            blocked_domains=config['domain_filter'].get('blocked_domains', []),
        ))
    if len(filters) > 0:
        bfs_deep_crawl_strategy_kwargs['filter_chain'] = FilterChain(filters)
    if 'max_depth' in config:
        bfs_deep_crawl_strategy_kwargs['max_depth'] = config['max_depth']
    if 'max_pages' in config:
        bfs_deep_crawl_strategy_kwargs['max_pages'] = config['max_pages']
    crawler_run_config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            **bfs_deep_crawl_strategy_kwargs,
            include_external=False
        ),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True
    )
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(
            url=config['url'],
            config=crawler_run_config
        )
        successful_results = list(filter(lambda res: res.success, results))
        with open(out_path, 'w') as f:
            f.write(__helper_format_preamble(config))
            f.write(f"{len(successful_results)}\n")
            for res in successful_results:
                f.write(__helper_format_result(res))


def __helper_format_preamble(config) -> str:
    preamble = f"% (created: {datetime.now().strftime("%m-%d-%y %I:%M %p")})\n"
    json_str = json.dumps(config, indent=4)
    for line in json_str.splitlines():
        preamble += f"% {line}\n"
    preamble += "% NOTE: the first url on each line is the source; all subsequent urls are internal links found on that source.\n"
    return preamble


def __helper_format_result(result) -> str:
    line = f"{result.url},"
    for link in result.links['internal']:
        line += link['href'] + ","
    line = line.rstrip(",") + "\n"
    return line

    