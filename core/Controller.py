__author__ = 'Andrew'
from core.Grid import Grid
from core.Inventory import Inventory
from datatypes.Energizer import Energizer
from datatypes.Sink import Sink
from datatypes.Relay import Relay
from datatypes.Sensor import Sensor
from datatypes.Packet import Packet
from exceptions.Exceptions import *
from core.Debug import *
from core.Audit import *
from decimal import Decimal
import csv, math, random


class Controller():
    """
    The controller in this semi MVC design.
    Contains all methods to do with the actual running
    of the simulation.
    """

    packet_count = 0

    dead_nodes = []
    dropped_packets = []

    period_limit = -1

    scheduled = []
    period_initialized = False

    def __init__(self):
        """
        (Controller) -> None

        Constructor
        """
        Inventory.load_settings()
        Inventory.load_nodes()
        Inventory.load_schedule()

        Audit.set_up()

        Inventory.SCHEDULED = Inventory.SCHEDULE[0]
        Inventory.PACKETS = []
        Inventory.PERIOD_COUNT = 0

        self.packet_count = 0
        self.dead_nodes = []
        self.period_initialized = False
        self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
        self.schedule_run_count = 0

    def fire(self):
        """
        (Controller) -> None

        Runs a period
        """
        if Inventory.SCHEDULE_INDEX is 0:
            self.period_initialized = False
            Inventory.SCHEDULE_INDEX = 0
            self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
            while True:
                try:
                    self.step_through()
                except DoneScheduleException:
                    break
        else:
            for i in range(Inventory.SCHEDULE_INDEX, len(Inventory.SCHEDULE)):
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
            Inventory.SCHEDULE_INDEX += 1
            if Inventory.SCHEDULE_INDEX >= len(Inventory.SCHEDULE):
                Inventory.SCHEDULE_INDEX = 0
            self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
        if self.done_schedule():
            self.collect_energy()
            Inventory.PERIOD_COUNT += 1
            self.period_initialized = False
            Inventory.SCHEDULE_INDEX = 0
            self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
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
        for e in Inventory.ENERGIZERS:
            for r in Inventory.RELAYS:
                dist = math.sqrt(abs(r.get_x() - e.get_x()) ** 2 + abs(r.get_x() - e.get_y()) ** 2)
                to_charge = e.energize(dist)
                r.recharge(to_charge)
                Audit.audit_recharge(r.get_id(), e.get_id(), to_charge, dist)
            for s in Inventory.SENSORS:
                dist = math.sqrt(abs(s.get_x() - e.get_x()) ** 2 + abs(s.get_x() - e.get_y()) ** 2)
                to_charge = e.energize(dist)
                s.recharge(to_charge)
                Audit.audit_recharge(s.get_id(), e.get_id(), to_charge, dist)

    def collect_energy(self):
        """
        (Controller) -> None

        Recharge energizers
        """
        for e in Inventory.ENERGIZERS:
            gather_amount = e.gather_energy(Inventory.SEED)
            Audit.audit_energy_gather(e.get_id(), gather_amount, e.get_battery())

    def generate_packets(self):
        """
        (Controller) -> None

        Generates packets from sensors.
        """
        for s in Inventory.SENSORS:
            packet_id = "p" + str(self.packet_count+1)
            try:
                if s.generate_packet(packet_id):
                    Inventory.PACKETS += [Packet(packet_id, s.get_id())]
                    self.packet_count += 1
            except NotEnoughEnergyException:
                continue

    def run_slot(self):
        """
        (Controller) -> None

        Runs scheduled slot.
        """
        slot = self.scheduled

        Inventory.FAILED_LINKS = []
        Inventory.SUCCESSFUL_LINKS = []

        self.schedule_run_count += 1
        for sender_id in slot:
            sender = Inventory.find_node(sender_id)
            sender.increment_energy_count()
            if sender.get_id() not in self.dead_nodes:
                packet_id = ''
                parent_id = ''
                #Send
                try:
                    packet_id, parent_id = sender.send()
                    sender.increment_lifetime()
                except EmptyQueueException:
                    continue
                except NotEnoughEnergyException:
                    self.dead_nodes += [sender_id]
                    Inventory.FAILED_LINKS += [sender_id]
                    sender.increment_send_lost_count()
                    try:
                        Audit.audit_send_fail(sender_id, sender.get_battery(),
                            sender.get_e_use_out(), sender.get_to_send())
                    except EmptyQueueException:
                        Audit.audit_send_fail(sender_id, sender.get_battery(),
                            sender.get_e_use_out())
                    continue

                #Hand Off
                receiver = Inventory.find_node(parent_id)
                packet = Inventory.find_packet(packet_id)

                #Receive
                if parent_id[0] == Inventory.TYPE_SINK:
                    packet.set_delivered()
                    packet.set_current(parent_id)
                    packet.increment_hop_count()

                    Audit.audit_transmission(packet_id, sender_id, parent_id)

                    Inventory.SUCCESSFUL_LINKS += [sender_id]
                else:
                    try:
                        receiver.receive(packet_id)
                        packet.set_current(parent_id)
                        packet.increment_hop_count()

                        Audit.audit_transmission(packet_id, sender_id, parent_id)

                        Inventory.SUCCESSFUL_LINKS += [sender_id]
                    except NotEnoughEnergyException:
                        self.dead_nodes += [parent_id]
                        Inventory.FAILED_LINKS += [sender_id]

                        Audit.audit_receive_fail(parent_id, receiver.get_battery(),
                                                 receiver.get_e_use_in(), packet_id)

                        receiver.increment_receive_lost_count()
                        packet.set_lost()

    def export_data(self):
        """
        (Controller) -> None

        Exports data to csv files.
        """
        if Inventory.PERIOD_COUNT <= 0:
            raise NullPeriodException

        data = []
        data += [['Id', 'Origin', 'Current', 'Delivered', 'Lost', 'Lost at', 'Hop Count']]
        for p in Inventory.PACKETS:
            data += [[p.get_id(), p.get_origin(), p.get_current(), str(p.get_delivered()),
                      str(p.get_lost()), p.get_lost_at(), str(p.get_hop_count())]]

        with open(Inventory.EXPORT_ROOT + 'packets.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y', 'Range', 'Battery', 'Gather Rate', 'Recharge Rate']]
        for e in Inventory.ENERGIZERS:
            data += [[e.get_id(), e.get_x(), e.get_y(), e.get_range(), Inventory.f_str(e.get_battery()),
                      e.get_gather_rate(), e.get_recharge_rate()]]
        with open(Inventory.EXPORT_ROOT + 'energizers.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use in', 'Energy use out', 'Parent',
                  'Send tries', 'Send fails', 'Send success rate', 'Receive tries', 'Receive fails',
                  'Receive success rate', 'Battery average', 'Lifetime']]
        for r in Inventory.RELAYS:
            data += [[r.get_id(), r.get_x(), r.get_y(), r.get_range(), Inventory.f_str(r.get_battery()),
                      r.get_e_use_in(),
                      r.get_e_use_out(), r.get_parent(), r.get_send_count(), r.get_send_lost_count(),
                      Inventory.f_str(r.get_send_success_rate()),
                      r.get_receive_count(), r.get_receive_lost_count(), Inventory.f_str(r.get_receive_success_rate()),
                      Inventory.f_str(r.get_energy_average()), r.get_lifetime()]]
        with open(Inventory.EXPORT_ROOT + 'relays.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use out', 'Parent', 'Send tries', 'Send fails',
                  'Send success rate', 'Battery average', 'Lifetime']]
        for s in Inventory.SENSORS:
            data += [[s.get_id(), s.get_x(), s.get_y(), s.get_range(), Inventory.f_str(s.get_battery()),
                      s.get_e_use_out(),
                      s.get_parent(),
                      s.get_send_count(), s.get_send_lost_count(), Inventory.f_str(s.get_send_success_rate()),
                      s.get_energy_average(),
                      s.get_lifetime()]]
        with open(Inventory.EXPORT_ROOT + 'sensors.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Id', 'X', 'Y']]
        for s in Inventory.SINKS:
            data += [[s.get_id(), s.get_x(), s.get_y()]]
        with open(Inventory.EXPORT_ROOT + 'sinks.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

        data = []
        data += [['Average Period Length']]
        avg_period_length = self.schedule_run_count / Inventory.PERIOD_COUNT
        data += [[Inventory.f_str(avg_period_length)]]
        with open(Inventory.EXPORT_ROOT + 'simulation.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)

    # SETTERS AND GETTERS

    def get_scheduled(self):
        return self.scheduled

    @staticmethod
    def get_period_count():
        return Inventory.PERIOD_COUNT

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