import scrapy
from tutorial.items import TutorialItem

class Spider1(scrapy.Spider):
    # 用于区别Spider。改名字必须是唯一的
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    # 包含了Spider在启动时进行爬取的url列表。因此第一个被获取到的页面将是其中之一。后续的URL则从URL获取
    # 到的数据中提取
    start_urls = [
        "https://scrapy-chs.readthedocs.io/zh_CN/0.24/intro/tutorial.html"
    ]
    '''
    是spider的一个方法。被调用时，每个初始URL完成下载后生成的Response对象将会作为唯一的参数传递
    给该函数。该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理
    的URL对象的Request对象
    '''
    def parse(self, response):
        '''filename = response.url.split("/")[-2]
        with open(filename, "wb") as f:
            f.write(response.body)'''
        for sel in response.xpath('//ul/li'):
            '''title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print(title, link, desc)'''
            item = TutorialItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item
        '''
        <html>
         <head>
          <base href='http://example.com/' />
          <title>Example website</title>
         </head>
         <body>
          <div id='images'>
           <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
           <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
           <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
           <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
           <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
          </div>
         </body>
        </html>
        '''
        # 解析html文件 以上html文件
        response.xpath('//title/text()')
        response.css('title::text')
        # => [<Selector xpath='descendant-or-self::title/text()' data='Example website'>]

        response.xpath('//title/text()').extract()
        response.xpath('title::text').extract()
        # => ['Example website']

        response.xpath('//base/@href').extract()
        response.css('base::attr(href)').extract()
        # => ['http://example.com/']

        response.xpath('//a[contains(@href, "image")]/@href').extract()
        response.css('a[href*=image]::attr(href)').extract()
        # => ['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

        response.xpath('//a[contains(@href, "image")]/img/@src').extract()
        response.css('a[href*=image] img::attr(src)').extract()
        # => ['image1_thumb.jpg',
        #  'image2_thumb.jpg',
        #  'image3_thumb.jpg',
        #  'image4_thumb.jpg',
        #  'image5_thumb.jpg']

        response.xpath('//a[contains(@href,"image")]').extract()
        # => ['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>',
        #  '<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>',
        #  '<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>',
        #  '<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>',
        #  '<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']

        links = response.css('a[href*=image]')
        for index, link in enumerate(links):
            args = (index, link.xpath('@href').extract(), link.xpath('img/@src').extract())

    from scrapy import Selector
    doc = """
         <div>
             <ul>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html">fourth item</a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a></li>
             </ul>
         </div>
         """
    sel = Selector(text=doc, type="html")
    sel.xpath('//li//@href').extract()
    # [u'link1.html', u'link2.html', u'link3.html', u'link4.html', u'link5.html']

    sel.xpath('//li[re:test(@class, "item-\d$")]//@href').extract()
    # [u'link1.html', u'link2.html', u'link4.html', u'link5.html']

    xp = lambda x: sel.xpath(x).extract()
    xp("//li[1]")

    sel = Selector(text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>')
    sel.css('.shout').xpath('./time/@datetime').extract()
    #[u'2014-07-23 19:00']

    '''
    该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request
    当spider启动爬取并且未指定URL时，该方法被调用
    '''
    def start_requests(self):
        return [scrapy.FormRequest("http",
                                   formdata={'user': "ade", 'password': 'ss'},
                                   callback=self.login_in)]
    def login_in(self, response):
        pass
