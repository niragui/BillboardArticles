from src.BillboardWebsite import BillboardWebsite
from src.BillboardArticle import BillboardArticle

from src.article_image.article_image import ArticleImage

import os
import sys


THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(THIS_FOLDER)

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.elements.filter import NodeFilter


url = "https://www.billboard.com/music/chart-beat/morgan-wallen-im-the-problem-11-weeks-atop-billboard-200-1236045928/"
article = BillboardArticle(url)

image = ArticleImage(article)

with open("article.html", "w", encoding="utf-8") as f:
    f.write(image.get_html())