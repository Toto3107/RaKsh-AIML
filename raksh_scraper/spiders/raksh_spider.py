import scrapy

class UniversalFetcher(scrapy.Spider):
    name = "universal_fetcher"

    def __init__(self, target_url=None, topic=None, *args, **kwargs):
        super(UniversalFetcher, self).__init__(*args, **kwargs)
        self.start_urls = [target_url]
        self.topic = topic # e.g., "Finance" or "Medical"

    def start_requests(self):
        for url in self.start_urls:
            # The 'impersonate' key triggers the TLS/JA3 stealth
            yield scrapy.Request(
                url, 
                meta={"impersonate": "chrome124"}, # Mimics a real modern browser
                callback=self.parse
            )

    def parse(self, response):
        # We capture the entire raw HTML. 
        # The "Correctness" of the dataset happens in the next step (The Brain).
        yield {
            "topic": self.topic,
            "url": response.url,
            "html": response.text,
            "status": response.status
        }