import scrapy
import json
from scrapy import Selector

from ..items import StartupItem


class StartupSpider(scrapy.Spider):
    name = 'startup'
    allowed_domains = ['e27.co']
    count = 0
    COUNT_MAX = 500

    def start_requests(self):
        url = 'https://e27.co/startups'
        for page in range(1, 33):
            url += '/load_startups_ajax?all&per_page={}&append=1&_=2018-08-29_13:37:36_03' \
                                 ''.format(page)
            yield scrapy.Request(url, callback=self.page_parse)

    def page_parse(self, response):
        data = json.loads(response.body)
        content = data['pagecontent'].strip()
        startups = Selector(text=content).xpath('//div[@class="startup-block"]')
        for startup in startups:
            if self.count < self.COUNT_MAX:
                url = startup.xpath('.//a[1]/@href').extract_first() + '?json'
                self.count += 1
                yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        item = StartupItem()
        content = response.body.strip()
        header = Selector(text=content).xpath('//div[@class="page-head"]')
        profile_content = Selector(text=content).xpath('//div[@class="profile-content"]')
        item['company_name'] = header.xpath('.//h1[@class="profile-startup"]/text()').extract_first()
        item['request_url'] = response.url.replace('?json', '')
        item['request_company_url'] = header.xpath('.//a[1]/@href').extract_first()
        item['location'] = header.xpath('.//div[@class="mbt"]/span[3]/a/text()').extract_first()
        item['tags'] = header.xpath('.//div[contains(@style, "word-wrap")]/span/a/text()').extract()
        item['founding_date'] = header.xpath('.//p[contains(text(), "Founded:")]/span/text()').extract_first()
        item['urls'] = header.xpath('.//div[contains(@class, "socials")]/a/@href').extract()
        item['description_short'] = header.xpath('.//div[h1[@class="profile-startup"]]/div[1]/text()').extract_first()
        item['founders'] = profile_content.xpath('.//span[contains(text(), "ounder")]/'
                                                 'preceding-sibling::span/a/text()').extract()
        item['description'] = profile_content.xpath('.//p[@class="profile-desc-text"]/text()').extract_first()
        item['employee_range'] = ''
        item['emails'] = ''
        item['phones'] = ''
        yield item
