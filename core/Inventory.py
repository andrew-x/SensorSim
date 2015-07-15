__author__ = 'Andrew'
import os
from exceptions.Exceptions import *
from datatypes.Energizer import Energizer
from datatypes.Sink import Sink
from datatypes.Relay import Relay
from datatypes.Sensor import Sensor
from datatypes.Packet import Packet
from decimal import Decimal

class Inventory():
    """
    Contains all constants and static variables of the simulation.
    """

    TEST_SWITCH = 2

    ROOT = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    EXPORT_ROOT = ROOT + '//Generated//'
    SETTINGS_FILENAME = os.path.join(ROOT, "input//SETTINGS.txt")
    NODES_FILENAME = os.path.join(ROOT, "input//NODES.txt")
    SCHEDULE_FILENAME = os.path.join(ROOT, "input//SCHEDULE.txt")

    GENERATE_NODES_PROTOCOL_FILENAME = os.path.join(ROOT, "protocols//GenerateNodesProtocol.py")
    GENERATE_NODES_PROTOCOL_PYC_FILENAME = os.path.join(ROOT, "protocols//__pycache__//GenerateNodesProtocol.cpython-34.pyc")

    SCALE_FACTOR = 5

    X_SIZE = 0
    Y_SIZE = 0
    SEED = 0
    REFRESH_DELAY = 0

    NEUTRAL_MODE = 0
    PLAY_MODE = 1
    STEP_THROUGH_MODE = 2
    PERIOD_MODE = 3

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

    SCHEDULE = []
    SUCCESSFUL_LINKS = []
    FAILED_LINKS = []

    SINKS = []
    ENERGIZERS = []
    SENSORS = []
    RELAYS = []

    PACKETS = []

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
        ENERGIZERS: E id x y range battery rate
        RELAY:      R id x y range battery energy_use_in energy_use_out parent_id
        SENSOR:     S id x y range battery energy_use_out parent_id
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
                if a[0] == Inventory.TYPE_RELAY:
                    slot += [Inventory.RELAYS[Inventory.find_relay(a)]]
                elif a[0] == Inventory.TYPE_SENSOR:
                    slot += [Inventory.SENSORS[Inventory.find_sensor(a)]]
            Inventory.SCHEDULE += [slot]

    @staticmethod
    def find_sink(target):
        """
        (Controller, string) -> int

        Returns the index of the sensor that matches the input id;
        returns -1 if sensor cannot be found
        """
        for i in range(0, len(Inventory.SINKS)):
            if Inventory.SINKS[i].get_id() == target:
                return i
        return -1

    @staticmethod
    def find_energizer(target):
        """
        (Controller, string) -> int

        Returns the index of the sensor that matches the input id;
        returns -1 if sensor cannot be found
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
        returns -1 if relay cannot be found
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
        returns -1 if sensor cannot be found
        """
        for i in range(0, len(Inventory.SENSORS)):
            if Inventory.SENSORS[i].get_id() == target:
                return i
        raise NotFoundException

    @staticmethod
    def find_packet(target):
        """
        (Controller, string) -> int

        Returns the index of the packet that matches the input id;
        returns -1 if packet cannot be found
        """
        for i in range(0, len(Inventory.PACKETS)):
            if Inventory.PACKETS[i].get_id() == target:
                return i
        raise NotFoundException

    @staticmethod
    def convert_values(to_convert):
        return to_convert * Inventory.SCALE_FACTOR