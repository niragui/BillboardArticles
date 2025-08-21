from ..BillboardArticle import BillboardArticle

from .constants import CSS_TEXT

import os
import sys


THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(THIS_FOLDER)))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.elements.text import Text
from BeautifulSoup.src.elements.tag import Tag


class ArticleImage():
    def __init__(self,
                 article: BillboardArticle) -> None:
        self.article = article

    def get_html(self):
        """
        Returns the html of the article
        """
        html_text = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.article.title}</title>
        """
        html_text += CSS_TEXT
        html_text += "</head>"
        html_text += f"""
            <body>
            <div class="container">
                <div class="left-panel">
                    <h1>{self.article.title}</h1>
                    <h2>{self.article.subtitle}</h2>
                    <img src="{self.article.cover}" alt="Article Image">
                    <div class="meta">
                        <p><strong>Topic:</strong> {self.article.topic}</p>
                        <p><strong>Writer:</strong> {self.article.writer}</p>
                    </div>
                </div>
                <div class="right-panel">
        """
        for text_node in self.article._texts:
            html_node_text = ""
            for sub_node in text_node.children:
                if isinstance(sub_node, Text):
                    html_node_text += sub_node.content
                elif not isinstance(sub_node, Tag):
                    continue
                elif sub_node.name == "div":
                    continue
                else:
                    html_node_text += sub_node.text

            node_text = html_node_text.replace("\n", "").replace("\t", "").strip()
            node_html = f"<{text_node.name}>{node_text}</{text_node.name}>"
            html_text += f"{node_html}\n<br>\n"

        html_text += """
                    </div>
                </div>
            </body>
        </html>
        """

        return html_text
