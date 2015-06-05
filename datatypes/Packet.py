__author__ = 'Andrew'


class Packet():
    id = ''
    origin = ''
    current = ''
    delivered = False

    def __init__(self, id='', origin=''):
        self.id = id
        self.origin = origin
        self.current = origin
        self.delivered = False

    def __str__(self):
        return 'ID: ' + self.id + ' ORIGIN: ' + self.origin + ' CURRENT: ' + self.current + ' DELIVERED: ' + str(self.delivered)

    def set_delivered(self):
        self.delivered = True

    def set_current(self, current):
        self.current = current

    def get_id(self):
        return self.id

    def get_origin(self):
        return self.origin

    def get_current(self):
        return self.current

    def get_delivered(self):
        return self.delivered