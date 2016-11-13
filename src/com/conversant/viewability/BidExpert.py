import os
import csv
from time import sleep
from com.conversant.common.URLEndpoint import URLEndpoint
from com.conversant.viewability.BidExpertSegments import BidExpertSegments
from com.conversant.common.EnvConfig import EnvConfig


class BidExpert:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def run(self, reader, handler):
        for row in reader:
            segments = BidExpertSegments(self.endpoint.getContent(row[0]))
            output = row + segments.video()
            handler(output)


class BidExpertHandler:
    def __init__(self, name):
        self.file = open(name, 'w', newline='')
        self.writer = csv.writer(self.file)

    def __del__(self):
        self.close()

    def handle(self, row):
        self.writer.writerow(row)
        print(row)
        sleep(0.01)

    def close(self):
        self.file.close()


def main():
    config = EnvConfig()

    expert = BidExpert(URLEndpoint(config.segments_api))
    handler = BidExpertHandler(os.path.join(os.path.expanduser("~"), 'data', config.segments_results))

    try:
        with open(os.path.join(os.path.expanduser("~"), 'data', config.segments_urls),
                  newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            expert.run(reader, handler.handle)
    except (KeyboardInterrupt, SystemExit):
        raise
    else:
        handler.close()

if __name__ == '__main__':
    main()