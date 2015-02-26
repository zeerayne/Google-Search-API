from utils import _get_search_url, get_html
from bs4 import BeautifulSoup


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


def search(query, pages=1):
    """Returns a list of GoogleResult."""

    results = []
    for i in range(pages):
        url = _get_search_url(query, i)
        html = get_html(url)
        if html:
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
