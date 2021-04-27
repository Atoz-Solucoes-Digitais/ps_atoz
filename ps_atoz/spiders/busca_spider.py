import scrapy


class BuscaSpider(scrapy.Spider):
    name = 'busca'
    start_urls = [
        'https://www.amazon.com.br/gp/movers-and-shakers/grocery',
    ]

    # Não é boa prática criar funções dentro da classe que não tenham relação
    # com a funcionalidade da classe. Essas duas funções poderiam ficar em um módulo
    # diferente, ou fora do escopo da classe.
    def convertInt(self, inteiro):
        # Muito bom usar comentarios docstring
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

    # Essa função esta em desacordo com o principio de que uma função deve apenas realizar uma tarefa.
    # Ela não converte apenas uma string para float, ela também limpa a string de "R$", por exemplo.
    # Além disso, a lógica usando "split" é complexa de ler e complicada de dar manutenção.
    # Poderia ter sido usada a função "replace"
    # Além disso, a lógica de conversão quebra se o preço tiver separador de milhar e.g. R$1.564,12
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
            
            # O nome "max_price" para essa variável pode causar confusão, pois elementos com a classe
            # apontada existem mesmo que nao haja um preço máximo no produto
            max_price = zg.css('a.a-link-normal.a-text-normal').get()
            
            if max_price is None:
                #Não é necessário imprimir None, poderia ter sido usado uma negação no condicional
                # if max_price is not None para executar apenas quando o max price não fosse None
                print(None)
            else:
                # Lógica muito complexa para identiicar se existe um preço máximo, o objetivo de usar scrapy é justamente
                # não ficar dividindo strings a partir de tags HTML. Poderia ter procurado por elementos span com a classe
                # p13n-sc-price e se houvessem 2, significa que há max_price
                t = max_price.split('<span')
                new_price = t[-1].rstrip('</span></span></a>').split('class="p13n-sc-price">')
                max_price = new_price[-1]
                if max_price == min_price:
                    max_price = None

            # É compreensível a intenção de condensar a lógica em uma linha, mas isso cria um código mais complexo do que o necessário 
            # para ser lido por outras pessoas.
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


