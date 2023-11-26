from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from scrapy.utils.sitemap import Sitemap, sitemap_urls_from_robots
import requests

class EpicuriousSpider(SitemapSpider):
    name = "epicurious"
    handle_httpstatus_list = [404]
    custom_settings = {
        "FEED_FORMAT" : "csv",
        "FEED_URI" : "test.csv"
    }

    def parse(self, response):
        print("########### This is response.url ################")
        print (response.url)

    def _parse_sitemap(self, response):
        if response.url.endswith('/robots.txt'):
            for url in sitemap_urls_from_robots(response.body):
                Request(url, callback=self._parse_sitemap)
        else:
            body = self._get_sitemap_body(response)
            if body is None:
                self.logger.info('Ignoring invalid sitemap: %s', response.url)
                return

            s = Sitemap(body)
            sites = []
            if s.type == 'sitemapindex':
                for loc in iterloc(s, self.sitemap_alternate_links):
                    if any(x.search(loc) for x in self._follow):
                        yield Request(loc, callback=self._parse_sitemap)
            elif s.type == 'urlset':
                for loc in iterloc(s):
                    for r, c in self._cbs:
                        if r.search(loc):
                            sites.append(loc)
                            for site in sites:
                                print(site)
                                yield{"url" : site}
                            break


    def __init__(self, spider=None, *a, **kw):
            super(EpicuriousSpider, self).__init__(*a, **kw)
            self.spider = spider
            l = []
            url = "https://www.epicurious.com"
            resp = requests.head(url + "/sitemap.xml/editorial-recipes")
            if (resp.status_code != 404):
                l.append(resp.url)
            else:
                resp = requests.head(url + "/robots.txt")
                if (resp.status_code == 200):
                    l.append(resp.url)
            self.sitemap_urls = l
            # print("########### This is sitemap_urls ################")
            # print (self.sitemap_urls)

def iterloc(it, alt=False):
    for d in it:
        yield d['loc']

        # Also consider alternate URLs (xhtml:link rel="alternate")
        if alt and 'alternate' in d:
            for l in d['alternate']:
                yield l
