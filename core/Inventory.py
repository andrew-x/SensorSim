__author__ = 'Andrew'
import os


class Inventory():
    TEST_SWITCH = 2

    ROOT = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    SETTINGS_FILENAME = os.path.join(ROOT, "input//SETTINGS.txt")
    NODES_FILENAME = os.path.join(ROOT, "input//NODES.txt")
    SCHEDULE_FILENAME = os.path.join(ROOT, "input//SCHEDULE.txt")

    X_SIZE = 0
    Y_SIZE = 0
    SEED = 0
    REFRESH_DELAY = 0

    TYPE_SINK = 'i'
    TYPE_RELAY = 'r'
    TYPE_SENSOR = 's'
    TYPE_ENERGIZER = 'e'

    SCHEDULE = []

    SINK = None
    ENERGIZERS = []
    SENSORS = []
    RELAYS = []

    PACKETS = []