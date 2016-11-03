
import urllib.request
import time

class URLResource:
    'Class to load URL resources'
    time = 0

    def __init__(self, url):
        self.url = url

    def read(self):
        """
        :return: content from URL
        """
        start = time.time()
        response = urllib.request.urlopen(self.url)
        content = response.read().decode(response.headers.get_content_charset())
        self.time = round((time.time() - start) * 1000)
        return content

    def elapsed(self):
        return self.time