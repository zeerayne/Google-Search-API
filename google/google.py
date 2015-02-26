from bs4 import BeautifulSoup
import re
import images
import currency
import calculator
from utils import write_html_to_file, _get_search_url, get_html, normalize_query


__author__ = "Anthony Casagrande <birdapi@gmail.com>, " + \
    "Agustin Benassi <agusbenassi@gmail.com>"
__version__ = "1.0.0"


# GLOBAL METHODS


def add_to_tbs(tbs, name, value):
    if tbs:
        return "%s,%s:%s" % (tbs, name, value)
    else:
        return "&tbs=%s:%s" % (name, value)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# RESULT CLASSES
class GoogleResult:

    """Represents a google search result."""

    def __init__(self):
        self.name = None
        self.link = None
        self.description = None
        self.thumb = None
        self.cached = None
        self.page = None
        self.index = None

    def __repr__(self):
        list_google = ["Name: ", self.name,
                       "\nLink: ", self.link]
        return "".join(list_google)


class ShoppingResult:

    """Represents a shopping result."""

    def __init__(self):
        self.name = None
        self.link = None
        self.thumb = None
        self.subtext = None
        self.description = None
        self.compare_url = None
        self.store_count = None
        self.min_price = None

    def __repr__(self):
        return self.name


# PUBLIC CLASS
class Google:

    """Defines the public static api methods."""

    DEBUG_MODE = False

    @staticmethod
    def search(query, pages=1):
        """Returns a list of GoogleResult."""

        results = []
        for i in range(pages):
            url = _get_search_url(query, i)
            html = get_html(url)
            if html:
                if Google.DEBUG_MODE:
                    write_html_to_file(
                        html, "{0}_{1}.html".format(query.replace(" ", "_"), i))
                soup = BeautifulSoup(html)
                lis = soup.findAll("li", attrs={"class": "g"})
                j = 0
                for li in lis:
                    res = GoogleResult()
                    res.page = i
                    res.index = j
                    a = li.find("a")
                    res.name = a.text.strip()
                    res.link = a["href"]
                    if res.link.startswith("/search?"):
                        # this is not an external link, so skip it
                        continue
                    sdiv = li.find("div", attrs={"class": "s"})
                    if sdiv:
                        res.description = sdiv.text.strip()
                    results.append(res)
                    j = j + 1
        return results

    search_images_old = staticmethod(images.search_old)

    search_images = staticmethod(images.search)

    convert_currency = staticmethod(currency.convert)

    exchange_rate = staticmethod(currency.exchange_rate)

    calculate = staticmethod(calculator.calculate)

    @staticmethod
    def shopping(query, pages=1):
        results = []
        for i in range(pages):
            url = Google._get_shopping_url(query, i)
            html = get_html(url)
            if html:
                if Google.DEBUG_MODE:
                    write_html_to_file(
                        html, "shopping_{0}_{1}.html".format(query.replace(" ", "_"), i))
                j = 0
                soup = BeautifulSoup(html)

                products = soup.findAll("li", "g")
                for prod in products:
                    res = ShoppingResult()

                    divs = prod.findAll("div")
                    for div in divs:
                        match = re.search(
                            "from (?P<count>[0-9]+) stores", div.text.strip())
                        if match:
                            res.store_count = match.group("count")
                            break

                    h3 = prod.find("h3", "r")
                    if h3:
                        a = h3.find("a")
                        if a:
                            res.compare_url = a["href"]
                        res.name = h3.text.strip()

                    psliimg = prod.find("div", "psliimg")
                    if psliimg:
                        img = psliimg.find("img")
                        if img:
                            res.thumb = img["src"]

                    f = prod.find("div", "f")
                    if f:
                        res.subtext = f.text.strip()

                    price = prod.find("div", "psliprice")
                    if price:
                        res.min_price = price.text.strip()

                    results.append(res)
                    j = j + 1
        return results

    @staticmethod
    def _get_shopping_url(query, page=0, per_page=10):
        return "http://www.google.com/search?hl=en&q={0}&tbm=shop&start={1}&num={2}".format(normalize_query(query), page * per_page, per_page)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
