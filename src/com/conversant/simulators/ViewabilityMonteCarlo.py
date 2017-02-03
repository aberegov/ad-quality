from random import randint
from collections import OrderedDict
import json
import networkx as nx
import os
import matplotlib.pyplot as plt
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

    def draw_tree(self):
        G = nx.DiGraph()
        self.draw_tree_iter(G, self.predictor.root_node())
        nx.shell_layout(G)
        nx.write_gml(G,  os.path.normpath(os.path.join(os.path.expanduser("~"), 'mk_tree.gml')), self.gml_stringizer)

    def draw_tree_iter(self, G, node, count=0):
        count = count + 1
        G.add_node(node)
        node.level = count
        for child_name, child_nid in node.children.items():
            child = self.predictor[child_nid]
            count = self.draw_tree_iter(G, child, count)
            G.add_edge(node, child)
        return count

    def gml_stringizer(self,node):
        return "%d:%s" % (node.level, node.name)

if __name__ == '__main__':
    validator = ViewabilityMonteCarlo()
    validator.generate()
    validator.output()
    validator.draw_tree()
