import scrapy

class PsAtozItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    image_link = scrapy.Field()
    thermometer_rank = scrapy.Field()
    recent_category_rank = scrapy.Field()
    past_category_rank = scrapy.Field()
    rank_percent_change = scrapy.Field()
    average_rate = scrapy.Field()
    rate_qty = scrapy.Field()
    offers_qty = scrapy.Field()
    min_price = scrapy.Field()
    max_price = scrapy.Field()
