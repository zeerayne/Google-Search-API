from utils import get_html_from_dynamic_site
from bs4 import BeautifulSoup
import urlparse


def write_html_to_file(html, filename):
    of = open(filename, "w")
    of.write(html.encode("utf-8"))
    # of.flush()
    of.close()



IMAGE_FORMATS = ["bmp", "gif", "jpg", "png", "psd", "pspimage", "thm",
                 "tif", "yuv", "ai", "drw", "eps", "ps", "svg", "tiff",
                 "jpeg", "jif", "jfif", "jp2", "jpx", "j2k", "j2c", "fpx",
                 "pcd", "png", "pdf"]

class ImageType:
    NONE = None
    FACE = "face"
    PHOTO = "photo"
    CLIPART = "clipart"
    LINE_DRAWING = "lineart"


class SizeCategory:
    NONE = None
    ICON = "i"
    LARGE = "l"
    MEDIUM = "m"
    SMALL = "s"
    LARGER_THAN = "lt"
    EXACTLY = "ex"


class LargerThan:
    NONE = None
    QSVGA = "qsvga"  # 400 x 300
    VGA = "vga"     # 640 x 480
    SVGA = "svga"   # 800 x 600
    XGA = "xga"     # 1024 x 768
    MP_2 = "2mp"    # 2 MP (1600 x 1200)
    MP_4 = "4mp"    # 4 MP (2272 x 1704)
    MP_6 = "6mp"    # 6 MP (2816 x 2112)
    MP_8 = "8mp"    # 8 MP (3264 x 2448)
    MP_10 = "10mp"  # 10 MP (3648 x 2736)
    MP_12 = "12mp"  # 12 MP (4096 x 3072)
    MP_15 = "15mp"  # 15 MP (4480 x 3360)
    MP_20 = "20mp"  # 20 MP (5120 x 3840)
    MP_40 = "40mp"  # 40 MP (7216 x 5412)
    MP_70 = "70mp"  # 70 MP (9600 x 7200)


class ColorType:
    NONE = None
    COLOR = "color"
    BLACK_WHITE = "gray"
    SPECIFIC = "specific"


class ImageOptions:

    """Allows passing options to filter a google images search."""

    def __init__(self):
        self.image_type = None
        self.size_category = None
        self.larger_than = None
        self.exact_width = None
        self.exact_height = None
        self.color_type = None
        self.color = None

    def get_tbs(self):
        tbs = None
        if self.image_type:
            # clipart
            tbs = add_to_tbs(tbs, "itp", self.image_type)
        if self.size_category and not (self.larger_than or (self.exact_width and self.exact_height)):
            # i = icon, l = large, m = medium, lt = larger than, ex = exact
            tbs = add_to_tbs(tbs, "isz", self.size_category)
        if self.larger_than:
            # qsvga,4mp
            tbs = add_to_tbs(tbs, "isz", SizeCategory.LARGER_THAN)
            tbs = add_to_tbs(tbs, "islt", self.larger_than)
        if self.exact_width and self.exact_height:
            tbs = add_to_tbs(tbs, "isz", SizeCategory.EXACTLY)
            tbs = add_to_tbs(tbs, "iszw", self.exact_width)
            tbs = add_to_tbs(tbs, "iszh", self.exact_height)
        if self.color_type and not self.color:
            # color = color, gray = black and white, specific = user defined
            tbs = add_to_tbs(tbs, "ic", self.color_type)
        if self.color:
            tbs = add_to_tbs(tbs, "ic", ColorType.SPECIFIC)
            tbs = add_to_tbs(tbs, "isc", self.color)
        return tbs


