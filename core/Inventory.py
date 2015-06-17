__author__ = 'Andrew'


class Inventory():
    TEST_SWITCH = 1


    SETTINGS_FILENAME = "SETTINGS.txt"
    NODES_FILENAME = "NODES.txt"
    SCHEDULE_FILENAME = "SCHEDULE.txt"

    SKIP_SIZE = 0
    REFRESH_RATE = 0

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

    CONTROL = None