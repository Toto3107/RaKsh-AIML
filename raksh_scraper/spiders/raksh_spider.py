import scrapy

class RakshSpider(scrapy.Spider):
    name = "raksh_spider"
    
    # CRITICAL: We remove start_urls = [] from here to prevent conflicts
    
    def __init__(self, start_url=None, *args, **kwargs):
        super(RakshSpider, self).__init__(*args, **kwargs)
        # We explicitly set the start_url passed from the ETL pipeline
        if start_url:
            self.start_urls = [start_url]
            self.logger.info(f"🚀 Spider targeted at: {start_url}")
        else:
            self.start_urls = []
            self.logger.error("❌ No URL provided to the spider!")

    def parse(self, response):
        # Extract meaningful text from common content tags
        text_content = " ".join(response.css('p::text, h1::text, h2::text, li::text').getall())
        
        yield {
            "url": response.url,
            "text": text_content[:4000], # Send a healthy chunk to Gemini
            "status": "extracted"
        }