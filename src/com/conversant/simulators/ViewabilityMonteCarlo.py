from random import randint
from collections import OrderedDict
from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator


class ViewabilityMonteCarlo(AbstractViewabilitySimulator):
    def __init__(self, source='ad_quality.bids_view'):
        super().__init__(source)
        self.track = set()

    def generate(self):
        # ad_format_id,network_id,seller_id,site_id,media_size,ad_position,device,os,browser_name,browser_version
        inputs = {
            '0ad_format_id'      : ['18', '52', '20', '17', '0'],
            '1network_id'        : ['12783', '15900', '1982', '12783', '12783', '243', '14200', '14100', '14000', '14000', '12783'],
            '2seller_id'         : ['9336', '69173', '311', '10738', '209874', '38488', '560747', '3932', '208724'],
            '3site_id'           : ['16312', '76446', '1216817', '45026', '2038105', '85743'],
            '4media_size'        : ['11', '18', '21'],
            '5ad_position'       : ['0', '1'],
            '6device'            : ['Table', 'iPhone', 'Other'],
            '7os'                : ['Android 5.x', 'Windows 10', 'Windows 7', 'iOS 8.2', 'Mac OS X', 'Windows 8.1'],
            '8browser_name'      : ['Chrome', 'Chrome Mobile', 'Firefox', 'Apple WebKit', 'Safari', 'Internet Explorer'],
            '9browser_version'   : ['51', '45', '49', '6', '13', '54', '11', '43']
        }

        inputs = OrderedDict(sorted(inputs.items(), key=lambda t: t[0]))

        for s in range(1000):
            row = [0]
            for name in inputs:
                ln = len(inputs[name])
                i = randint(0, ln - 1)
                row.append(inputs[name][i])
            row.append(0)
            row.append(0)
            self.handle_row(row)

    def process_row(self, row, view):
        if view != -1:
            if view not in self.track:
                self.append(row[1:-2] + [view])
                self.track.add(view)


if __name__ == '__main__':
    validator = ViewabilityMonteCarlo()
    validator.generate()
    validator.output()
    validator.print_tree()
