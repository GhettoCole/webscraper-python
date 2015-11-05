#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import build_opener
from urllib.error import HTTPError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re


class WebScraper:
    def __init__(self):
        self.opener = build_opener()
        # Like a human
        self.opener.addheaders = [
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"),
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        ]

    def getAnchors(self, compliledRegExp):
        return self.bsObj.findAll("a", {"href": compliledRegExp})

    def crawl(self, url):
        html = self.opener.open(url)
        self.rawHtml = html.read()
        self.bsObj = BeautifulSoup(self.rawHtml, "html.parser")

    def countLinks(self, url, regExp):
        self.crawl(url)
        anchors = self.getAnchors(regExp)
        print("%s\t%s" % (url, len(anchors)))

if __name__ == "__main__":
    baseUrl = "http://example.com"
    for i in ["11435", "23456", "143456"]:
        #url = urljoin(baseurl, "11435")
        #url = urljoin(baseUrl, "12957")
        url = urljoin(baseUrl, i)
        targetRegExp = re.compile("^https?:\/\/example\.com")
        pagerRegExp = re.compile("^/\d+\?page=")

        try:
            ws = WebScraper()
            ws.countLinks(url, targetRegExp)
            pagers = ws.getAnchors(pagerRegExp)
            for pager in pagers:
                nextUrl = urljoin(baseUrl, pager["href"])
                ws.countLinks(nextUrl, targetRegExp)
        except HTTPError as e:
            print("%s\t%s" % (url, e))
