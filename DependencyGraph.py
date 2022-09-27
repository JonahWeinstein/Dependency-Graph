import os


class DependencyGraph:
    def __init__(self, directoryPath):
        self.path = directoryPath

    def readDirectory(self):
        for root, dirs, files in os.walk(self.path, topdown=False):
            for name in files:
                print(os.path.join(root, name))
            for name in dirs:
                print(os.path.join(root, name))





