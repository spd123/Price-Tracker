from UserAgents import Get_Headers
import scrapy
import pymongo
import datetime
from scrapy.crawler import CrawlerProcess
from cleanPriceData import Clean_price

client = pymongo.MongoClient("mongodb://localhost:27017/")
DB     = client["Amazon"]
collection = DB["Books"]

class WebScrapper(scrapy.Spider):
    name = "AmazonWebSpider"
    headers = {'User-Agent' : Get_Headers()}
    Secondary_pages = 1
    def start_requests(self):
        urls = [ 'https://www.amazon.in/Books/b?ie=UTF8&node=976389031&ref_=sd_allcat_sbc_books_all' ]
        for url in urls:
            yield scrapy.Request(url=url, callback= self.Pages, headers= self.headers)

    def Pages(self, response):
        Categories = response.xpath('.//div[@id="leftNav"]//span/a/@href').extract()
        non_cat = 'https://www.amazon.in/gp/search/other/ref=lp_976389031'
        for category in Categories:
            link = response.urljoin(category)
            if link in links or non_cat in link:
                pass
            else:
                links.add(link)
                try:
                    yield scrapy.Request(url=link, callback= self.get_Details_of_Primary_Page, headers= self.headers)
                except:
                    pass

    def Product_details_on_first_page(self,asin,response):
        base_query = './/li[@data-asin=' + f'"{str(asin)}"' + ']'
        Product_title = response.xpath(
            base_query + '//h2[@class = "a-size-medium s-inline s-access-title a-text-normal"]/text()').extract()

        Product_link = response.xpath(
            base_query + '//a[@class="a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"]/@href').extract()

        Paperback = response.xpath(
            base_query + '//div[@class="a-column a-span7"]//div/a[@title = "Paperback"]/../following-sibling::div[1]'
                         '//span[@class="a-size-base a-color-price s-price a-text-bold" or @class="a-size-base a-color-price a-text-bold"]/text()').extract() or None

        Kindle_Edition = response.xpath(
            base_query + '//div[@class="a-column a-span7"]//div/a[@title = "Kindle Edition"]/../following-sibling::div[1]'
                         '//span[@class="a-size-base a-color-price s-price a-text-bold" or @class="a-size-base a-color-price a-text-bold"]/text()').extract() or None

        Hardcover = response.xpath(
            base_query + '//div[@class="a-column a-span7"]//div/a[@title = "Hardcover"]/../following-sibling::div[1]'
                         '//span[@class="a-size-base a-color-price s-price a-text-bold" or @class="a-size-base a-color-price a-text-bold"]/text()').extract() or None

        if Paperback is not None:
            Paperback = Clean_price(Paperback[0])
        if Kindle_Edition is not None:
            Kindle_Edition = Clean_price(Kindle_Edition[0])
        if Hardcover is not None:
            Hardcover = Clean_price(Hardcover[0])
        for obj in collection.find({'ASIN': str(asin)}):
            if Paperback != obj['Paperback'][-1]['price']:
                collection.update({"ASIN": str(asin)},{'$push': {'Paperback': {'price': Paperback, 'time': datetime.datetime.utcnow()}}})
            if Kindle_Edition != obj['Kindle_Edition'][-1]['price']:
                collection.update({"ASIN": str(asin)},{'$push': {'Kindle_Edition': {'price': Kindle_Edition, 'time': datetime.datetime.utcnow()}}})
            if Hardcover != obj['Hardcover'][-1]['price']:
                collection.update({"ASIN": str(asin)},{'$push': {'Hardcover': {'price': Hardcover, 'time': datetime.datetime.utcnow()}}})


    def Product_details_on_next_page(self,asin_next,response):
        base_query_next = './/div[@data-asin=' + f'"{str(asin_next)}"' + ']'
        link_next = response.xpath(
            base_query_next + '//h2[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-2"]/a/@href').extract()
        Product_link_next = response.urljoin(link_next[0])
        Product_title_next = response.xpath(
            base_query_next + '//span[@class="a-size-medium a-color-base a-text-normal"]/text()').extract()

        Paperback_next = response.xpath(
            base_query_next + '//div[@class="a-row a-size-base a-color-base"]/a[contains(text(),"Paperback")]'
                              '/../following-sibling::div[1]//span[@class="a-price-whole" or @class="a-color-price"]/text()').extract() or None

        Kindle_Edition_next = response.xpath(
            base_query_next + '//div[@class="a-row a-size-base a-color-base"]/a[contains(text(),"Kindle Edition")]'
                              '/../following-sibling::div[1]//span[@class="a-price-whole" or @class="a-color-price"]/text()').extract() or None

        Hardcover_next = response.xpath(
            base_query_next + '//div[@class="a-row a-size-base a-color-base"]/a[contains(text(),"Hardcover")]'
                              '/../following-sibling::div[1]//span[@class="a-price-whole" or @class="a-color-price"]/text()').extract() or None
        if Paperback_next is not None:
            Paperback_next = Clean_price(Paperback_next[0])
        if Kindle_Edition_next is not None:
            Kindle_Edition_next = Clean_price(Kindle_Edition_next[0])
        if Hardcover_next is not None:
            Hardcover_next = Clean_price(Hardcover_next[0])

        for obj in collection.find({"ASIN": str(asin_next)}):
            if Paperback_next != obj['Paperback'][-1]['price']:
                collection.update({"ASIN": str(asin_next)},{'$push': {'Paperback': {'price': Paperback_next, 'time': datetime.datetime.utcnow()}}})
            if Kindle_Edition_next != obj['Kindle_Edition'][-1]['price']:
                collection.update({"ASIN": str(asin_next)},{'$push': {'Kindle_Edition': {'price': Kindle_Edition_next, 'time': datetime.datetime.utcnow()}}})
            if Hardcover_next != obj['Hardcover'][-1]['price']:
                collection.update({"ASIN": str(asin_next)},{'$push': {'Hardcover': {'price': Hardcover_next, 'time': datetime.datetime.utcnow()}}})

    def get_Details_of_Primary_Page(self,response):
        try:
            ASIN = response.xpath('.//li[@class = "s-result-item celwidget  "]/@data-asin').extract()
            for asin in ASIN:
                if asin in asins:
                    pass
                else:
                    self.Product_details_on_first_page(asin,response)
                    asins.add(asin)
            next_page = response.xpath('.//div[@class="pagnHy"]/span[@class="pagnRA"]/a/@href').extract()
            yield scrapy.Request(url = response.urljoin(next_page[0]) , callback= self.get_Details_of_Primary_Page, headers= self.headers)
        except:
            ASIN_next = response.xpath('.//div[@class="sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"]/@data-asin').extract()
            for asin_next in ASIN_next:
                if asin_next in asins:
                    pass
                else:
                    self.Product_details_on_next_page(asin_next,response)
                    asins.add(asin_next)
                asins.add(asin_next)
            self.Secondary_pages += 1
            try:
                next_page_link = response.xpath('.//li[@class="a-last"]/a/@href').extract()
                yield scrapy.Request(url = response.urljoin(next_page_link[0]), callback= self.get_Details_of_Primary_Page, headers= self.headers)
            except:
                self.Secondary_pages = 1



links = set()
asins = set()
process = CrawlerProcess()
process.crawl(WebScrapper)
process.start()