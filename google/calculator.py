from utils import get_html_from_dynamic_site
from utils import _get_search_url
from bs4 import BeautifulSoup


class CalculatorResult:

    """Represents a result returned from google calculator."""

    def __init__(self):
        self.value = None
        self.from_value = None
        self.unit = None
        self.from_unit = None
        self.expr = None
        self.result = None
        self.fullstring = None


# PUBLIC
def calculate(expr):
    url = _get_search_url(expr)
    html = get_html_from_dynamic_site(url)
    bs = BeautifulSoup(html)

    cr = CalculatorResult()
    cr.value = _get_to_value(bs)
    cr.from_value = _get_from_value(bs)
    cr.unit = _get_to_unit(bs)
    cr.from_unit = _get_from_unit(bs)
    cr.expr = _get_expr(bs)
    cr.result = _get_result(bs)
    cr.fullstring = _get_fullstring(bs)

    return cr


# PRIVATE
def _get_to_value(bs):
    return float(bs.find("input", {"id": "ucw_rhs_d"})["value"])


def _get_from_value(bs):
    return float(bs.find("input", {"id": "ucw_lhs_d"})["value"])


def _get_to_unit(bs):
    return None


def _get_from_unit(bs):
    return None


def _get_expr(bs):
    return None


def _get_result(bs):
    return None


def _get_fullstring(bs):
    return None
