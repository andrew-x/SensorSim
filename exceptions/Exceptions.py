__author__ = 'Andrew'


class NotEnoughEnergyException(Exception):
    pass


class DoneScheduleException(Exception):
    pass


class EmptyQueueException(Exception):
    pass


class NotFoundException(Exception):
    pass


class NullPeriodException(Exception):
    pass


class ImproperSettingsException(Exception):
    pass


class ImproperNodesException(Exception):
    pass


class ImproperScheduleException(Exception):
    pass