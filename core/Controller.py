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
import csv


class Controller():
    """
    The controller in this semi MVC design.
    Contains all methods to do with the actual running
    of the simulation.
    """

    packet_count = 0

    dead_nodes = []
    dropped_packets = []

    schedule_run_count = 0
    period_count = 0
    period_limit = -1

    scheduled = []
    period_initialized = False
    schedule_index = 0

    def __init__(self):
        """
        (Controller) -> None

        Constructor
        """
        Inventory.load_settings()
        Inventory.load_nodes()
        Inventory.load_schedule()

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
        """
        (Controller) -> None

        Runs a period
        """
        if self.schedule_index is 0:
            self.period_initialized = False
            self.schedule_index = 0
            self.scheduled = Inventory.SCHEDULE[self.schedule_index]
            while True:
                try:
                    self.step_through()
                except DoneScheduleException:
                    break
        else:
            for i in range(self.schedule_index, len(Inventory.SCHEDULE)):
                self.step_through()
            self.fire()

    def step_through(self):
        """
        (Controller) -> None

        Runs scheduled slot
        """
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
        """
        (Controller) -> None

        Checks if the schedule is done. As in, all packets that can be delivered this time has been delivered.
        """
        for p in Inventory.PACKETS:
            if p.get_delivered() is False and p.get_current() not in self.dead_nodes and p.get_lost() is False:
                return False
        return True

    def energize(self):
        """
        (Controller) -> None

        Energizes all nodes
        """
        # TODO: improve.
        for e in Inventory.ENERGIZERS:
            e.energize()

    def collect_energy(self):
        """
        (Controller) -> None

        Recharge energizers
        """
        # TODO: improve.
        for e in Inventory.ENERGIZERS:
            e.gather_energy()

    def generate_packets(self):
        """
        (Controller) -> None

        Generates packets from sensors.
        """
        # TODO: improve.
        for s in Inventory.SENSORS:
            packet_id = "p" + str(self.packet_count+1)
            if s.generate_packet(packet_id):
                Inventory.PACKETS += [Packet(packet_id, s.get_id())]
                self.packet_count += 1

    def run_slot(self):
        """
        (Controller) -> None

        Runs scheduled slot.
        """
        # TODO: Make more efficient
        slot = self.scheduled

        Inventory.FAILED_LINKS = []
        Inventory.SUCCESSFUL_LINKS = []

        self.schedule_run_count += 1
        for node in slot:
            node.increment_energy_count()
            if node.get_id() not in self.dead_nodes:
                packet_id = ''
                parent_id = ''
                #Send
                try:
                    packet_id, parent_id = node.send()
                    node.increment_lifetime()
                except NotEnoughEnergyException:
                    self.dead_nodes += [node.get_id()]
                    Inventory.FAILED_LINKS += [node]

                    node.increment_send_lost_count()
                    continue
                except EmptyQueueException:
                    continue

                #Receive
                if parent_id[0] == Inventory.TYPE_SINK:
                    Inventory.PACKETS[Inventory.find_packet(packet_id)].set_delivered()
                    Inventory.PACKETS[Inventory.find_packet(packet_id)].set_current(parent_id)
                    Inventory.PACKETS[Inventory.find_packet(packet_id)].increment_hop_count()

                    Inventory.SUCCESSFUL_LINKS += [node]
                else:
                    try:
                        Inventory.RELAYS[Inventory.find_relay(parent_id)].receive(packet_id)
                        Inventory.PACKETS[Inventory.find_packet(packet_id)].set_current(parent_id)
                        Inventory.PACKETS[Inventory.find_packet(packet_id)].increment_hop_count()

                        Inventory.SUCCESSFUL_LINKS += [node]
                    except NotEnoughEnergyException:
                        self.dead_nodes += [parent_id]
                        Inventory.FAILED_LINKS += [node]

                        Inventory.RELAYS[Inventory.find_relay(parent_id)].increment_receive_lost_count()
                        Inventory.PACKETS[Inventory.find_packet(packet_id)].set_lost()

    def export_data(self):
        """
        (Controller) -> None

        Exports data to csv files.
        """
        print('Export')
        data = []
        data += [['Id', 'Origin', 'Current', 'Delivered', 'Lost', 'Lost at', 'Hop Count']]
        for p in Inventory.PACKETS:
            data += [[p.get_id(), p.get_origin(), p.get_current(), str(p.get_delivered()),
                      str(p.get_lost()), p.get_lost_at(), str(p.get_hop_count())]]

        with open(Inventory.EXPORT_ROOT + 'packets.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y', 'Range', 'Battery', 'Rate']]
        for e in Inventory.ENERGIZERS:
            data += [[e.get_id(), e.get_x(), e.get_y(), e.get_range(), e.get_battery(), e.get_rate()]]
        with open(Inventory.EXPORT_ROOT + 'energizers.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use in', 'Energy use out', 'Parent',
                  'Send tries', 'Send fails', 'Send success rate', 'Receive tries', 'Receive fails',
                  'Receive success rate', 'Battery average']]
        for r in Inventory.RELAYS:
            data += [[r.get_id(), r.get_x(), r.get_y(), r.get_battery(), r.get_e_use_in(), r.get_e_use_out(),
                      r.get_parent(), r.get_send_count(), r.get_send_lost_count(), r.get_send_success_rate(),
                      r.get_receive_count(), r.get_receive_lost_count(), r.get_receive_success_rate(),
                      r.get_energy_average()]]
        with open(Inventory.EXPORT_ROOT + 'relays.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use out', 'Parent', 'Send tries', 'Send fails',
                  'Send success rate', 'Battery average']]
        for s in Inventory.SENSORS:
            data += [[s.get_id(), s.get_x(), s.get_y(), s.get_range(), s.get_battery(), s.get_parent(),
                      s.get_send_count(), s.get_send_lost_count(), s.get_send_success_rate(), s.get_energy_average()]]
        with open(Inventory.EXPORT_ROOT + 'sensors.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y']]
        for s in Inventory.SINKS:
            data += [[s.get_id(), s.get_x(), s.get_y()]]
        with open(Inventory.EXPORT_ROOT + 'sensors.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Average Period Length']]
        avg_period_length = self.schedule_run_count / self.period_count
        data += [[avg_period_length]]
        with open(Inventory.EXPORT_ROOT + 'simulation.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

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
    def set_sinks(sinks):
        Inventory.SINKS = sinks

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
    def get_sinks():
        return Inventory.SINKS

    @staticmethod
    def get_packets():
        return Inventory.PACKETS