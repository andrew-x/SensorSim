__author__ = 'Andrew'
from exceptions.Exceptions import *
from datatypes.Node import Node


class Sensor(Node):
    range = -1
    battery = -1
    e_use_out = -1
    parent = None
    packet = ''

    energy_count = 0
    energy_count_count = 0

    send_count = 0
    send_lost_count = 0

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
        """
        (Sensor, string) -> None

        Generates a packet
        """
        # TODO: Add energy loss.
        self.packets += [packet_id]
        return True

    def send(self):
        """
        (Sensor) -> None

        Sends the packet at the top of the que.
        Raises NotEnoughEnergyException if it does not have
        the energy required.
        """
        if self.battery < self.e_use_out:
            raise NotEnoughEnergyException
        self.battery -= self.e_use_out
        if len(self.packets) > 0:
            self.send_count += 1
            return self.packets.pop(0), self.parent
        else:
            raise EmptyQueueException

    def increment_send_lost_count(self):
        self.send_lost_count += 1

    def increment_energy_count(self):
        self.energy_count += self.battery
        self.energy_count_count += 1

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

    def get_send_lost_count(self):
        return self.send_lost_count

    def get_send_count(self):
        return self.send_count