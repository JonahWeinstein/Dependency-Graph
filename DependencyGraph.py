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
        return re.search("require" + "\('[^']*'\);*\\n", line)

    def normalize_paths(self, path, file):

        # check if import is a system/third party package
        if path[0] != '.':
            return path
        # otherwise get the path
        else:
            # get file directory path (for path normalization)
            file_dir = os.path.dirname(file)
            abs_path = os.path.join(file_dir, path)
            # normalize path with respect to importing file
            norm_path = os.path.normpath(abs_path)
            final_path = os.path.relpath(norm_path, self.path)
            return final_path

    def getImports(self):
        for file in self.allFiles:
            imports = []
            f = open(file, "r")
            lines = f.readlines()
            for line in lines:

                result = self.__match(line)
                if result:
                    value = result.group()[:-1]
                    # using ; char to terminate statements is optional in js
                    if value[-1:] == ';':
                        value = value[:-1]
                        print(value)
                    # get import name by cutting away require keyword
                    import_name = value[9:-2]
                    final_path = self.normalize_paths(import_name, file)
                    # trim require and parentheses and add import name to this files imports
                    imports.append(final_path)
            # create key value pair with file path as key and imports array as value
            new = Node(os.path.relpath(file, self.path), imports)
            self.nodes.append(new)

    def buildGraph(self):
        # keep track of which nodes have been created
        added_nodes = {}
        dot = graphviz.Digraph(graph_attr={'rankdir':'LR'})
        for node in self.nodes:
            node.name = node.name[:-3]
            if node.name not in added_nodes:
                dot.node(node.name)
                added_nodes[node.name] = "added"
            for w in node.adjacency_list:
                if w not in added_nodes:
                    dot.node(node.name)
                    added_nodes[w] = "added"
                dot.edge(w, node.name)
        # print(dot.source)
        dot.render('doctest-output/round-table.gv').replace('\\', '/')











