import scrapy
from ..items import PsAtozItem

class GrocerySpider(scrapy.Spider):
    name = 'grocery'
    start_urls = ['https://www.amazon.com.br/gp/movers-and-shakers/grocery/']

    def parse(self, response):
        # Raspagem, validação, limpeza e conversão de tipos concentrada em apenas uma função.
        # Isso dificulta manutenção. Poderia ter separado em funções privadas da spider.
        
        # Bacana o uso do Scrapy Item
        items = PsAtozItem()

        containers = response.css(".zg-item-immersion")

        for container in containers :
            name = container.css('.a-spacing-small img').xpath("@alt").extract_first()
            link = container.xpath(".//span[@class='aok-inline-block zg-item']").xpath(".//a[@class='a-link-normal']").xpath("@href").extract_first()
            image_link = container.css('.a-spacing-small img').xpath("@src").extract_first()

            # Tipo errado, voltando string ao invés de integer e nao removeu o "#"
            thermometer_rank = container.css(".zg-badge-text::text").extract_first()

            #parsing sales_movement text
            sales_movement = container.css(".zg-sales-movement::text").extract_first()
            split_text = sales_movement.split(':')
            recent_category_rank = int(split_text[1].split('(')[0])
            past_category_rank = int(split_text[2].replace('.', '').replace(' ', '')[:-1])

            #transforming percentage to int
            perc = container.css(".zg-percent-change::text").extract_first()
            perc = perc[:-1].replace('.', '')
            rank_percent_change = int(perc)

            #parsing stars avarage
            star_text = container.xpath(".//i[@class='a-icon a-icon-star a-star-5 aok-align-top']").css("span::text").extract_first()
            average_rate = None if star_text == None else float(star_text.split(' ')[0].replace(',','.'))

            #converting to int
            ratings_qty = container.xpath(".//a[@class='a-size-small a-link-normal']/text()").extract_first()
            rate_qty = None if ratings_qty == None else int(ratings_qty.replace('.', ''))

            #offers qty
            oq = container.xpath(".//span[@class='a-color-secondary']/text()").extract_first()
            offers_qty = None if oq == None else int(oq.split(' ')[0])

            #parsing price
            min_price = None
            max_price = None
            # Ao utilizar extract_first, apenas o primeiro elemento é extraído, ou seja,
            # nunca conseguirá extrair o preço máximo
            prices = container.css(".p13n-sc-price::text").extract_first()
            if(prices != None) :
                # Lógica de limpeza não contempla preços que tenham separador de milhar
                # e.g. "R$1.189,99"
                prices = prices.replace('R$', '')
                prices = prices.replace(',', '.')
                split_price = prices.split(' - ')
                min_price = None if len(split_price) == 0 else float(split_price[0])
                max_price = None if len(split_price) <= 1 else float(split_price[1])
            
            items['name'] = name
            items['link'] = link
            items['image_link'] = image_link
            items['thermometer_rank'] = thermometer_rank
            items['recent_category_rank'] = recent_category_rank
            items['past_category_rank'] = past_category_rank
            items['rank_percent_change'] = rank_percent_change
            items['average_rate'] = average_rate
            items['rate_qty'] = rate_qty
            items['offers_qty'] = offers_qty
            items['min_price'] = min_price
            items['max_price'] = max_price

            yield items
        


        
        

