__author__ = 'Andrew'

from core.Inventory import *


class Debug():
    @staticmethod
    def print_send_receive():
        print(*Inventory.RELAYS, sep='\n')
        print(*Inventory.SENSORS, sep='\n')

    @staticmethod
    def print_packets():
        print(*Inventory.PACKETS, sep='\n')

    @staticmethod
    def print_relays():
        print(*Inventory.RELAYS, sep='\n')

    @staticmethod
    def print_sensors():
        print(*Inventory.SENSORS, sep='\n')

    @staticmethod
    def print_sinks():
        print(*Inventory.SINKS, sep='\n')

    @staticmethod
    def print_energizers():
        print(*Inventory.ENERGIZERS, sep='\n')

    @staticmethod
    def print_node(node):
        print(Inventory.find_node(node))
