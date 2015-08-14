__author__ = 'Andrew'
import os

from random import randint
from NodeUtils import *


class GenerateNodesProtocol:

    nodes = []

    def OUT(self):
        '''
        (GenerateNodesProtocol) -> None

        DO NOT MODIFY
        '''

        with open(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] + ("//input//NODES.txt" if os.name == 'nt' else "/input/NODES.txt"), "w") as f:
            [f.write(n) for n in self.nodes]
            f.close()

    def GENERATE(self):
        '''
        (GenerateNodesProtocol) -> None

        Modify nodes such that it will populate according to the right protocol.

        Note: this is the method that will be called so do not alter this method's name and adhere
        to the type contract.
        '''
        with open("//input//SETTINGS.txt" if os.name == 'nt' else "input/SETTINGS.txt") as f:
            settings = f.readlines()
        f.close()

        settings = [x.strip('\n') for x in settings]

        for setting in settings:
            parts = setting.split(':')
            if parts[0] == "X_SIZE":
                X_SIZE = int(parts[1])
            elif parts[0] == "Y_SIZE":
                Y_SIZE = int(parts[1])
            elif parts[0] == "SEED":
                if len(parts[1]) > 0:
                    SEED = parts[1]
                else:
                    SEED = hex(random.randint(0,2**32-1))
            elif parts[0] == "NODES":
                nodenum = int(parts[1])
            elif parts[0] == "RANGE":
                Range = int(parts[1])

        workingnodes = generateNodes(nodenum,SEED,X_SIZE,Y_SIZE)
        workingnodes = dijkstra(nodes,Range,"hop")
        workingnodes = setOuter(nodes)
        self.nodes = formatNodeData(workingnodes)
        
        
        self.OUT()

if __name__ == '__main__':
    GenerateNodesProtocol().GENERATE()
