import scrapy
from scrapy import Request
from ..items import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        count = 1
        start_url = response.url
        page_url = start_url
        while count <= 2:
            yield Request(url=page_url,
                          callback=self.parse_area_page)
            count += 1
            page_url = start_url + '&pageset=' + str(count)

    def parse_area_page(self, response):

        property_all_links = response.css(".h4-space a").xpath("@href").extract()
        for item in property_all_links:

            link = 'https://londonrelocation.com' + item
            yield Request(url=link,
                          callback=self.parse_property_page)

    def parse_property_page(self, response):

        entry = Property()

        title = response.css("h1::text").extract()[0]
        price = response.css("h3::text").extract()[0].split()[0][1:]
        link = response.url

        entry['title'] = title
        entry['price'] = price
        entry['url'] = link
        yield entry
