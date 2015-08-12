__author__ = 'Andrew'
from exceptions.Exceptions import *
from datatypes.Node import Node
from core.Inventory import *


class Relay(Node):
    range = -1
    battery = -1
    e_use_in = -1
    e_use_out = -1
    parent = None
    packets = []

    battery_max = -1

    send_count = 0
    receive_count = 0
    send_lost_count = 0
    receive_lost_count = 0
    send_success_rate = 0
    receive_success_rate = 0

    energy_count = 0
    energy_count_count = 0
    energy_average = 0

    def __init__(self, id, x, y, relay_range, battery, e_use_in, e_use_out, parent):
        super(Relay, self).__init__(id, x, y)

        self.range = relay_range
        self.battery = battery
        self.battery_max = battery
        self.e_use_in = e_use_in
        self.e_use_out = e_use_out
        self.parent = parent
        self.packets = []

        self.send_count = 0
        self.receive_count = 0
        self.send_lost_count = 0
        self.receive_lost_count = 0
        self.send_success_rate = 100
        self.receive_success_rate = 100

    def receive(self, packet):
        """
        (Relay, string) -> None

        Takes in the input packet and adds to packet que
        Raises NotEnoughEnergyException if this relay does not have the
        amount of energy needed.
        """
        self.receive_count += 1
        if self.battery < self.e_use_in:
            self.battery = 0
            raise NotEnoughEnergyException

        self.battery -= self.e_use_in
        self.packets += [packet]

    def send(self):
        """
        (Relay) -> string

        Sends the packet at the top of the que
        Raises NotEnoughEnergyException if this relay does not have the
        amount of energy needed.
        """
        if len(self.packets) > 0:
            packet = self.packets.pop(0)
            try:
                if self.battery < self.e_use_out:
                    Inventory.find_packet(packet).set_lost()
                    self.battery = 0
                    raise NotEnoughEnergyException
                else:
                    self.battery -= self.e_use_out
            finally:
                self.send_count += 1
                return packet, self.parent
        else:
            raise EmptyQueueException

    def recharge(self, recharge_amount):
        if self.battery + recharge_amount > self.battery_max:
            self.battery = self.battery_max
        else:
            self.battery += recharge_amount

    def increment_send_lost_count(self):
        self.send_lost_count += 1
        self.send_success_rate = (self.send_count - self.send_lost_count) / self.send_count * 100

    def increment_receive_lost_count(self):
        self.receive_lost_count += 1
        self.receive_success_rate = (self.receive_count - self.receive_lost_count) / self.receive_count * 100

    def increment_energy_count(self):
        self.energy_count += self.battery
        self.energy_count_count += 1
        self.energy_average = self.energy_count / self.energy_count_count

    def __str__(self):
        return super(Relay, self).__str__() + " | range: " + str(self.range) + " | battery: " + str(
            self.battery) + " | e_use_in: " + str(self.e_use_in) + " | e_use_out: " + str(self.e_use_out) + \
            " | parent: " + self.parent + ' | send_count: ' + str(self.send_count) + ' | send_lost_count: ' +\
            str(self.send_lost_count) + ' | receive_count: ' + str(self.receive_count) + ' | receive_lost_count: ' +\
            str(self.receive_lost_count) + ' | send_success_rate: ' + str(self.send_success_rate) + \
            ' | receive_send_success_rate: ' + str(self.receive_success_rate) + ' | energy_average: ' + \
            str(self.energy_average)

    # GETTERS AND SETTERS

    def get_range(self):
        return self.range

    def get_battery(self):
        return self.battery

    def get_e_use_in(self):
        return self.e_use_in

    def get_e_use_out(self):
        return self.e_use_out

    def get_parent(self):
        return self.parent

    def get_packets(self):
        return self.packets

    def get_send_lost_count(self):
        return self.send_lost_count

    def get_receive_lost_count(self):
        return self.receive_lost_count

    def get_send_count(self):
        return self.send_count

    def get_receive_count(self):
        return self.receive_count

    def get_send_success_rate(self):
        return self.send_success_rate

    def get_receive_success_rate(self):
        return self.receive_success_rate

    def get_energy_average(self):
        return self.energy_average

    def get_to_send(self):
        return self.packets[-1]