import scrapy
from mydata.items import MovieItem


class SecondSpider(scrapy.Spider):
    name = "sorna"
    allowed_domains = ["imdb.com"]
    start_urls = ("https://www.imdb.com/chart/top",)

    def parse(self, response):
        links = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href').extract()
        i = 1
        for link in links:
            abs_url = response.urljoin(link)
            url_next = '//* [@id="main"]/div/span/div/div/div[2]/table/tbody/tr[' + str(i) + ']/td[3]/strong/text()'
            rating = response.xpath(url_next).extract()
            if i <= len(links):
                i = i + 1
                yield scrapy.Request(abs_url, callback=self.parse_details, meta={'rating': rating})

    def parse_details(self, response):
        item = MovieItem()
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0][:-1]
        item['directors'] =response.xpath(
            '//div[@class="credit_summary_item"]/span[@itemprop="director"]/a/span/text()').extract()[0]
        item['writers'] = response.xpath(
            '//div[@class="credit_summary_item"]/span[@itemprop="creator"]/a/span/text()').extract()
        item['stars'] = response.xpath(
            '//div[@class="credit_summary_item"]/span[@itemprop="actors"]/a/span/text()').extract()
        item['popularity'] = response.xpath('//div[@class="titileReviewBarSubItem"]/div/span/text()').extract()[2][
                             21:-8]

        print(item)
