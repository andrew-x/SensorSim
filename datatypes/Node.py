__author__ = 'Andrew'


class Node():
    id = ''
    x = -1
    y = -1
    lifetime = 0

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return 'id: ' + self.id + ' | x: ' + str(self.x) + ' | y: ' + str(self.y) + ' | lifetime: ' + str(self.lifetime)

    def increment_lifetime(self):
        """
        None -> None

        Increments the measure of how long the node
        has been alive.
        """
        self.lifetime += 1

    # SETTERS AND GETTERS

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_lifetime(self):
        return self.lifetime