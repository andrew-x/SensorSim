__author__ = 'Andrew'
from exceptions.Exceptions import *
from datatypes.Node import Node


class Sensor(Node):
    range = -1
    battery = -1
    e_use_out = -1
    parent = None
    packet = ''

    lost_count = 0

    def __init__(self, id, x, y, range, battery, e_use_out, parent):
        super(Sensor, self).__init__(id, x, y)

        self.id = id
        self.x = x
        self.y = y
        self.range = range
        self.battery = battery
        self.e_use_out = e_use_out
        self.parent = parent
        self.packets = []

        self.lost_count = 0

    def generate_packet(self, packet_id):
        # QUESTION: DOES THIS USE UP ENERGY?
        self.packets += [packet_id]
        return True

    def send(self):
        if self.battery < self.e_use_out:
            raise NotEnoughEnergyException

        self.battery -= self.e_use_out
        if len(self.packets) > 0:
            return self.packets.pop(0), self.parent
        return None, self.parent

    def increment_lost_count(self):
        self.lost_count += 1

    def __str__(self):
        return super(Sensor, self).__str__() + " | range: " + str(self.range) + " | battery: " + str(
            self.battery) + " | e_use_in: " + str(
            self.e_use_out) + " | parent: " + self.parent

    # GETTERS AND SETTERS

    def get_range(self):
        return self.range

    def get_battery(self):
        return self.battery

    def get_e_use_out(self):
        return self.e_use_out

    def get_parent(self):
        return self.parent

    def get_packets(self):
        return self.packets