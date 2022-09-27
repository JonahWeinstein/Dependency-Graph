import sys
from DependencyGraph import DependencyGraph

if __name__ == '__main__':

    graph = DependencyGraph(sys.argv[1])
    graph.readDirectory()



