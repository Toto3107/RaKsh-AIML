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
        # 1. Check if the response is actually a web page (text/html)
        if not hasattr(response, 'text'):
            self.logger.warning(f"⚠️ Skipping non-text content: {response.url}")
            return

        # 2. Extract text safely
        text_content = " ".join(response.css('p::text, h1::text, h2::text, li::text').getall())
        
        # 3. If it's a small page or failed extraction, try the body directly
        if len(text_content) < 100:
            text_content = response.body.decode('utf-8', errors='ignore')[:4000]

        yield {
            "url": response.url,
            "text": text_content,
            "status": "extracted"
        }