class ImageResult:

    """Represents a google image search result."""

    ROOT_FILENAME = "img"
    DEFAULT_FORMAT = "jpg"

    def __init__(self):
        self.name = None
        self.link = None
        self.thumb = None
        self.thumb_width = None
        self.thumb_height = None
        self.width = None
        self.height = None
        self.filesize = None
        self.format = None
        self.domain = None
        self.page = None
        self.index = None
        self.site = None

    def __repr__(self):
        string = "ImageResult(" + \
                 "index={}, page={}, ".format(self.index, self.page) + \
                 "domain={}, link={})".format(self.domain, self.link)
        return string

    def download(self, path="download"):
        """Download an image to a given path."""

        self._create_path(path)

        try:
            response = requests.get(self.link, stream=True)

            path_filename = self._get_path_filename(path)
            with open(path_filename, 'wb') as output_file:
                shutil.copyfileobj(response.raw, output_file)

            del response

        except Exception as inst:
            print self.link, "has failed:"
            print inst

    def _get_path_filename(self, path):
        """Build the filename to download.

        Checks that filename is not already in path. Otherwise looks for
        another name.

        >>> ir = ImageResult()
        >>> ir._get_path_filename("test")
        'test\\\img3.jpg'
        >>> ir.name = "pirulo"
        >>> ir.format = "jpg"
        >>> ir._get_path_filename("test")
        'test\\\pirulo.jpg'
        """

        path_filename = None

        # preserve the original name
        if self.name and self.format:
            original_filename = self.name + "." + self.format
            path_filename = os.path.join(path, original_filename)

        # create a default name if there is no original name
        if not path_filename or os.path.isfile(path_filename):

            # take the format of the file, or use default
            if self.format:
                file_format = self.format
            else:
                file_format = self.DEFAULT_FORMAT

            # create root of file, until reaching a non existent one
            i = 1
            default_filename = self.ROOT_FILENAME + str(i) + "." + file_format
            path_filename = os.path.join(path, default_filename)
            while os.path.isfile(path_filename):
                i += 1
                default_filename = self.ROOT_FILENAME + str(i) + "." + \
                    file_format
                path_filename = os.path.join(path, default_filename)

        return path_filename

    def _create_path(self, path):
        """Create a path, if it doesn't exists."""

        if not os.path.isdir(path):
            os.mkdir(path)


# PRIVATE METHODS
def _parse_image_format(image_link):
    """Parse an image format from a download link.

    Args:
        image_link: link to download an image.

    >>> link = "http://blogs.elpais.com/.a/6a00d8341bfb1653ef01a73dbb4a78970d-pi"
    >>> Google._parse_image_format(link)

    >>> link = "http://minionslovebananas.com/images/gallery/preview/Chiquita-DM2-minion-banana-3.jpg%3Fw%3D300%26h%3D429"
    >>> Google._parse_image_format(link)
    'jpg'

    """
    parsed_format = image_link[image_link.rfind(".") + 1:]

    if parsed_format not in IMAGE_FORMATS:
        for image_format in IMAGE_FORMATS:
            if image_format in parsed_format:
                parsed_format = image_format
                break

    if parsed_format not in IMAGE_FORMATS:
        parsed_format = None

    return parsed_format


def _get_images_req_url(query, image_options=None, page=0, per_page=20):
    query = query.strip().replace(":", "%3A").replace(
        "+", "%2B").replace("&", "%26").replace(" ", "+")

    # url = "http://images.google.com/images?q=%s&sa=N&start=%i&ndsp=%i&sout=1" % (
    # query, page * per_page, per_page)
    # TRYING NEW URL
    url = "https://www.google.com.ar/search?q={}".format(query) + \
          "&es_sm=122&source=lnms" + \
          "&tbm=isch&sa=X&ei=DDdUVL-fE4SpNq-ngPgK&ved=0CAgQ_AUoAQ" + \
          "&biw=1024&bih=719&dpr=1.25"

    if image_options:
        tbs = image_options.get_tbs()
        if tbs:
            url = url + tbs

    return url


