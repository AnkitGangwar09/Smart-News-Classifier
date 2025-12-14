import scrapy
from urllib.parse import urljoin

class newspider(scrapy.Spider):
    name = "newser"
    start_urls = ['https://www.hindustantimes.com/lifestyle',
                  'https://www.hindustantimes.com/business',
                  ]

    def parse(self,response):
        for article in response.css('div.cartHolder'):
            link = article.css('a').attrib['href']

            yield response.follow(link, callback = self.parse_article)



        
        next = response.css('div.listPagination')
        next_page = next.css('a').attrib['href']

        if "https://www.hindustantimes.com" in next_page:
            yield response.follow(next_page, callback = self.parse)
        else:
            next_page_url = urljoin('https://www.hindustantimes.com', next_page)
            yield response.follow(next_page_url, callback = self.parse)             
        

    def parse_article(self, response):

        category = response.url.split("/")[3]

        news = response.css('div.detail')
        if "sports" in response.url:
            content = news.css('p::text').getall()
        else:
            news = response.xpath("//p//text()").getall()
            content = " ".join(news).strip()

        news_title = response.css('div.fullStory')
        title = news_title.css('h1::text').get()

        yield{
            'Title' : title,
            'Content' : content,
            'Category' : category,
        }

