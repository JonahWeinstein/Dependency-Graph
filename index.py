import sys
import argparse
from DependencyGraph import DependencyGraph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('project_root', help = 'root of project directory')
    parser.add_argument('--ignore', dest='ignore', nargs='*', help='list of directories to ignore when building the graph')
    parser.add_argument('--local_imports', dest='local_imports', help='set as true if you only want to graph local imports')
    args = parser.parse_args()
    graph = DependencyGraph(args.project_root, args.ignore, args.local_imports)
    graph.readDirectory()
    graph.getImports()
    graph.buildGraph()


