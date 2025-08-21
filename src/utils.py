

def get_article_id(url: str):
    """
    Return the ID of the article url

    Paramters:
        - url: String of the URL of the article
    """
    if url.endswith("/"):
        url = url[:-1]

    id_start = url.rfind("-") + 1

    return url[id_start:]
