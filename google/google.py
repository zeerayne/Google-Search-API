from bs4 import BeautifulSoup
import httplib
import urllib2
import re
import images
import currency

try:
    import json
except ImportError:
    import simplejson as json

__author__ = "Anthony Casagrande <birdapi@gmail.com>, " + \
    "Agustin Benassi <agusbenassi@gmail.com>"
__version__ = "1.0.0"


# GLOBAL METHODS
def normalize_query(query):
    return query.strip().replace(":", "%3A").replace("+", "%2B").replace("&", "%26").replace(" ", "+")


def add_to_tbs(tbs, name, value):
    if tbs:
        return "%s,%s:%s" % (tbs, name, value)
    else:
        return "&tbs=%s:%s" % (name, value)


def parse_calc_result(string):
    result = CalculatorResult()
    result.fullstring = string
    string = string.strip().replace(u"\xa0", " ")
    if string.find("=") != -1:
        result.expr = string[:string.rfind("=")].strip()
        string = string[string.rfind("=") + 2:]
        result.result = string
    tokens = string.split(" ")
    if len(tokens) > 0:
        result.value = ""
        for token in tokens:
            if is_number(token):
                result.value = result.value + token
            else:
                if result.unit:
                    result.unit = result.unit + " " + token
                else:
                    result.unit = token
        return result
    return None


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_html(url):
    try:
        request = urllib2.Request(url)
        request.add_header(
            "User-Agent", "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101")
        html = urllib2.urlopen(request).read()
        return html
    except:
        print "Error accessing:", url
        return None


def write_html_to_file(html, filename):
    of = open(filename, "w")
    of.write(html)
    of.flush()
    of.close()


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


class CalculatorResult:

    """Represents a result returned from google calculator."""

    def __init__(self):
        self.value = None
        self.unit = None
        self.expr = None
        self.result = None
        self.fullstring = None


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
            url = Google._get_search_url(query, i)
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

    @staticmethod
    def _get_search_url(query, page=0, per_page=10):
        # note: num per page might not be supported by google anymore (because of
        # google instant)
        return "http://www.google.com/search?hl=en&q=%s&start=%i&num=%i" % (normalize_query(query), page * per_page, per_page)

    @staticmethod
    def calculate_old(expr):
        url = Google._get_search_url(expr)
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html)
            topstuff = soup.find("div", id="topstuff")
            if topstuff:
                a = topstuff.find("a")
                if a and a["href"].find("calculator") != -1:
                    h2 = topstuff.find("h2")
                    if h2:
                        return parse_calc_result(h2.text)
        return None

    @staticmethod
    def search_images_old(query, image_options=None, pages=1):
        """Old method to search images in google."""

        return images.search_old(query, image_options, pages)

    @staticmethod
    def search_images(query, image_options=None, num_images=50):
        """Search images in google.

        # >>> results = Google.search_images("banana")
        # <type 'exceptions.KeyError'> 'style' index= 97
        # <type 'exceptions.KeyError'> 'style' index= 98
        # <type 'exceptions.KeyError'> 'style' index= 99
        # >>> len(results)
        # 100
        # >>> isinstance(results[0], ImageResult)
        # True
        """

        return images.search(query, image_options, num_images)

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

    @staticmethod
    def convert_currency(amount, from_currency, to_currency):
        """Method to convert currency.

        Args:
            amount: numeric amount to convert
            from_currency: currency denomination of the amount to convert
            to_currency: target currency denomination to convert to
        """
        return currency.convert_currency(amount, from_currency, to_currency)

    @staticmethod
    def exchange_rate(from_currency, to_currency):
        """Gets the exchange rate of one currency to another.

        Args:
            from_currency: starting currency denomination (1)
            to_currency: target currency denomination to convert to (rate)

        Returns:
            rate / 1 to convert from_currency in to_currency
        """
        return currency.exchange_rate(from_currency, to_currency)

    @staticmethod
    def calculate(expr):
        conn = httplib.HTTPSConnection("www.google.com")
        req_url = "/ig/calculator?hl=en&q={0}".format(expr.replace(" ", "%20"))
        headers = {
            "User-Agent": "Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101"}
        conn.request("GET", req_url, "", headers)
        response = conn.getresponse()
        j = response.read().decode("utf-8").replace(u"\xa0", "")
        conn.close()
        j = re.sub(r"{\s*'?(\w)", r'{"\1', j)
        j = re.sub(r",\s*'?(\w)", r',"\1', j)
        j = re.sub(r"(\w)'?\s*:", r'\1":', j)
        j = re.sub(r":\s*'(\w)'\s*([,}])", r':"\1"\2', j)
        js = json.loads(j)
        return parse_calc_result(js["lhs"] + " = " + js["rhs"])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
