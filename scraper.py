#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import build_opener
import os
import re
import sys
import time
import yaml


class WebScraper:
    def __init__(self, fileOutput=False, fileName="result.tsv"):
        self.opener = build_opener()
        # Like a human
        self.opener.addheaders = [
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36"),
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        ]
        with open("config.yml", "r") as stream:
            self.config = yaml.load(stream)
            if self.config["url_type"] != "incremental":
                print("url_type `{url_type}` is not suppoted yet".format(url_type=self.config["url_type"]))
                sys.exit()
        self.fileOutput = fileOutput
        self.fileName = fileName

    def getAnchors(self, compliledRegExp):
        return self.bsObj.findAll("a", {"href": compliledRegExp})

    def crawl(self, url):
        self.url = url
        self.articleId = url[len("http://" + self.config['crawl_domain'] + "/"):]
        html = self.opener.open(url)
        self.rawHtml = html.read()
        self.bsObj = BeautifulSoup(self.rawHtml, "html.parser")

    def countLinks(self, regExp, date):
        anchors = self.getAnchors(regExp)
        print("{url}\t{article_id}\t{count}\t{last_updated_at}".format(url=self.url, article_id=self.articleId, count=len(anchors), last_updated_at=date))
        if self.fileOutput is True:
            f = open(self.fileName, "a")
            f.write("{url}\t{article_id}\t{count}\t{last_updated_at}\n".format(url=self.url, article_id=self.articleId, count=len(anchors), last_updated_at=date))
            f.close()

    def getLastUpdatedAt(self):
        articleDate = self.bsObj.find("p", { "class": "article_date" })
        if articleDate is None:
            articleDate = self.bsObj.find("p", { "class": "update" })
            if articleDate is None:
                return None
            dateStr = articleDate.get_text()
            return datetime.strptime(dateStr, self.config["last_updated_at_format_bottom"]).strftime("%Y-%m-%d")
        else:
            dateStr = articleDate.get_text()
            return datetime.strptime(dateStr, self.config["last_updated_at_format"]).strftime("%Y-%m-%d")

if __name__ == "__main__":
    ws = WebScraper(fileOutput=True)
    baseUrl = "http://" + ws.config["crawl_domain"]

    if os.path.isfile(ws.fileName):
        os.remove(ws.fileName)

    i = ws.config["resource_id"]["min"]
    while i <= ws.config["resource_id"]["max"]:
        url = urljoin(baseUrl, str(i))
        hrefDomainRegexp = re.compile(ws.config["href_domain_regexp"])
        pagerRegExp = re.compile(ws.config["pager_regexp"])

        try:
            ws.crawl(url)
            ws.countLinks(hrefDomainRegexp, ws.getLastUpdatedAt())
            pagers = ws.getAnchors(pagerRegExp)
            for pager in pagers:
                nextUrl = urljoin(baseUrl, pager["href"])
                ws.crawl(nextUrl)
                ws.countLinks(hrefDomainRegexp, ws.getLastUpdatedAt())
        except HTTPError as e:
            print("{url}\t\t\t\t{error}".format(url=url, error=e))

        i += 1
        time.sleep(0.3)
