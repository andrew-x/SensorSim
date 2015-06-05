__author__ = 'Andrew'
from core.Grid import Grid
from datatypes.Energizer import Energizer
from datatypes.Sink import Sink
from datatypes.Relay import Relay
from datatypes.Sensor import Sensor
from datatypes.Packet import Packet
from exceptions.Exceptions import *

import gtk

class Controller():
    '''
    INPUT PROTOCOL:
    SINKS:      I id x y
    ENERGIZERS: E id x y range battery rate
    RELAY:      R id x y range battery energy_use_in energy_use_out parent_id
    SENSOR:     S id x y range battery energy_use_out parent_id

    QUESTIONS:
    - Sensor use up energy when generating packet?
    - Do you need range?
    -
    '''

    SETTINGS_FILENAME = "SETTINGS.txt"
    NODES_FILENAME = "NODES.txt"
    SCHEDULE_FILENAME = "SCHEDULE.txt"

    TYPE_SINK = 'i'
    TYPE_RELAY = 'r'
    TYPE_SENSOR = 's'
    TYPE_ENERGIZER = 'e'

    grid = Grid()
    schedule = []

    nodes = []
    sink = None
    energizers = []
    sensors = []
    relays = []
    packets = []

    packet_count = 0

    dead_nodes = []
    dropped_packets = []

    period_count = 0
    period_limit = -1

    def __init__(self):
        self.load_settings()
        self.load_nodes()
        self.load_schedule()

        self.period_limit = 2 # int(input('How many periods to run? '))
        self.period_count = 0
        self.run()

    def run(self):
        self.init_run()
        while self.period_count < self.period_limit:
            self.dead_nodes = []

            self.energize()
            self.generate_packets()
            print(self.done_schedule())
            while self.done_schedule() is False:
                self.run_schedule()
            self.collect_energy()
            self.period_count += 1

            for p in self.packets:
                print(str(p) + ' ',)
            print('\n')

    def init_run(self):
        self.packets = []
        self.period_count = 0
        self.packet_count = 0
        self.dead_nodes = []

    def done_schedule(self):
        for p in self.packets:
            if p.get_delivered() is False and p.get_current() not in self.dead_nodes:
                return False
        return True

    def energize(self):
        for e in self.energizers:
            e.energize()

    def collect_energy(self):
        for e in self.energizers:
            e.gather_energy()

    def generate_packets(self):
        for s in self.sensors:
            if s.generate_packet(self.packet_count):
                self.packets += [Packet(str(self.packet_count), s.get_id())]
                self.packet_count += 1

    def run_schedule(self):
        for slot in self.schedule:
            for node in slot:
                if node.get_id() not in self.dead_nodes:
                    packet_id = ''
                    parent_id = ''
                    try:
                        packet_id, parent_id = node.send()
                        node.increment_lifetime()
                    except NotEnoughEnergyException:
                        self.dead_nodes += [node.get_id()]
                        node.increment_lost_count()
                        continue
                    if packet_id is None:
                        continue
                    if parent_id[0] == self.TYPE_SINK:
                        self.packets[self.find_packet(packet_id)].set_delivered()
                    else:
                        try:
                            self.relays[self.find_relay(parent_id)].receive(packet_id)
                            self.packets[self.find_packet(packet_id)].set_current(parent_id)
                        except NotEnoughEnergyException:
                            node.increment_lost_count()
                            self.dead_nodes += [parent_id]


    def find_relay(self, target):
        for i in range(0, len(self.relays)):
            if self.relays[i].get_id() == target:
                return i
        return -1

    def find_packet(self, target):
        for i in range(0, len(self.packets)):
            if self.packets[i].get_id() == target:
                return i
        return -1

    def find_sensor(self, target):
        for i in range(0, len(self.sensors)):
            if self.sensors[i].get_id() == target:
                return i
        return -1

    def load_settings(self):
        x_size = -1
        y_size = -1
        seed = -1
        with open(self.SETTINGS_FILENAME) as f:
            content = f.readlines()
        for l in content:
            l = l.strip()
            if 'X_SIZE' in l:
                x_size = int(l[l.index(':') + 1:])
            elif 'Y_SIZE' in l:
                y_size = int(l[l.index(':') + 1:])
            elif 'SEED' in l:
                seed = int(l[l.index(':') + 1:])
        if x_size is not -1 and y_size is not -1 and seed is not -1:
            self.grid = Grid(x_size, y_size)
        else:
            print('IMPROPER SETTINGS FILE')

    def load_nodes(self):
        with open(self.NODES_FILENAME) as f:
            content = f.readlines()
        try:
            for l in content:
                arr = l.split()
                if arr[0] is 'I':
                    self.sink = Sink(arr[1], int(arr[2]), int(arr[3]))
                elif arr[0] is 'E':
                    self.energizers += [
                        Energizer(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]))]
                elif arr[0] is 'R':
                    self.relays += [
                        Relay(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]), int(arr[7]),
                              arr[8])]
                elif arr[0] is 'S':
                    self.sensors += [
                        Sensor(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]),
                               arr[7])]
        except IndexError:
            print("INVALID NODES FILE")

    def load_schedule(self):
        with open(self.SCHEDULE_FILENAME) as f:
            content = f.readlines()
        for l in content:
            arr = l.split()
            slot = []
            for a in arr:
                if a[0] == self.TYPE_RELAY:
                    slot += [self.relays[self.find_relay(a)]]
                elif a[0] == self.TYPE_SENSOR:
                    slot += [self.sensors[self.find_sensor(a)]]
            self.schedule += [slot]

if __name__ == '__main__':
    control = Controller()
