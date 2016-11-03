from com.conversant.common.URLResource import URLResource
import urllib

class URLEndpoint:
    def __init__(self, base):
        self.base = base

    def getContent(self, params):
        url = self.base.format(urllib.parse.quote(params))
        resource = URLResource(url)
        return  resource.read()
