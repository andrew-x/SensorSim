__author__ = 'Andrew'
from core.Grid import Grid
from core.Inventory import Inventory
from datatypes.Energizer import Energizer
from datatypes.Sink import Sink
from datatypes.Relay import Relay
from datatypes.Sensor import Sensor
from datatypes.Packet import Packet
from exceptions.Exceptions import *
from decimal import Decimal


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

    packet_count = 0

    dead_nodes = []
    dropped_packets = []

    period_count = 0
    period_limit = -1

    scheduled = []
    period_initialized = False
    schedule_index = 0

    def __init__(self):
        self.load_settings()
        self.load_nodes()
        self.load_schedule()

        Inventory.SCHEDULED = Inventory.SCHEDULE[0]
        Inventory.PACKETS = []
        self.period_count = 0
        self.packet_count = 0
        self.dead_nodes = []

        self.period_count = 0
        self.period_initialized = False
        self.schedule_index = 0
        self.scheduled = Inventory.SCHEDULE[self.schedule_index]

    def fire(self):
        self.period_initialized = False
        self.schedule_index = 0
        self.scheduled = Inventory.SCHEDULE[self.schedule_index]
        while True:
            try:
                self.step_through()
            except DoneScheduleException:
                break

    def step_through(self):
        if not self.period_initialized:
            self.dead_nodes = []
            self.energize()
            self.generate_packets()
            self.period_initialized = True
        if not self.done_schedule():
            self.run_slot()
            self.schedule_index += 1
            if self.schedule_index >= len(Inventory.SCHEDULE):
                self.schedule_index = 0
            self.scheduled = Inventory.SCHEDULE[self.schedule_index]
        if self.done_schedule():
            self.collect_energy()
            self.period_count += 1
            self.period_initialized = False
            self.schedule_index = 0
            self.scheduled = Inventory.SCHEDULE[self.schedule_index]
            raise DoneScheduleException

    def done_schedule(self):
        for p in Inventory.PACKETS:
            if p.get_delivered() is False and p.get_current() not in self.dead_nodes:
                return False
        return True

    def energize(self):
        # TODO: make this better.
        for e in Inventory.ENERGIZERS:
            e.energize()

    def collect_energy(self):
        for e in Inventory.ENERGIZERS:
            e.gather_energy()

    def generate_packets(self):
        for s in Inventory.SENSORS:
            packet_id = "p" + str(self.packet_count+1)
            if s.generate_packet(packet_id):
                Inventory.PACKETS += [Packet(packet_id, s.get_id())]
                self.packet_count += 1

    def run_slot(self):
        slot = self.scheduled
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
                if parent_id[0] == Inventory.TYPE_SINK:
                    Inventory.PACKETS[self.find_packet(packet_id)].set_delivered()
                    Inventory.PACKETS[self.find_packet(packet_id)].set_current(parent_id)
                else:
                    try:
                        Inventory.RELAYS[self.find_relay(parent_id)].receive(packet_id)
                        Inventory.PACKETS[self.find_packet(packet_id)].set_current(parent_id)
                    except NotEnoughEnergyException:
                        node.increment_lost_count()
                        self.dead_nodes += [parent_id]

    def find_relay(self, target):
        for i in range(0, len(Inventory.RELAYS)):
            if Inventory.RELAYS[i].get_id() == target:
                return i
        return -1

    def find_packet(self, target):
        for i in range(0, len(Inventory.PACKETS)):
            if Inventory.PACKETS[i].get_id() == target:
                return i
        return -1

    def find_sensor(self, target):
        for i in range(0, len(Inventory.SENSORS)):
            if Inventory.SENSORS[i].get_id() == target:
                return i
        return -1

    # INITIALIZE METHODS

    def load_settings(self):
        x_size = -1
        y_size = -1
        seed = -1
        refresh_delay = -1
        with open(Inventory.SETTINGS_FILENAME) as f:
            content = f.readlines()
        for l in content:
            l = l.strip()
            val = Decimal(l[l.index(':') + 1:])
            if 'X_SIZE' in l:
                x_size = val
            elif 'Y_SIZE' in l:
                y_size = val
            elif 'SEED' in l:
                seed = val
            elif 'REFRESH_DELAY' in l:
                refresh_delay = val
        if x_size is not -1 and y_size is not -1 and seed is not -1 and refresh_delay is not -1:
            Inventory.SEED = seed
            Inventory.REFRESH_DELAY = refresh_delay
            Inventory.X_SIZE = x_size
            Inventory.Y_SIZE = y_size
        else:
            print('IMPROPER SETTINGS FILE')

    def load_nodes(self):
        with open(Inventory.NODES_FILENAME) as f:
            content = f.readlines()
        try:
            for l in content:
                arr = l.split()
                if arr[0] is 'I':
                    Inventory.SINK = Sink(arr[1], int(arr[2]), int(arr[3]))
                elif arr[0] is 'E':
                    Inventory.ENERGIZERS += [
                        Energizer(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]))]
                elif arr[0] is 'R':
                    Inventory.RELAYS += [
                        Relay(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]), int(arr[7]),
                              arr[8])]
                elif arr[0] is 'S':
                    Inventory.SENSORS += [
                        Sensor(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]),
                               arr[7])]
        except IndexError:
            print("INVALID NODES FILE")

    def load_schedule(self):
        with open(Inventory.SCHEDULE_FILENAME) as f:
            content = f.readlines()
        for l in content:
            arr = l.split()
            slot = []
            for a in arr:
                if a[0] == Inventory.TYPE_RELAY:
                    slot += [Inventory.RELAYS[self.find_relay(a)]]
                elif a[0] == Inventory.TYPE_SENSOR:
                    slot += [Inventory.SENSORS[self.find_sensor(a)]]
            Inventory.SCHEDULE += [slot]

    # SETTERS AND GETTERS

    def get_scheduled(self):
        return self.scheduled

    def get_period_count(self):
        return self.period_count

    @staticmethod
    def set_energizers(energizers):
        Inventory.ENERGIZERS = energizers

    @staticmethod
    def set_relays(relays):
        Inventory.RELAYS = relays

    @staticmethod
    def set_sensors(sensors):
        Inventory.SENSORS = sensors

    @staticmethod
    def set_sink(sink):
        Inventory.SINK = sink

    @staticmethod
    def get_energizers():
        return Inventory.ENERGIZERS

    @staticmethod
    def get_relays():
        return Inventory.RELAYS

    @staticmethod
    def get_sensors():
        return Inventory.SENSORS

    @staticmethod
    def get_sink():
        return Inventory.SINK

    @staticmethod
    def get_packets():
        return Inventory.PACKETS