# PUBLIC METHODS
def search_old(query, image_options=None, pages=1):
    results = []
    for i in range(pages):
        url = get_image_search_url(query, image_options, i)
        html = get_html(url)
        if html:
            if Google.DEBUG_MODE:
                write_html_to_file(
                    html, "images_{0}_{1}.html".format(query.replace(" ", "_"), i))
            j = 0
            soup = BeautifulSoup(html)
            match = re.search("dyn.setResults\((.+)\);</script>", html)
            if match:
                init = unicode(match.group(1), errors="ignore")
                tokens = init.split('],[')
                for token in tokens:
                    res = ImageResult()
                    res.page = i
                    res.index = j
                    toks = token.split(",")

                    # should be 32 or 33, but seems to change, so just make sure no exceptions
                    # will be thrown by the indexing
                    if (len(toks) > 22):
                        for t in range(len(toks)):
                            toks[t] = toks[t].replace('\\x3cb\\x3e', '').replace(
                                '\\x3c/b\\x3e', '').replace('\\x3d', '=').replace('\\x26', '&')
                        match = re.search(
                            "imgurl=(?P<link>[^&]+)&imgrefurl", toks[0])
                        if match:
                            res.link = match.group("link")
                        res.name = toks[6].replace('"', '')
                        res.thumb = toks[21].replace('"', '')
                        res.format = toks[10].replace('"', '')
                        res.domain = toks[11].replace('"', '')
                        match = re.search(
                            "(?P<width>[0-9]+) &times; (?P<height>[0-9]+) - (?P<size>[^ ]+)", toks[9].replace('"', ''))
                        if match:
                            res.width = match.group("width")
                            res.height = match.group("height")
                            res.filesize = match.group("size")
                        results.append(res)
                        j = j + 1
    return results


def search(query, image_options=None, images=50):
    """Main method to search images in google."""

    results = set()
    curr_img = 0
    page = 0
    while curr_img < images:

        page += 1
        url = _get_images_req_url(query, image_options, page)
        html = get_html_from_dynamic_site(url)
        # write_html_to_file(html, "test_search_images.html")

        if html:

            # parse html into bs
            soup = BeautifulSoup(html)

            # find all divs containing an image
            div_container = soup.find("div", {"id": "rg_s"})
            divs = div_container.find_all("div", {"class": "rg_di"})
            j = 0
            for div in divs:

                # try:
                res = ImageResult()

                # store indexing paramethers
                res.page = page
                res.index = j

                # get url of image and its paramethers
                a = div.find("a")
                if a:
                    google_middle_link = a["href"]
                    url_parsed = urlparse.urlparse(google_middle_link)
                    qry_parsed = urlparse.parse_qs(url_parsed.query)
                    res.link = qry_parsed["imgurl"][0]
                    res.format = _parse_image_format(res.link)
                    res.width = qry_parsed["w"][0]
                    res.height = qry_parsed["h"][0]
                    res.site = qry_parsed["imgrefurl"][0]
                    res.domain = urlparse.urlparse(res.site).netloc

                # get url of thumb and its size paramethers
                img = a.find_all("img")
                if img:

                    # get url trying "src" and "data-src" keys
                    try:
                        res.thumb = img[0]["src"]
                    except:
                        res.thumb = img[0]["data-src"]

                    try:
                        img_style = img[0]["style"].split(";")
                        img_style_dict = {i.split(":")[0]: i.split(":")[1]
                                          for i in img_style}
                        res.thumb_width = img_style_dict["width"]
                        res.thumb_height = img_style_dict["height"]
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print exc_type, exc_value, "index=", res.index

                prev_num_results = len(results)
                results.add(res)
                curr_num_results = len(results)

                # increment image counter only if new image was added
                images_added = curr_num_results - prev_num_results
                curr_img += images_added
                if curr_img >= images:
                    break

                j = j + 1

    return set(results)


def download(image_results, path=None):
    """Download a list of images.

    Args:
        images_list: a list of ImageResult instances
        path: path to store downloaded images.
    """

    total_images = len(image_results)
    i = 1
    for image_result in image_results:
        progress = "".join(["Downloading image ", str(i),
                            " (", str(total_images), ")"])
        print progress
        if path:
            image_result.download(path)
        else:
            image_result.download()
        i += 1
