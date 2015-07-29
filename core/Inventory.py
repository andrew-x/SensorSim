__author__ = 'Andrew'
import os
from exceptions.Exceptions import *
from datatypes.Energizer import *
from datatypes.Sink import *
from datatypes.Relay import *
from datatypes.Sensor import *
from datatypes.Packet import *
from decimal import Decimal

import unittest

class Inventory():
    """
    Contains all constants and static variables of the simulation.
    """

    TEST_SWITCH = 2
    AUDIT_MODE = True

    ROOT = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    EXPORT_ROOT = ROOT + '//Generated//'
    SETTINGS_FILENAME = os.path.join(ROOT, "input//SETTINGS.txt")
    NODES_FILENAME = os.path.join(ROOT, "input//NODES.txt")
    SCHEDULE_FILENAME = os.path.join(ROOT, "input//SCHEDULE.txt")

    GENERATE_NODES_PROTOCOL_FILENAME = os.path.join(ROOT,
                                                    "protocols//GenerateNodesProtocol.py")
    GENERATE_SCHEDULE_PROTOCOL_FILENAME = os.path.join(ROOT,
                                                    "protocols//GenerateScheduleProtocol.py")
    GENERATE_NODES_PROTOCOL_PYC_FILENAME = os.path.join(ROOT,
                                                        "protocols//__pycache__//GenerateNodesProtocol.cpython-34.pyc")

    # Settings

    SCALE_FACTOR = 5

    X_SIZE = 0
    Y_SIZE = 0
    SEED = 0
    REFRESH_DELAY = 0

    NEUTRAL_MODE = 0
    PLAY_MODE = 1
    STEP_THROUGH_MODE = 2
    PERIOD_MODE = 3

    # Constants

    TYPE_SINK = 'i'
    TYPE_RELAY = 'r'
    TYPE_SENSOR = 's'
    TYPE_ENERGIZER = 'e'

    COLOR_SINK = 'blue'
    COLOR_RELAY = 'red'
    COLOR_SENSOR = 'green'
    COLOR_ENERGIZER = 'yellow'

    COLOR_LINK_DEFAULT = 'purple'
    COLOR_LINK_SUCCESS = 'green'
    COLOR_LINK_FAIL = 'red'

    UPDATE_TYPE_SEND_SUCCESS = 1
    UPDATE_TYPE_SEND_FAIL = 2
    UPDATE_TYPE_RECEIVE_SUCCESS = 3
    UPDATE_TYPE_RECEIVE_FAIL = 4

    # Model

    SCHEDULE = []
    SUCCESSFUL_LINKS = []
    FAILED_LINKS = []
    NODES_TO_AUDIT = ['e1']

    SINKS = []
    ENERGIZERS = []
    SENSORS = []
    RELAYS = []

    PACKETS = []

    PERIOD_COUNT = 0
    SCHEDULE_INDEX = 0

    PACKET_LOST_COUNT = 0

    @staticmethod
    def load_settings():
        """
        (Controller) -> None

        Loads the settings file values
        """
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
            print('IMPROPER SETTINGS FILE')  # TODO: switch to forgiveness

    @staticmethod
    def load_nodes():
        """
        (Controller) -> None

        Loads nodes from input file.
        """
        '''
        INPUT PROTOCOL:
        SINKS:      I id x y
        ENERGIZERS: E id x y range battery gather_rate recharge_rate
        RELAY:      R id x y range battery energy_use_in energy_use_out parent_id
        SENSOR:     S id x y range battery energy_use_out energy_use_generate parent_id
        '''
        with open(Inventory.NODES_FILENAME) as f:
            content = f.readlines()
        try:
            for l in content:
                arr = l.split()
                if arr[0] is 'I':
                    Inventory.SINKS += [Sink(arr[1], int(arr[2]), int(arr[3]))]
                elif arr[0] is 'E':
                    Inventory.ENERGIZERS += [
                        Energizer(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]), int(arr[7]))]
                elif arr[0] is 'R':
                    Inventory.RELAYS += [
                        Relay(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]), int(arr[7]),
                              arr[8])]
                elif arr[0] is 'S':
                    Inventory.SENSORS += [
                        Sensor(arr[1], int(arr[2]), int(arr[3]), int(arr[4]), int(arr[5]), int(arr[6]),
                               int(arr[7]), arr[8])]
        except IndexError:
            print("INVALID NODES FILE")

    @staticmethod
    def load_schedule():
        """
        (Controller) -> None

        Loads schedule from input file.
        """
        with open(Inventory.SCHEDULE_FILENAME) as f:
            content = f.readlines()
        for l in content:
            arr = l.split()
            slot = []
            for a in arr:
                slot += [a]
            Inventory.SCHEDULE += [slot]

    @staticmethod
    def get_all_nodes():
        out = []
        for e in Inventory.ENERGIZERS:
            out += [e]
        for s in Inventory.SENSORS:
            out += [s]
        for r in Inventory.RELAYS:
            out += [r]
        for s in Inventory.SINKS:
            out += [s]
        return out

    @staticmethod
    def find_node(target):
        if target[0] == Inventory.TYPE_SINK:
            return Inventory.SINKS[Inventory.find_sink(target)]
        if target[0] == Inventory.TYPE_ENERGIZER:
            return Inventory.ENERGIZERS[Inventory.find_energizer(target)]
        if target[0] == Inventory.TYPE_RELAY:
            return Inventory.RELAYS[Inventory.find_relay(target)]
        if target[0] == Inventory.TYPE_SENSOR:
            return Inventory.SENSORS[Inventory.find_sensor(target)]

    @staticmethod
    def find_sink(target):
        """
        (Controller, string) -> int

        Returns the index of the sensor that matches the input id;
        raises NotFoundException if cannot be found
        """
        for i in range(0, len(Inventory.SINKS)):
            if Inventory.SINKS[i].get_id() == target:
                return i
        raise NotFoundException

    @staticmethod
    def find_energizer(target):
        """
        (Controller, string) -> int

        Returns the index of the sensor that matches the input id;
        raises NotFoundException if cannot be found
        """
        for i in range(0, len(Inventory.ENERGIZERS)):
            if Inventory.ENERGIZERS[i].get_id() == target:
                return i
        raise NotFoundException

    @staticmethod
    def find_relay(target):
        """
        (Controller, string) -> int

        Returns the index of the relay that matches the input id;
        raises NotFoundException if cannot be found
        """
        for i in range(0, len(Inventory.RELAYS)):
            if Inventory.RELAYS[i].get_id() == target:
                return i
        raise NotFoundException

    @staticmethod
    def find_sensor(target):
        """
        (Controller, string) -> int

        Returns the index of the sensor that matches the input id;
        raises NotFoundException if cannot be found
        """
        for i in range(0, len(Inventory.SENSORS)):
            if Inventory.SENSORS[i].get_id() == target:
                return i
        raise NotFoundException

    @staticmethod
    def find_packet(target):
        """
        (Controller, string) -> Packet

        Returns the packet that matches the input id;
        raises NotFoundException if cannot be found
        """
        pos = -1
        for i in range(0, len(Inventory.PACKETS)):
            if Inventory.PACKETS[i].get_id() == target:
                pos = i
                break
        else:
            raise NotFoundException
        return Inventory.PACKETS[pos]

    @staticmethod
    def get_packet_export_index():
        return ['Id', 'Origin', 'Current', 'Delivered', 'Lost', 'Lost at', 'Hop Count']

    @staticmethod
    def get_energizer_export_index():
        return ['Id', 'X', 'Y', 'Range', 'Battery', 'Gather Rate', 'Recharge Rate']

    @staticmethod
    def get_relay_export_index():
        return ['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use in', 'Energy use out', 'Parent',
                'Send tries', 'Send fails', 'Send success rate', 'Receive tries', 'Receive fails',
                'Receive success rate', 'Battery average', 'Lifetime']

    @staticmethod
    def get_sensor_export_index():
        return ['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use out', 'Parent', 'Send tries', 'Send fails',
                'Send success rate', 'Battery average', 'Lifetime']

    @staticmethod
    def get_sink_export_index():
        return ['Id', 'X', 'Y']

    @staticmethod
    def get_packet_export(p):
        return [p.get_id(), p.get_origin(), p.get_current(), str(p.get_delivered()),
                str(p.get_lost()), p.get_lost_at(), str(p.get_hop_count())]

    @staticmethod
    def get_sensor_export(s):
        return [s.get_id(), s.get_x(), s.get_y(), s.get_range(), Inventory.f_str(s.get_battery()),
                s.get_e_use_out(), s.get_parent(),s.get_send_count(), s.get_send_lost_count(),
                Inventory.f_str(s.get_send_success_rate()), s.get_energy_average(), s.get_lifetime()]

    @staticmethod
    def get_energizer_export(e):
        return [e.get_id(), e.get_x(), e.get_y(), e.get_range(), Inventory.f_str(e.get_battery()),
                e.get_gather_rate(), e.get_recharge_rate()]

    @staticmethod
    def get_relay_export(r):
        return [r.get_id(), r.get_x(), r.get_y(), r.get_range(), Inventory.f_str(r.get_battery()),
                r.get_e_use_in(), r.get_e_use_out(), r.get_parent(), r.get_send_count(), r.get_send_lost_count(),
                Inventory.f_str(r.get_send_success_rate()), r.get_receive_count(), r.get_receive_lost_count(),
                Inventory.f_str(r.get_receive_success_rate()), Inventory.f_str(r.get_energy_average()),
                r.get_lifetime()]

    @staticmethod
    def get_sink_export(s):
        return [s.get_id(), s.get_x(), s.get_y()]

    @staticmethod
    def convert_values(to_convert):
        return to_convert * Inventory.SCALE_FACTOR

    @staticmethod
    def f_str(to_convert):
        return "{0:.2f}".format(to_convert)