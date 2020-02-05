# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import CrawlingWebItem
import re

class WowSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # kindle unlimited book list
    start_urls = ['https://www.amazon.cn/s?bbn=116169071&rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cp_n_feature_nineteen_browse-bin%3A1338154071&dc&fst=as%3Aoff&qid=1580463937&rnid=1338153071&ref=lp_116169071_nr_p_n_feature_nineteen_0']

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_first_page)

    def parse_first_page(self, response):
        total_pages = response.xpath("//ul[@class='a-pagination']/li[@class='a-disabled']/text()").extract()[-1]
        self.total_pages = int(total_pages)
        yield from self.parse_list(response)

    def parse_list(self, response):
        sels = response.xpath("//div[@data-index]//a[contains(@class, 'a-link-normal a-text-normal')]")
        for sel in sels:
            item = CrawlingWebItem()
            full_name = sel.xpath("./span/text()").extract_first()
            link = sel.xpath("./@href").extract_first()
            link = response.urljoin(link)
            item["full_name"] = full_name
            item["link"] = link
            yield Request(url=link, callback=self.parse_book, meta={"item": item})
        # whether next page is available
        cp = response.xpath("//ul[@class='a-pagination']/li[@class='a-selected']/a/text()").extract_first()
        current_page = int(cp)
        if current_page < self.total_pages:
            next_url = response.xpath("//ul[@class='a-pagination']/li[@class='a-last']/a/@href").extract_first()
            next_url = response.urljoin(next_url)
            yield Request(url=next_url, callback=self.parse_list)

    def parse_book(self, response):
        item = response.meta["item"]
        price = response.xpath("//span[@class='extra-message olp-link']/a/text()").extract_first()
        price = re.search("[\d\.]+", price).group()
        sels = response.xpath("//div[@id='ps-content']")
        pre_time = "".join(sels.xpath("./div[@class='buying']/span/text()").extract())
        desc = sels.xpath(".//div[@id='postBodyPS']/div").extract_first()
        description = re.sub("<[^>]+>", "", desc)
        item["price"] = price
        item["present_time"] = pre_time
        item["description"] = description
        yield item