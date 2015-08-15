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
    EXPORT_ROOT = ROOT + ('//Generated//' if os.name == 'nt' else '/generated/')
    SETTINGS_FILENAME = os.path.join(ROOT, "input//SETTINGS.txt" if os.name == 'nt' else "input/SETTINGS.txt")
    NODES_FILENAME = os.path.join(ROOT, "input//NODES.txt" if os.name == 'nt' else "input/NODES.txt")
    SCHEDULE_FILENAME = os.path.join(ROOT, "input//SCHEDULE.txt" if os.name == 'nt' else "input/SCHEDULE.txt")

    GENERATE_NODES_PROTOCOL_FILENAME = os.path.join(ROOT, "protocols//GenerateNodesProtocol.py" if os.name == 'nt' else "protocols/GenerateNodesProtocol.py")
    GENERATE_SCHEDULE_PROTOCOL_FILENAME = os.path.join(ROOT, "protocols//GenerateScheduleProtocol.py" if os.name == 'nt' else "protocols/GenerateScheduleProtocol.py")

    # Settings

    NODES_TO_AUDIT = []
    AUDIT_PERIOD_LENGTH = False

    X_SIZE = 0
    Y_SIZE = 0
    SEED = 0
    REFRESH_DELAY = 0

    COLOR_SINK = 'blue'
    COLOR_RELAY = 'red'
    COLOR_SENSOR = 'green'
    COLOR_ENERGIZER = 'yellow'

    COLOR_LINK_DEFAULT = 'purple'
    COLOR_LINK_SUCCESS = 'green'
    COLOR_LINK_FAIL = 'red'

    # Constants
    SCALE_FACTOR = 5

    TYPE_SINK = 'i'
    TYPE_RELAY = 'r'
    TYPE_SENSOR = 's'
    TYPE_ENERGIZER = 'e'

    NEUTRAL_MODE = 0
    PLAY_MODE = 1
    STEP_THROUGH_MODE = 2
    PERIOD_MODE = 3

    UPDATE_TYPE_SEND_SUCCESS = 1
    UPDATE_TYPE_SEND_FAIL = 2
    UPDATE_TYPE_RECEIVE_SUCCESS = 3
    UPDATE_TYPE_RECEIVE_FAIL = 4

    # Model

    SCHEDULE = []
    SUCCESSFUL_LINKS = []
    FAILED_LINKS = []

    SINKS = []
    ENERGIZERS = []
    SENSORS = []
    RELAYS = []

    PACKETS = []

    PERIOD_COUNT = 0
    SCHEDULE_INDEX = 0

    PERIOD_LENGTHS = []

    PACKET_LOST_COUNT = 0

    @staticmethod
    def load_settings():
        """
        None -> None

        Loads the settings file values
        """
        x_size = -1
        y_size = -1
        seed = -1
        refresh_delay = -1

        nodes_to_audit = []
        audit_period_length = False
        audit_mode = False

        color_sink = ''
        color_relay = ''
        color_sensor = ''
        color_energizer = ''
        color_link_default = ''
        color_link_success = ''
        color_link_fail = ''

        with open(Inventory.SETTINGS_FILENAME) as f:
            content = f.readlines()
        for l in content:
            l = l.strip()
            val = l[l.index(':') + 1:]
            if 'X_SIZE' in l:
                x_size = Decimal(val)
            elif 'Y_SIZE' in l:
                y_size = Decimal(val)
            elif 'SEED' in l:
                seed = Decimal(val)
            elif 'REFRESH_DELAY' in l:
                refresh_delay = Decimal(val)
            elif 'NODES_TO_AUDIT' in l:
                nodes_to_audit = val.split(" ")
            elif 'AUDIT_PERIOD_LENGTH' in l:
                audit_period_length = val.lower() == 'true'
            elif 'AUDIT_MODE' in l:
                audit_mode == val.lower() == 'true'
            elif 'COLOR_SINK' in l:
                color_sink = val
            elif 'COLOR_RELAY' in l:
                color_relay = val
            elif 'COLOR_SENSOR' in l:
                color_sensor = val
            elif 'COLOR_ENERGIZER' in l:
                color_energizer = val
            elif 'COLOR_LINK_DEFAULT' in l:
                color_link_default = val
            elif 'COLOR_LINK_SUCCESS' in l:
                color_link_success = val
            elif 'COLOR_LINK_FAIL' in l:
                color_link_fail = val
        if x_size is not -1 and y_size is not -1 and seed is not -1 and refresh_delay is not -1\
                and color_sink is not '' and color_relay is not ''\
                and color_sensor is not '' and color_energizer is not '' and color_link_default is not ''\
                and color_link_success is not '' and color_link_fail is not '':
            Inventory.SEED = seed
            Inventory.REFRESH_DELAY = refresh_delay
            Inventory.X_SIZE = x_size
            Inventory.Y_SIZE = y_size
            Inventory.NODES_TO_AUDIT = nodes_to_audit
            Inventory.AUDIT_PERIOD_LENGTH = audit_period_length
            Inventory.AUDIT_MODE = audit_mode

            Inventory.COLOR_SINK = color_sink
            Inventory.COLOR_RELAY = color_relay
            Inventory.COLOR_SENSOR = color_sensor
            Inventory.COLOR_ENERGIZER = color_energizer
            Inventory.COLOR_LINK_DEFAULT = color_link_default
            Inventory.COLOR_LINK_SUCCESS = color_link_success
            Inventory.COLOR_LINK_FAIL = color_link_fail
        else:
            raise ImproperSettingsException

    @staticmethod
    def load_nodes():
        """
        None -> None

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
            raise ImproperNodesException

    @staticmethod
    def load_schedule():
        """
        None -> None

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
        """
        None -> list of all nodes

        Return list of all the nodes in the system.
        """
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
        """
        (Str) -> Node

        Returns the node in the system.
        """
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
        (Str) -> int

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
        (Str) -> int

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
        (Str) -> int

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
        (Str) -> int

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
        (Str) -> Packet

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
        """
        None -> Array of str

        returns the index for data export of packet.
        """
        return ['Id', 'Origin', 'Current', 'Delivered', 'Lost', 'Lost at', 'Hop Count']

    @staticmethod
    def get_energizer_export_index():
        """
        None -> Array of str

        returns the index for data export of energizer.
        """
        return ['Id', 'X', 'Y', 'Range', 'Battery', 'Gather Rate', 'Recharge Rate']

    @staticmethod
    def get_relay_export_index():
        """
        None -> Array of str

        returns the index for data export of relay.
        """
        return ['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use in', 'Energy use out', 'Parent',
                'Send tries', 'Send fails', 'Send success rate', 'Receive tries', 'Receive fails',
                'Receive success rate', 'Battery average', 'Lifetime']

    @staticmethod
    def get_sensor_export_index():
        """
        None -> Array of str

        returns the index for data export of sensor.
        """
        return ['Id', 'X', 'Y', 'Range', 'Battery', 'Energy use out', 'Parent', 'Send tries', 'Send fails',
                'Send success rate', 'Battery average', 'Lifetime']

    @staticmethod
    def get_sink_export_index():
        """
        None -> Array of str

        returns the index for data export of sink.
        """
        return ['Id', 'X', 'Y']

    @staticmethod
    def get_packet_export(p):
        """
        None -> Array of str

        returns formatted data fields of packet.
        """
        return [p.get_id(), p.get_origin(), p.get_current(), str(p.get_delivered()),
                str(p.get_lost()), p.get_lost_at(), str(p.get_hop_count())]

    @staticmethod
    def get_sensor_export(s):
        """
        None -> Array of str

        returns formatted data fields of sensor.
        """
        return [s.get_id(), s.get_x(), s.get_y(), s.get_range(), Inventory.f_str(s.get_battery()),
                s.get_e_use_out(), s.get_parent(),s.get_send_count(), s.get_send_lost_count(),
                Inventory.f_str(s.get_send_success_rate()), s.get_energy_average(), s.get_lifetime()]

    @staticmethod
    def get_energizer_export(e):
        """
        None -> Array of str

        returns formatted data fields of energizer.
        """
        return [e.get_id(), e.get_x(), e.get_y(), e.get_range(), Inventory.f_str(e.get_battery()),
                e.get_gather_rate(), e.get_recharge_rate()]

    @staticmethod
    def get_relay_export(r):
        """
        None -> Array of str

        returns formatted data fields of relay.
        """
        return [r.get_id(), r.get_x(), r.get_y(), r.get_range(), Inventory.f_str(r.get_battery()),
                r.get_e_use_in(), r.get_e_use_out(), r.get_parent(), r.get_send_count(), r.get_send_lost_count(),
                Inventory.f_str(r.get_send_success_rate()), r.get_receive_count(), r.get_receive_lost_count(),
                Inventory.f_str(r.get_receive_success_rate()), Inventory.f_str(r.get_energy_average()),
                r.get_lifetime()]

    @staticmethod
    def get_sink_export(s):
        """
        None -> Array of str

        returns formatted data fields of sink.
        """
        return [s.get_id(), s.get_x(), s.get_y()]

    @staticmethod
    def convert_values(to_convert):
        """
        (Decimal) -> Decimal

        Returns value converted to the scale of system. Used for rendering coordinates.
        """
        return to_convert * Inventory.SCALE_FACTOR

    @staticmethod
    def f_str(to_convert):
        """
        (Decimal) -> Str

        Returns value rounded to two decimal places as string.
        """
        return "{0:.2f}".format(to_convert)
