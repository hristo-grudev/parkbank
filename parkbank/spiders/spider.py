import scrapy

from scrapy.loader import ItemLoader

from ..items import ParkbankItem
from itemloaders.processors import TakeFirst


class ParkbankSpider(scrapy.Spider):
	name = 'parkbank'
	start_urls = ['https://www.parkbank.com/blog/category/parkbanknews']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "button-primary", " " ))]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//em//*[contains(concat( " ", @class, " " ), concat( " ", "page", " " ))]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//*[(@id = "js-post-title")]/text()').get()
		description = response.xpath('//div[@class="text-content clearfix"]//text()[normalize-space() and not(ancestor::div[class="social-share"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "date", " " ))]/text()').get()

		item = ItemLoader(item=ParkbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
