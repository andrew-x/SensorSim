__author__ = 'Andrew'
from datatypes.Node import Node


class Sink(Node):

    def __init__(self, id, x, y):
        super(Sink, self).__init__(id, x, y)

    def __str__(self):
        return super(Sink, self).__str__()