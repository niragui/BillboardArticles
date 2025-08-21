import os

from .json_handle import read_json

BILLBOARD_URL = "https://www.billboard.com/"

THIS_FOLDER = os.path.dirname(__file__)
IMPORTANT_CHARTS_FILE = os.path.join(THIS_FOLDER, "charts_reveals.json")

IMPORTANT_CHARTS_REVEALS = read_json(IMPORTANT_CHARTS_FILE)