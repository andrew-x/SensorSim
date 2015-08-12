__author__ = 'Andrew'
from datatypes.Node import Node
import math, random


class Energizer(Node):
    range = -1
    battery = -1
    battery_max = -1
    gather_rate = -1
    recharge_rate = -1

    def __init__(self, energizer_id, x, y, energizer_range, battery, gather_rate, recharge_rate):
        super(Energizer, self).__init__(energizer_id, x, y)
        self.range = energizer_range
        self.battery = battery
        self.battery_max = battery
        self.gather_rate = gather_rate
        self.recharge_rate = recharge_rate

    def gather_energy(self, seed):
        """
        None -> Decimal

        Gathers energy, returns the energy gained.
        """
        random.seed(seed)
        gather_amount = self.gather_rate * random.random()
        if self.battery + gather_amount > self.battery_max:
            try:
                return self.battery_max - self.battery_max
            finally:
                self.battery = self.battery_max
        else:
            self.battery += gather_amount
            return gather_amount

    def energize(self, dist):
        """
        None -> Decimal

        Returns the amount of energy to charge
        """
        # TODO: improve, questions
        if dist > self.range:
            return 0
        try:
            return dist / self.range * self.recharge_rate
        finally:
            self.battery = 0

    def __str__(self):
        return super(Energizer, self).__str__() + " | range: " + str(self.range) + " | battery: " + str(
            self.battery) + " | gather_rate: " + str(self.gather_rate) + ' | recharge_rate: ' + str(self.recharge_rate)

    # GETTERS AND SETTERS

    def get_battery(self):
        return self.battery

    def get_gather_rate(self):
        return self.gather_rate

    def get_recharge_rate(self):
        return self.recharge_rate

    def get_range(self):
        return self.range