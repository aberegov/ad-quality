from com.conversant.common.Tree import Tree
from com.conversant.common.Node import Node
from com.conversant.common.SQLShell import SQLShell


class DatabaseTree(Tree):
    def __init__(self, sql):
        super().__init__()
        self.add_node(Node('root'))
        self.sql = sql

    def build(self):
        shell = SQLShell()
        shell.execute(self.sql, {}, self.process_row)

    def process_row(self, row):
        self.build_path(row[:-1], row[-1])
