from link_parser import LinkParser
from request import Request
from rule_processor import RuleProcessor
from exploit_processor import ExploitProcessor

class Spider:
    def __init__(self, url, authentication_instance = None, banned_urls = []):
        self.url = url
        self.auth_cookie = None
        self.banned_urls = banned_urls

        if authentication_instance:
            self.auth_cookie = authentication_instance.get_cookie_jar()

    def run(self):
        http_request = Request(self.auth_cookie)
        pagesToVisit = [self.url]
        numberVisited = 0
        foundWord = False
        already_visited = []
        parser = LinkParser(self.url)
        rule_processor = RuleProcessor()
        exploit_processor = ExploitProcessor()

        while pagesToVisit != [] and not foundWord:
            # Start from the beginning of our collection of pages to visit:
            url = pagesToVisit[0]
            pagesToVisit = pagesToVisit[1:]

            if url in already_visited:
                continue

            if "logout" in url and self.auth_cookie != None:
                continue

            if self.is_url_banned(url):
                continue

            try:
                print "Visiting: %s" % url
                http_request.send(url)
                links = parser.getLinks(http_request)
                body = http_request.get_body()

                candidates = rule_processor.test_all_rules(http_request, body, url)

                if len(candidates) > 0:
                    print "==== Identified as vulnerable Exploiting... ===="
                    result = exploit_processor.run_all_exploits(http_request, body, url)

                    if result != False:
                        print "==== Exploit Successful... ===="
                        print result
                    else:
                        print "==== Exploit Failed... ===="

                pagesToVisit = pagesToVisit + links
                already_visited.append(url)
                numberVisited = numberVisited + 1
            except:
                print(" **Failed!**")

    def is_url_banned(self, url):
        for banned_url in self.banned_urls:
            if banned_url in url:
                return True

        return False