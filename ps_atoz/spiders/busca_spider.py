import scrapy


class BuscaSpider(scrapy.Spider):
    name = 'busca'
    start_urls = [
        'https://www.amazon.com.br/gp/movers-and-shakers/grocery',
    ]

    def convertInt(self, inteiro):

        """
            Converte numeros em inteiros, ex.: 1.200 em 1200
        """

        if inteiro is None:
            return None

        elif len(inteiro.split('.')) == 2:
            a = inteiro.split('.')
            inteiro = int(a[0] + a[1])
            return inteiro

        elif len(inteiro.split(' ')) > 2:
            a = inteiro.split(' ')[0]
            return int(a)

        else:
            inteiro = int(inteiro)
            return inteiro

    def convertFloat(self, f):
        """
            Converte numeros float, retirando a virgula e colocando um ponto
        """
        if f is None:
            return None

        elif len(f.split(' ')) == 4:
            conv = f.split(' ')[0]
            a = conv.split(',')
            b = a[0] + '.' + a[1]
            return float(b)

        elif len(f.split('-')) == 2:
            a = f.split('-')
            a = a.split('>')
            return float(a)

        else:
            conv = f.lstrip('R$')
            a = conv.split(',')
            b = a[0] + '.' + a[1]
            return float(b)

    def parse(self, response, **kwargs):
        for zg in response.css('li.zg-item-immersion'):
            min_price = zg.css('span.p13n-sc-price::text').get()
            max_price = zg.css('a.a-link-normal.a-text-normal').get()
            if max_price is None:
                print(None)
            else:
                t = max_price.split('<span')
                new_price = t[-1].rstrip('</span></span></a>').split('class="p13n-sc-price">')
                max_price = new_price[-1]
                if max_price == min_price:
                    max_price = None

            yield {
                'name': zg.xpath('span/div/span/a/div/text()').get().strip(),
                'link': zg.css('span.aok-inline-block.zg-item a::attr(href)').get(),
                'image_link': zg.css('img::attr(src)').get(),
                'thermometer_rank': int(zg.xpath('span/div/div/span/span/text()').get().split('#')[1]),
                'recent_category_rank': int(zg.css('span.zg-sales-movement::text').get().split(' ')[3]),
                'past_category_rank': self.convertInt(zg.css('span.zg-sales-movement::text').get().split(' ')[5].rstrip(')')),
                'rank_percent_change': self.convertInt(zg.css('span.zg-percent-change::text').get().split('%')[0]),
                'average_rate': self.convertFloat(zg.css('span.a-icon-alt::text').get()),
                'rate_qty': self.convertInt(zg.css('a.a-size-small.a-link-normal::text').get()),
                'offers_qty': self.convertInt(zg.css('span.a-color-secondary::text').get()),
                'min_price': self.convertFloat(min_price),
                'max_price': self.convertFloat(max_price)
            }


