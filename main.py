import scrapy

class QuotesSpider(scrapy.Spider):
    name = "products"

    start_urls = ["https://www.amazon.com.br/gp/movers-and-shakers/grocery"]

    def parse(Self, response):
        base_url = "https://www.amazon.com.br{}"
        cont_li = 1
        products = response.xpath('//*[@id="zg-ordered-list"]/li')
        for product in products:
            name = product.xpath(f'//li[{cont_li}]/span/div/span/a/div/text()').get().strip()
            path_to_product = product.xpath(f'//li[{cont_li}]/span/div/span/a').attrib['href']
            link = base_url.format(path_to_product)
            image_link = product.xpath(f'//li[{cont_li}]/span/div/span/a/span/div/img').attrib['src']
            thermometer_rank = product.xpath(f'//li[{cont_li}]/span/div/div/span[1]/span/text()').get()
            rank_percent_change = product.xpath(f'//li[{cont_li}]/span/div/div/span[3]/span[2]/text()').get()
            recent_category_rank = product.xpath(f'//li[{cont_li}]/span/div/div/span[3]/span[3]/text()').get()
            past_category_rank = product.xpath(f'//li[{cont_li}]/span/div/div/span[3]/span[3]/text()').get()
            average_rate = product.xpath(f'//li[{cont_li}]/span/div/span/div[1]/a[1]/i/span/text()').get()
            rate_qty = product.xpath(f'//li[{cont_li}]/span/div/span/div[1]/a[2]/text()').get()
            offers_qty = product.xpath(f'//li[{cont_li}]/span/div/span/a[2]/span/text()').get()
            min_price = product.xpath(f'//li[{cont_li}]/span/div/span/div[2]/a/span/span/text()').get()
            max_price = product.xpath(f'//li[{cont_li}]/span/div/span/div[2]/a/span/span[2]/text()').get()

            yield {
                'name': name,
                'link': link,
                'image_link': image_link,
                'thermometer_rank': normalize_thermometer_rank(thermometer_rank),
                'recent_category_rank': normalize_recent_category_rank(recent_category_rank),
                'past_category_rank': normalize_past_category_rank(past_category_rank),
                'rank_percent_change': normalize_rank_percent_change(rank_percent_change),
                'average_rate': normalize_average_rate(average_rate),
                'rate_qty': normalize_rate_qty(rate_qty),
                'offers_qty': normalize_offers_qty(offers_qty),
                'min_price': normalize_min_price(min_price),
                'max_price': normalize_max_price(max_price)
            }
            cont_li+=1

def normalize_rate_qty(rate_qty):
    if rate_qty == None:
        return None
    return int(rate_qty.replace(".", ""))

def normalize_thermometer_rank(thermometer_rank):
    if thermometer_rank == None:
        return None
    return int(thermometer_rank.replace("#", ""))

def normalize_recent_category_rank(recent_category_rank):
    if recent_category_rank == None:
        return None
    value = recent_category_rank.split(":")[1]
    return int(value.split("(")[0].strip())

def normalize_past_category_rank(past_category_rank):
    if past_category_rank == None:
        return None
    value = past_category_rank.split(":")[-1]
    return int(value.strip().replace(")", "").replace(".", ""))

def normalize_rank_percent_change(rank_percent_change):
    if rank_percent_change == None:
        return None
    return int(rank_percent_change.replace("%", "").replace(".", ""))

def normalize_average_rate(average_rate):
    if average_rate == None:
        return None
    return float(average_rate.split(" ")[0].replace(",", "."))

def normalize_offers_qty(offers_qty):
    if offers_qty == None:
        return None
    return int(offers_qty.split(" ")[0].replace(".", ""))

def normalize_min_price(min_price):
    if min_price == None:
        return None
    return float(min_price.replace("R$", "").replace(",", "."))

def normalize_max_price(max_price):
    if max_price == None:
        return None
    return float(max_price.replace("R$", "").replace(",", "."))