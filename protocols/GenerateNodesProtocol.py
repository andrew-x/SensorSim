__author__ = 'Andrew'
import os

from random import randint


class GenerateNodesProtocol:

    nodes = []

    def OUT(self):
        '''
        (GenerateNodesProtocol) -> None

        DO NOT MODIFY
        '''
        with open(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] + "//input//NODES.txt", "w") as f:
            [f.write(n) for n in self.nodes]
            f.close()

    def GENERATE(self):
        '''
        (GenerateNodesProtocol) -> None

        Modify nodes such that it will populate according to the right protocol.

        Note: this is the method that will be called so do not alter this method's name and adhere
        to the type contract.
        '''
        # todo: generation code here
        self.OUT()

if __name__ == '__main__':
    GenerateNodesProtocol().GENERATE()