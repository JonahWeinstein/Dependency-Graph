import os
import re
import graphviz


class Node:
    def __init__(self, name, adjacency_list):
        self.name = name
        self.adjacency_list = adjacency_list


# creates dependency graph for given project file, currently only supports nodejs projects using
# commonJS imports
class DependencyGraph:
    def __init__(self, directory_path):
        self.path = directory_path
        self.allFiles = []
        self.nodes = []

    def readDirectory(self):
        # look through all files recursively and add their absolute path to all Files array
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                self.allFiles.append(os.path.join(root, name))

    def __match(self, line):
        return re.search("require" + "\('[^']*'\)\\n", line)

    def getImports(self):
        for file in self.allFiles:
            imports = []
            f = open(file, "r")
            lines = f.readlines()
            for line in lines:

                result = self.__match(line)
                if result:

                    relative_path = result.group()[9:-3]
                    if relative_path[0] != '.':
                        imports.append(relative_path)
                    else:
                        abs_path = os.path.join(self.path, relative_path)
                        final_path = os.path.normpath(abs_path)
                        # trim require and parentheses and add import name to this files imports
                        imports.append(final_path)
            # create key value pair with file path as key and imports array as value
            new = Node(file, imports)
            self.nodes.append(new)


    def buildGraph(self):
        dot = graphviz.Digraph(graph_attr={'rankdir':'LR'})
        for node in self.nodes:
            dot.node(node.name)
            for w in node.adjacency_list:
                dot.edge(node.name, w)
        # print(dot.source)
        dot.render('doctest-output/round-table.gv').replace('\\', '/')











