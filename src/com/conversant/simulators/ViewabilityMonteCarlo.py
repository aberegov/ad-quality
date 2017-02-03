from random import randint
from collections import OrderedDict
import json
import os
from com.conversant.simulators.AbstractViewabilitySimulator import AbstractViewabilitySimulator


class ViewabilityMonteCarlo(AbstractViewabilitySimulator):
    def __init__(self, source='ad_quality.bids_view'):
        super().__init__(source)
        self.track = set()

    def generate(self):
        self.logger.info("Generating random inputs")
        # ad_format_id,network_id,seller_id,site_id,media_size,ad_position,device,os,browser_name,browser_version
        with open(self.get_data_file('json/keys.json')) as data_file:
            inputs = json.load(data_file)

        inputs = OrderedDict(sorted(inputs.items(), key=lambda t: t[0]))

        for s in range(100):
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
