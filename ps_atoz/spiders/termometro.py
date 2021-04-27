import scrapy
import re


class TermometroSpider(scrapy.Spider):
    name = 'termometro'

    def __init__(self, start_url):
        self.start_urls = [start_url]

    def parse(self, response):
        item_list = response.css('ol#zg-ordered-list')
        items = item_list.css('li span.a-list-item')
        
        for item in items:
            min_price, max_price = self._get_prices(item)
            category_ranks = self._get_category_ranks(item)
            
            yield {
                'name': self._get_name(item),
                'link': response.urljoin(self._get_link(item)),
                'image_link': self._get_image_link(item),
                'thermometer_rank': self._get_thermometer_rank(item),
                'recent_category_rank': min(category_ranks),
                'past_category_rank': max(category_ranks),
                'rank_percent_change': self._get_rank_percent_change(item),
                'average_rate': self._get_average_rate(item),
                'rate_qty': self._get_rate_qty(item),
                'offers_qty': self._get_offers_qty(item),
                'min_price': min_price,
                'max_price': max_price,
            }


    def _get_name(self, item):
        return item.css('span.zg-item a.a-link-normal div::text').get().strip()

    def _get_link(self, item):
        return item.css('span.zg-item a.a-link-normal::attr(href)').get()

    def _get_image_link(self, item):
        return item.css('span.zg-item img::attr(src)').get()

    def _get_thermometer_rank(self, item):
        thermometer_rank_str = item.css('span.zg-badge-text::text').get()
        thermometer_rank_str = thermometer_rank_str.replace('#', '')
        thermometer_rank_str = thermometer_rank_str.replace('.', '')
        return int(thermometer_rank_str)

    def _get_category_ranks(self, item):
        category_ranks = item.css('span.zg-sales-movement::text').get()
        category_ranks = re.sub('[.,]', '', category_ranks)
        category_ranks = re.findall('[0-9]+', category_ranks)
        return list(map(int, category_ranks))

    def _get_rank_percent_change(self, item):
        rank_percent_change = item.css('span.zg-percent-change::text').get()
        rank_percent_change = rank_percent_change.replace('%', '')
        rank_percent_change = rank_percent_change.replace('.', '')
        return int(rank_percent_change)

    def _get_average_rate(self, item):
        container = item.css('span.zg-item')
        average_rate = container.css('.a-icon-star .a-icon-alt::text').get()
        if not average_rate:
            average_rate = container.xpath('./div//div//a') \
                                    .css('::attr(title)').get()
        
        if not average_rate:
            return None

        average_rate = average_rate.replace(',', '.')
        average_rate = average_rate.split()[0]
        return float(average_rate)

    def _get_rate_qty(self, item):
        container = item.css('span.zg-item')
        rate_qty_candidates = container.xpath('./div//a//text()').getall()

        for candidate in rate_qty_candidates:
            try:
                return int(candidate.replace('.', ''))
            except (ValueError, TypeError):
                pass

        return None

    def _get_offers_qty(self, item):
        span_texts = item.css('span::text').getall()
        offers_qty = None
        for text in span_texts:
            if 'oferta' in text:
                text_oferta = re.sub('[,.]', '', text)
                offers_qty = re.findall('[0-9]+', text_oferta)[0]
                return int(offers_qty)

    def _get_prices(self, item):
        prices = item.css('span.p13n-sc-price::text').getall()
        
        if not prices:
            return (None, None)
        
        min_price = re.sub('[R$.]', '', prices[0])
        min_price = float(min_price.replace(',', '.'))
        
        max_price = None
        if len(prices) > 1:
            max_price = re.sub('[R$.]', '', prices[1])
            max_price = float(max_price.replace(',', '.'))
        
        return (min_price, max_price)

