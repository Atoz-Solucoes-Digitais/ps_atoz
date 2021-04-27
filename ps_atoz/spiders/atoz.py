import scrapy


class QuotesSpider(scrapy.Spider):
    name = "atoz"
    start_urls = [
        'https://www.amazon.com.br/gp/movers-and-shakers/grocery/',
    ]

    def parse(self, response):
        for i in response.xpath('//li[@class="zg-item-immersion"]'):

            #Definição do nome:
            # Identificadores não representativos nas variaveis
            n = i.xpath('.//div/text()').get()
            n=n.split('\n')
            n=n[1].strip()
            name = n
            
            # Faltou uma maior separação de responsabilidade no código. Todo o processamento
            # incluindo raspagem, limpeza e casting dos dados foi feito junto, tornando o debug complicado

            #Definição do link:
            link = 'amazon.com.br' + i.xpath('.//a/@href').get()

            #Definição do link de imagem:
            image_link = i.xpath('.//img/@src').get()

            #Definição do link do thermometer_rank:
            
            thermometer_rank = i.xpath('.//span[@class="zg-badge-text"]//text()').get()
            thermometer_rank = int(thermometer_rank.split("#")[1])

            #Definição do recent_category_rank e past_category_rank:

            category_rank = i.xpath('.//span[@class="zg-sales-movement"]//text()').get()
            recent_category_rank = category_rank.split(': ')[1]
            recent_category_rank = int(recent_category_rank.split(' ')[0])

            past_category_rank = category_rank.split(': ')[2]
            past_category_rank = int(past_category_rank.split(')')[0].replace('.',''))

            # #Definição do rank_percent_change:

            rank_percent_change = i.xpath('.//span[@class="zg-percent-change"]//text()').get()
            rank_percent_change = int(rank_percent_change.replace('%', '').replace('.', ''))

            # Bom tratamento de erros preenchendo None como fallback
            #Definição do average_rate:
            try:
                average_rate = i.xpath('.//span[@class="a-icon-alt"]//text()').get()
                average_rate = float(average_rate.split(' ')[0].replace(',', '.'))

            except:
                average_rate = None

            # #Definição do rate_qty:

            try:
                rate_qty = int(i.xpath('.//a[@class="a-size-small a-link-normal"]//text()').get())
            except:
                rate_qty = None


            # #Definição do offers_qty:

            try:
                offers_qty = i.xpath('.//span[@class="a-color-secondary"]//text()').get()
                offers_qty = int(offers_qty.split(' ')[0])
            except:
                offers_qty = None


            # #Definição do min_price e max_price:

            try:
                price = i.xpath('.//span[@class="p13n-sc-price"]//text()').getall()
                # Legal ter utilizado list comprehension aqui.
                # Não funcionará caso encontre algum preço acima de R$999,99 já que
                # Terá '.' com separador de milhar (RS1.000,00) como rate_qty
                # Muita lógica agrupada
                price = [(p.replace('R$', '').replace(',', '.')) for p in price]

                min_price = float(price[0])

                try:
                    max_price = float(price[1])
                except:
                    max_price = None

            except:
                min_price = None
                max_price = None



            yield {
                'name': name,
                'link': link,
                'image_link': image_link,
                'thermometer_rank': thermometer_rank,
                'recent_category_rank': recent_category_rank,
                'past_category_rank': past_category_rank,
                'rank_percent_change': rank_percent_change,
                'average_rate': average_rate,
                'rate_qty': rate_qty,
                'offers_qty': offers_qty,
                'min_price': min_price,
                'max_price': max_price
            }
