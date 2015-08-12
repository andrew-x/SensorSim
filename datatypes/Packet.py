__author__ = 'Andrew'


class Packet():
    id = ''
    origin = ''
    current = ''
    lost_at = ''
    delivered = False
    lost = False

    hop_count = 0

    def __init__(self, packet_id='', origin=''):
        self.id = packet_id
        self.origin = origin
        self.current = origin
        self.delivered = False

    def increment_hop_count(self):
        """
        None -> None

        Increments the number of hops this packet has committed.
        """
        self.hop_count += 1

    def __str__(self):
        return 'id: ' + self.id + ' | origin: ' + self.origin + ' | current: ' + self.current + ' | delivered: ' + str(
            self.delivered) + ' | lost: ' + str(self.lost) + ' | lost at: ' + self.lost_at

    # GETTERS AND SETTERS

    def set_delivered(self):
        self.delivered = True

    def set_lost(self):
        self.lost_at = self.current
        self.current = ''
        self.lost = True

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

    def get_lost(self):
        return self.lost

    def get_lost_at(self):
        return self.lost_at

    def get_hop_count(self):
        return self.hop_count