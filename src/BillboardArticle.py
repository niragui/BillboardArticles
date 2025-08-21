import requests

from bisect import insort

import datetime

import os
import sys

from .exceptions import ConnectionError

from .filters import TOPIC_FILTER, DATE_FILTER, TITLE_FILTER
from .filters import SUBTITITLE_FILTER, WRITER_FILTER, COVER_FILTER
from .filters import TEXT_FILTER, TEXT_HEADERS_FILTER, IMAGE_FILTER
from .filters import CHART_FILTER, ARTIST_FILTER

from .constants import IMPORTANT_CHARTS_REVEALS

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(THIS_FOLDER))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.parser import MySoup
from BeautifulSoup.src.elements.text import Text
from BeautifulSoup.src.elements.tag import Tag


DATE_FORMAT = "%m/%d/%Y"
CHART_URL = "https://www.billboard.com/charts/"
ARTIST_URL = "https://www.billboard.com/artist/"


class BillboardArticle():
    def __init__(self,
                 url: str) -> None:
        self.url = url
        self.html_soup = None

        self.topic = None
        self.date = None

        self.title = None
        self.subtitle = None
        self.writer = None

        self.charts = []
        self.artists = []

        self.cover = None
        self._texts = []

        self.read_html()
        self.read_data()

    def read_html(self):
        """
        Asks the Billboard website to retrieve the html content from it
        and sets the soup element
        """
        billboard_response = requests.get(self.url)

        if billboard_response.status_code // 100 != 2:
            raise ConnectionError(f"Couldn't Read Billboard Website [{billboard_response.status_code} | {billboard_response.reason}]")

        html = billboard_response.content.decode("utf-8")

        self.html_soup = MySoup(html)

    @property
    def chart_revealed(self):
        """
        Returns a string indicating which chart was revealed. If None
        it's not a chart reveal.
        """
        matched_chart = None

        for chart, reveal_text in IMPORTANT_CHARTS_REVEALS.items():
            if self.text.find(reveal_text) >= 0:
                matched_chart = chart
                break

        return matched_chart

    def read_data(self):
        """
        Reads the HTML of the article to set the data
        """
        if self.html_soup is None:
            self.read_html()

        topic_node = self.html_soup.find(TOPIC_FILTER)
        if topic_node:
            self.topic = topic_node.text.strip()

        date_node = self.html_soup.find(DATE_FILTER)
        if date_node:
            date = datetime.datetime.strptime(date_node.text.strip(), DATE_FORMAT)
            self.date = date.date()

        title_node = self.html_soup.find(TITLE_FILTER)
        if title_node:
            self.title = title_node.text.strip()

        subtitle_node = self.html_soup.find(SUBTITITLE_FILTER)
        if subtitle_node:
            self.subtitle = subtitle_node.text.strip()

        writer_node = self.html_soup.find(WRITER_FILTER)
        if writer_node:
            self.writer = writer_node.text.strip()

        cover_node = self.html_soup.find(COVER_FILTER)
        if cover_node:
            image_node = cover_node.find(IMAGE_FILTER)
            if image_node:
                img_url = image_node.attrs.get("src", None)
                self.cover = img_url

        text_header_nodes = self.html_soup.find_all(TEXT_FILTER)
        if text_header_nodes:
            self._texts = text_header_nodes

        text_header_nodes = self.html_soup.find_all(TEXT_HEADERS_FILTER)
        if text_header_nodes:
            for text_node in text_header_nodes:
                insort(self._texts, text_node)

        artist_nodes = self.html_soup.find_all(ARTIST_FILTER)
        if artist_nodes:
            self.artists = []
            for artist_node in artist_nodes:
                artist_name = artist_node.text
                artist_name = artist_name.replace("\n", "")
                artist_name = artist_name.replace("\t", "")
                artist_name = artist_name.strip()

                if artist_name not in self.artists:
                    self.artists.append(artist_name)

        charts_nodes = self.html_soup.find_all(CHART_FILTER)
        if charts_nodes:
            self.charts = []
            for chart_node in charts_nodes:
                chart_name = chart_node.text
                chart_name = chart_name.replace("\n", "")
                chart_name = chart_name.replace("\t", "")
                chart_name = chart_name.strip()

                if chart_name not in self.charts:
                    self.charts.append(chart_name)

    @property
    def text(self):
        """
        Returns the article text as plain text
        """
        final_text = ""
        for text in self._texts:
            html_node_text = ""
            for sub_node in text.children:
                if isinstance(sub_node, Text):
                    html_node_text += sub_node.content
                elif not isinstance(sub_node, Tag):
                    continue
                elif sub_node.name == "div":
                    continue
                else:
                    html_node_text += sub_node.text

            node_text = html_node_text.replace("\n", "").replace("\t", "").strip()
            if len(node_text) > 0:
                final_text += f"{node_text}\n\n"

        return final_text

    def __repr__(self) -> str:
        return f"BillboardArticle(Topic: {self.topic} | Title: {self.title} | By: {self.writer} | On: {self.date})"

    def __str__(self) -> str:
        return f"BillboardArticle(Topic: {self.topic} | Title: {self.title} | By: {self.writer} | On: {self.date})"