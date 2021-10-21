# -*- coding: utf-8 -*-

import urllib
import urllib.robotparser
import re
import random
import time
from datetime import datetime, timedelta
import socket


DEFAULT_AGENT = 'thu_igemer_2021'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 2
DEFAULT_TIMEOUT = 60
DEFAULT_URL = "http://www.kazusa.or.jp/codon/cgi-bin/spsearch.cgi?species="

class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache
        self.headers = {'User-agent': self.user_agent}

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError: 
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                self.cache[url] = result
        return result['html']


    def download(self, url, headers, proxy, num_retries, data=None):
        #print ('Downloading:', url)
        request = urllib.request.Request(url, data, headers)
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print ('Download error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    return self._get(url, headers, proxy, num_retries-1, data)
            else:
                code = None
        return {'html': html, 'code': code}
    
    def get_links(self, html):
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
        return webpage_regex.findall(html.decode('utf-8'))
    def get_species(self, html):
        webpage_regex = re.compile('<I>(.*)</I>',re.IGNORECASE)
        return webpage_regex.findall(html.decode('utf-8'))

class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}
        
    def wait(self, url):
        domain = urllib.parse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()

class Search:
    def __init__(self, search_name, seed_url=DEFAULT_URL, html=None):
        self.rp = urllib.robotparser.RobotFileParser()
        self.rp.set_url('http://www.kazusa.or.jp/robots.txt')
        self.rp.read()
        self.html = html
        self.seed_url = seed_url
        self.search_name = search_name
        
    def link_getter(self):
        url = self.seed_url + self.search_name.replace(' ','+') + '&c=s'
        seen = list()
        D = Downloader()
        if self.rp.can_fetch(D.user_agent,url):
            html = D.download(url,D.headers,D.proxies,D.num_retries)['html']
            for link in D.get_links(html):
                link = urllib.parse.urljoin(self.seed_url,link)
                if link not in seen:
                    seen.append(link)
        else:
            print('Blocked by robots.txt',url)
        return seen

    def species_getter(self):
        url = self.seed_url + self.search_name.replace(' ','+') + '&c=s'
        seen = list()
        D = Downloader()
        if self.rp.can_fetch(D.user_agent,url):
            html = D.download(url,D.headers,D.proxies,D.num_retries)['html']
            for species in D.get_species(html):
                if species not in seen:
                    seen.append(species)
        else:
            print('Blocked by robots.txt',url)
        return seen

#S = Search('Esccccc')
#print(S.species_getter())
