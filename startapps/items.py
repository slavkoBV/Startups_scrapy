import scrapy


class StartupItem(scrapy.Item):

    company_name = scrapy.Field()
    request_url = scrapy.Field()
    request_company_url = scrapy.Field()
    location = scrapy.Field()
    tags = scrapy.Field()
    founding_date = scrapy.Field()
    founders = scrapy.Field()
    employee_range = scrapy.Field()
    urls = scrapy.Field()
    emails = scrapy.Field()
    phones = scrapy.Field()
    description_short = scrapy.Field()
    description = scrapy.Field()
