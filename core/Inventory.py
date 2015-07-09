__author__ = 'Andrew'
import os


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

    X_SIZE = 0
    Y_SIZE = 0
    SEED = 0
    REFRESH_DELAY = 0

    TYPE_SINK = 'i'
    TYPE_RELAY = 'r'
    TYPE_SENSOR = 's'
    TYPE_ENERGIZER = 'e'

    UPDATE_TYPE_SEND_SUCCESS = 1
    UPDATE_TYPE_SEND_FAIL = 2
    UPDATE_TYPE_RECEIVE_SUCCESS = 3
    UPDATE_TYPE_RECEIVE_FAIL = 4

    SCHEDULE = []

    SINK = None
    ENERGIZERS = []
    SENSORS = []
    RELAYS = []

    PACKETS = []