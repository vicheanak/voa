# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from voa.items import VoaItem
from scrapy.linkextractors import LinkExtractor
import time


class TestSpider(CrawlSpider):
    name = "voa"
    allowed_domains = ["khmer.voanews.com"]
    start_urls = [
    'http://khmer.voanews.com/z/2278.html',
    ]

    def parse(self, response):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        hxs = scrapy.Selector(response)
        item = VoaItem()
        highlight = hxs.xpath('//div[@class="media-block horizontal with-date width-img size-2"]')
        item['categoryId'] = '1'

        name = highlight.xpath('div[@class="content"]/a[1]/h4[1]/span[1]/text()')
        if not name:
            print('VOA => [' + now + '] No title')
        else:
            item['name'] = name.extract_first()

        url = highlight.xpath('div[@class="content"]/a[1]/@href')
        if not url:
            print('VOA => [' + now + '] No url')
        else:
            item['url'] = 'http://khmer.voanews.com/' + url.extract_first()

        description = highlight.xpath('div[@class="content"]/a[1]/p[1]/text()')
        if not description:
            print('VOA => [' + now + '] No description')
        else:
            item['description'] = description.extract_first()

        imageUrl = highlight.xpath('a[1]/div[1]/img[1]/@src')
        item['imageUrl'] = ''
        if not imageUrl:
            print('VOA => [' + now + '] No imageUrl')
        else:
            imageUrl = imageUrl.extract_first()
            imageUrl = imageUrl.split('_', 1)
            imageUrl = imageUrl[0] + '_w987_r1_s.jpg'
            item['imageUrl'] = imageUrl


        yield item

        followups = hxs.xpath('//ul[@id="ordinaryItems"]/li')


        for followup in followups:
            item = VoaItem()
            item['categoryId'] = '1'



            name = followup.xpath('div[1]/div[@class="content"]/a[1]/h4[1]/span[1]/text()')
            if not name:
                print('VOA => [' + now + '] No title')
            else:
                item['name'] = name.extract_first()

            url = followup.xpath('div[1]/div[@class="content"]/a[1]/@href')

            if not url:
                print('VOA => [' + now + '] No url')
            else:
                item['url'] = 'http://khmer.voanews.com/' + url.extract_first()

            description = followup.xpath('div[1]/div[@class="content"]/a[1]/p[1]/text()')
            if not description:
                print('VOA => [' + now + '] No description')
            else:
                item['description'] = description.extract_first()

            imageUrl = followup.xpath('div[1]/a[1]/div[1]/img[1]/@src')
            if not imageUrl:
                print('VOA => [' + now + '] No imageUrl')
            else:
                imageUrl = imageUrl.extract_first()
                imageUrl = imageUrl.split('_', 1)
                imageUrl = imageUrl[0] + '_w987_r1_s.jpg'
                item['imageUrl'] = imageUrl

            yield item



    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        item_page = hxs.css('div.item-page')
        description = item_page.xpath('p[1]/text()')
        if not description:
            print('ThmeyThmey => [' + now + '] No description')
        else:
            item['description'] = item_page.xpath('p[1]/strong/text()').extract_first() + ' ' + description.extract_first()

        imageUrl = item_page.xpath('p[last()]/img/@src')
        if not imageUrl:
            print('ThmeyThmey => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()


        yield item
