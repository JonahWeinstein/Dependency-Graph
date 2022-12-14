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
    # directory path is abs path to root of you project, ignore is an array of relative paths (from directory path)
    # of directories that should not be graphed, such as node_modules
    def __init__(self, directory_path, ignore=None, local_imports = False):

        if ignore is None:
            ignore = []
        self.path = directory_path
        self.allFiles = []
        self.nodes = []
        self.ignore = ignore
        self.local_imports = local_imports

    def check_ignore(self, path):

        for ignore in self.ignore:
            if os.path.join(self.path, ignore) in path:
                return True
        return False

    def readDirectory(self):
        print('Reading Project Directory...')
        # look through all files recursively and add their absolute path to all Files array
        for root, dirs, files in os.walk(self.path, topdown=False):

            for name in files:
                # check if this file is in a directory to ignore
                file_path = os.path.join(root, name)
                ignore = self.check_ignore(file_path)
                if not ignore and os.path.splitext(file_path)[-1] == '.js':
                    self.allFiles.append(os.path.join(root, name))



    def extract_import(self, import_line):
        value = import_line.group()
        # search for content between single or double quotes
        name = re.search('(?:\'|\").*(?:\'|\")', value)
        if name:
            return name.group().strip('\'\"')
        
    def __match(self, line):
        # TODO: normalize lines: strip whitespace before regexing
        if line[:2] == '//':
            return
        # look for commonJS require statements
        result = None
        match = re.search("require" + "\('[^']*'\)*", line)
        # extract name of imported file from match
        if match:
            result = self.extract_import(match)
        # look for ES6 import statements
        else:
            match = re.search("import" + ".*", line)
            # extract name of imported file from match
            if match:
                result = self.extract_import(match)
        # if local_imports is set to true, only return local import matches
        if self.local_imports and result and result[0] != '.':
            return None
        return result

    # used to make path of import relative to project root as opposed to being relative to the file that imports it
    # path is the path in the import (ex ../routers/userRouter) and file is the file that imports it
    # (file = importing file, path = imported file)
    def normalize_paths(self, path, file):
        # check if import is a system/third party package
        if path[0] != '.':
            return path
        # otherwise get the path
        else:
            # get directory path of importing file
            file_dir = os.path.dirname(file)
            abs_path = os.path.join(file_dir, path)

            # normalize path with respect to importing file
            norm_path = os.path.normpath(abs_path)
            # get path relative to project root
            final_path = os.path.relpath(norm_path, self.path)
            return final_path

    def getImports(self):
        print('Getting imports...')
        for file in self.allFiles:
            imports = []
            f = open(file, "r")
            lines = f.readlines()
            for line in lines:

                result = self.__match(line)
                if result:
                    final_path = self.normalize_paths(result, file)
                    if final_path:
                        imports.append(final_path)
            # create key value pair with file path as key and imports array as value
            new = Node(os.path.relpath(file, self.path), imports)
            self.nodes.append(new)

    def buildGraph(self):
        print('Building Dependency Graph...')
        # keep track of which nodes have been created
        added_nodes = {}
        dot = graphviz.Digraph(graph_attr={'rankdir':'LR'})
        for node in self.nodes:
            # remove file extension since it won't be in import statements
            node.name = os.path.splitext(node.name)[0]
            if node.name not in added_nodes:
                dot.node(node.name)
                added_nodes[node.name] = "added"
            for w in node.adjacency_list:
                if w not in added_nodes:
                    dot.node(node.name)
                    added_nodes[w] = "added"
                dot.edge(w, node.name)
        dot.render('doctest-output/round-table.gv').replace('\\', '/')











