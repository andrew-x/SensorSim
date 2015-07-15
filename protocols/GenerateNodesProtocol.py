__author__ = 'Andrew'
import os

from random import randint

class GenerateNodesProtocol:

    nodes = []

    def GENERATE(self):
        '''
        (GenerateNodesProtocol) -> None

        Set Inventory.SENSORS, Inventory.SINKS, Inventory.RELAYS, Inventory.ENERGIZERS

        Note: this is the method that will be called so do not alter this method's name and adhere
        to the type contract.
        '''
        for i in range(50):
            x = randint(1, 99)
            y = randint(2, 99)
            self.nodes += [['i'+str(i+1), x, y]]

    def OUT(self):
        with open(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] + "//NODES.txt", "w") as f:
            for n in self.nodes:
                f.write(n)
            f.close()


if __name__ == '__main__':
    GenerateNodesProtocol().GENERATE()