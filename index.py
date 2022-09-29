import sys
import argparse
from DependencyGraph import DependencyGraph

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('root', help = 'root of project directory')
    parser.add_argument('--ignore', dest='ignore', nargs='*', help='list of directories to ignore when building the graph')
    args = parser.parse_args()
    graph = DependencyGraph(args.root, args.ignore)
    graph.readDirectory()
    graph.getImports()
    graph.buildGraph()


