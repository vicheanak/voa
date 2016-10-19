# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from voa.items import VoaItem
from scrapy.linkextractors import LinkExtractor
import time
import lxml.etree
import lxml.html


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

        request = scrapy.Request(item['url'], callback=self.parse_detail)
        request.meta['item'] = item
        yield request

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


            request = scrapy.Request(item['url'], callback=self.parse_detail)
            request.meta['item'] = item
            yield request



    def parse_detail(self, response):
        item = response.meta['item']
        hxs = scrapy.Selector(response)
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        htmlcontent = ''
        for p in root.xpath('//div[@class="wysiwyg"][1]'):
            htmlcontent = lxml.html.tostring(p, encoding=unicode)

        item['htmlcontent'] = htmlcontent

        if not item['htmlcontent']:
            for pa in root.xpath('//div[@class="intro content-offset"][1]'):
                htmlcontent = lxml.html.tostring(pa, encoding=unicode)
                item['htmlcontent'] = htmlcontent

        imageUrl = hxs.xpath('//div[@class="thumb listThumb"]/img[1]/@src')
        item['imageUrl'] = ''
        if not imageUrl:
            print('VOA => [' + now + '] No imageUrl')
        else:
            item['imageUrl'] = imageUrl.extract_first()
            for m in root.xpath('//div[@class="thumb listThumb"]/img[1]'):
                img = lxml.html.tostring(m, encoding=unicode)
                item['htmlcontent'] = img + item['htmlcontent']


        yield item
