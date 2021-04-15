# Projeto para vaga de Desenvolvedor Python Jr.
***

## Instalação (Linux)
1. Clonar este repositório e entrar na pasta
2. Criar ambiente virtual
```
python3 -m venv .venv
```
3. Ativar ambiente virtual
```
source .venv/bin/activate 
```
4. Instalar dependências
```
python3 -m pip install requirements.txt
```
## Introdução
Uma das principais responsabilidades no dia-a-dia de um desenvolvedor na Atoz será o desenvolvimento e manutenção de *crawlers* para páginas da Amazon. Para isso utilizamos o framework *[Scrapy](https://docs.scrapy.org/en/latest/intro/overview.html)* já que ele oferece diversas facilidades para essa tarefa como *[middlewares](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html)*, *[pipelines](https://docs.scrapy.org/en/latest/topics/item-pipeline.html)* e *[seletores](https://docs.scrapy.org/en/latest/topics/selectors.html)*. Um breve tutorial da ferramenta pode ser encontrado [aqui](https://docs.scrapy.org/en/latest/intro/tutorial.html).

Esse repositório já contém um projeto inicial do Scrapy. Faça um *fork*, desenvolva o que é pedido e depois faça um *pull request*.

## Descrição
A Amazon tem uma [página](https://www.amazon.com.br/gp/movers-and-shakers) que é atualizada de hora em hora onde são mostrados os produtos que mais subiram de ranking. Esses resultados são separados em categorias, como por exemplo [Alimentos e Bebidas](https://www.amazon.com.br/gp/movers-and-shakers/grocery). Alguns exemplos de como um item pode aparecer no ranking: 

![Exemplo de item 1](https://i.imgur.com/E4EmoNY.png)![Exemplo de item 2](https://i.imgur.com/ws5tn55.png)
![Exemplo de item 3](https://i.imgur.com/oMxLF92.png)

O desafio consiste em extrair (utilizando os seletores *css* e *xpath* do Scrapy) os seguintes dados de cada item de uma página do ranking:
 - Nome (e.g. "Cápsulas de Café Lungo Estremo L'Or 10 Cápsulas")
 - Link do produto (obtido no *href* do nome)
 - Link da imagem (obtido no *src* da imagem)
 - Rank no termometro (e.g. 1, 15 e 95)
 - Porcentagem de mudança do rank (e.g. 3081, 344 e 66)
 - Rank atual na categoria (e.g. 11)
 - Rank anterior na categoria (não é possível enxergar na imagem, mas está no elemento HTML)
 - Média de avaliação (o número exato que aparece ao colocar o cursor sobre as estrelas)
 - Quantidade de avaliações (e.g. 59, 290, 927)
 - Quantidade de ofertas (e.g. na imagem 3 é 8)
 - Preço mínimo (e.g. 5,79 ou 143,76 ou 22,9 ou None quando não existir)
 - Preço máximo (e.g. 267,67 na imagem 2)

Para isso deve-se criar uma *spider* que recebe uma *start_url* de uma das categorias [Alimentos e Bebidas](https://www.amazon.com.br/gp/movers-and-shakers/grocery), extrai os items da primeira página do ranking gravando-os em um arquivo JSON (ver [Storing the scraped data](https://docs.scrapy.org/en/latest/intro/tutorial.html#storing-the-scraped-data)). Cada item do arquivo json deve ter o formato abaixo:

```json
{
    'name': string,
    'link': string,
    'image_link': string,
    'thermometer_rank': integer,
    'recent_category_rank': integer,
    'past_category_rank': integer,
    'rank_percent_change': integer,
    'average_rate': Optional[float],
    'rate_qty': Optional[integer],
    'offers_qty': Optional[integer],
    'min_price': Optional[float],
    'max_price': Optional[float]
}
```
Os campos marcados com *Optional* podem ter *None* como valor, os outros devem ter um valor para todos os itens.

A documentação do Scrapy é rica e muito bem escrita, recomendo fortemente a leitura. Caso surjam dúvidas, pode me chamar no Whatsapp no número que fornecerei.
