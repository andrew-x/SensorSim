__author__ = 'Andrew'
from datatypes.Node import Node


class Energizer(Node):
    range = -1
    battery = -1
    rate = -1

    def __init__(self, id, x, y, range, battery, rate):
        super(Energizer, self).__init__(id, x, y)
        self.range = range
        self.battery = battery
        self.rate = rate

    def gather_energy(self):
        self.battery += self.rate  # TODO: Augment with time

    def energize(self):
        try:
            return self.battery
        finally:
            self.battery = 0

    def __str__(self):
        return super(Energizer, self).__str__() + " | range: " + str(self.range) + " | battery: " + str(
            self.battery) + " | rate: " + str(self.rate)

    # GETTERS AND SETTERS

    def get_rate(self):
        return self.rate

    def get_range(self):
        return self.range