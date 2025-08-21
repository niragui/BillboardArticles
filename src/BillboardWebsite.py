import requests

import datetime

import os
import sys

from .constants import BILLBOARD_URL
from .exceptions import ConnectionError

from .filters import ARTICLES_FILTER, ARTICLE_URL_FILTER
from .utils import get_article_id

from .BillboardArticle import BillboardArticle

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(THIS_FOLDER))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup


class BillboardWebsite():
    def __init__(self) -> None:
        self.html_soup = None
        self.read_date = None

        self.read_html()

    def read_html(self):
        """
        Asks the Billboard website to retrieve the html content from it
        and sets the soup element
        """
        billboard_response = requests.get(BILLBOARD_URL)

        self.read_date = datetime.datetime.now()

        if billboard_response.status_code // 100 != 2:
            raise ConnectionError(f"Couldn't Read Billboard Website [{billboard_response.status_code} | {billboard_response.reason}]")

        html = billboard_response.content.decode("utf-8")

        self.html_soup = MySoup(html)

    def reload(self):
        """
        Relod the data
        """
        self.read_html()

    def get_articles(self):
        """
        Read the articles and save them in the object attribute
        """
        if self.html_soup is None:
            self.read_html()

        articles_nodes = self.html_soup.find_all(ARTICLES_FILTER)

        articles_urls = []

        for node in articles_nodes:
            url_node = node.find(ARTICLE_URL_FILTER)

            if url_node is None:
                continue

            url = url_node.attrs["href"]
            articles_urls.append(url)

        if len(articles_urls) == 0:
            return []

        articles = []
        for url in articles_urls:
            new_article = BillboardArticle(url)
            articles.append(new_article)

        return articles

    def __repr__(self) -> str:
        return f"BillboardWesbite(Updated: {self.read_date})"

    def __str__(self) -> str:
        return f"BillboardWesbite(Updated: {self.read_date})" 