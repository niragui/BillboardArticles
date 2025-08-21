from typing import Optional

import json

from enum import Enum

from functools import partial

import os
import sys

THIS_FOLDER = os.path.dirname(__file__)
AUTOMATIONS_FOLDER = os.path.dirname(os.path.dirname(THIS_FOLDER))

sys.path.append(AUTOMATIONS_FOLDER)

from BeautifulSoup.src.elements.filter import NodeFilter

THIS_FOLDER = os.path.dirname(__file__)
FILTERS_FILE = os.path.join(THIS_FOLDER, "filters.json")

with open(FILTERS_FILE) as f:
    FILTERS_DATA = json.load(f)

ACTION_FIELD = "action"
VALUE_FIELD = "value"


class Actions(Enum):
    EQUALS = "equals"
    STARTS = "starts_with"
    CONTAINS = "contains"
    ENDS = "ends_with"
    NOT_EQUALS = "not_equals"
    NOT_EXISTS = "not_exists"


def evaluate_rule(attr_value: Optional[str],
                  rule: dict):
    """
    Evaluates a single attributes rule

    Parameters:
        - attr_value: Value of the attribute being evaluted
        - rule: Dictionary of the rule {action: value}
    """
    if not isinstance(rule, dict):
        return False

    action = rule.get(ACTION_FIELD, None)
    value = rule.get(VALUE_FIELD, None)

    if not action:
        return False

    try:
        action = Actions(action)
    except ValueError:
        return False

    if action == Actions.NOT_EXISTS:
        return attr_value is None

    if attr_value is None or value is None:
        return False

    attr_value = attr_value.strip()

    if action == Actions.EQUALS:
        return attr_value == value
    elif action == Actions.STARTS:
        return attr_value.startswith(value)
    elif action == Actions.CONTAINS:
        return value in attr_value
    elif action == Actions.ENDS:
        return attr_value.endswith(value)
    elif action == Actions.NOT_EQUALS:
        return attr_value != value
    else:
        raise ValueError(f"Unsupported action: {action}")


def attrs_filter(attrs: dict,
                 rules: dict):
    """
    Evalutates the attributes to match the rules dictionary

    Parameters:
        - attrs: Attibutes dictionary to evalute
        - rules: Dictionary of rules to use for the given item
    """
    for attr_key, condition in rules.items():
        attr_val = attrs.get(attr_key, None)
        if isinstance(attr_val, str):
            attr_val = attr_val.strip()

        rule_list = condition if isinstance(condition, list) else [condition]

        if not any(evaluate_rule(attr_val, rule) for rule in rule_list):
            return False

    return True


def get_filter(rules: dict):
    """
    Returns the NodeFilter for the json data given

    Parameters:
        - rules: Dictionary with the rules to follow
    """
    tag_name = rules.get("tag", None)
    attr_rules = rules.get("attributes", {})

    attr_rules = partial(attrs_filter, rules=attr_rules)

    return NodeFilter(tag_name, None, attr_rules)


ARTICLES_FILTER = get_filter(FILTERS_DATA.get("articles", {}))
ARTICLE_URL_FILTER = get_filter(FILTERS_DATA.get("article_url", {}))

TOPIC_FILTER = get_filter(FILTERS_DATA.get("article-topic", {}))
DATE_FILTER = get_filter(FILTERS_DATA.get("article-date", {}))
TITLE_FILTER = get_filter(FILTERS_DATA.get("article-title", {}))
SUBTITITLE_FILTER = get_filter(FILTERS_DATA.get("article-subtitle", {}))
WRITER_FILTER = get_filter(FILTERS_DATA.get("article-writer", {}))
COVER_FILTER = get_filter(FILTERS_DATA.get("article-cover", {}))
IMAGE_FILTER = get_filter(FILTERS_DATA.get("article-image", {}))
TEXT_FILTER = get_filter(FILTERS_DATA.get("article-texts", {}))
TEXT_HEADERS_FILTER = get_filter(FILTERS_DATA.get("article-texts-headers", {}))

CHART_FILTER = get_filter(FILTERS_DATA.get("article-charts", {}))
ARTIST_FILTER = get_filter(FILTERS_DATA.get("article-artists", {}))