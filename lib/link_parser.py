from HTMLParser import HTMLParser
from urlparse import urljoin

class LinkParser(HTMLParser):
    def __init__(self, scope_url):
        HTMLParser.__init__(self)
        self.scope_url = scope_url

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = urljoin(self.baseUrl, value)

                    if self.scope_url not in newUrl:
                        continue

                    self.links = self.links + [newUrl]

    def getLinks(self, request):
        self.links = []
        self.baseUrl = request.get_url()

        if 'text/html' in request.get_header('Content-Type'):
            htmlBytes = request.get_body()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return self.links
        else:
            return "",[]