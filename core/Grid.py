__author__ = 'Andrew'


class Grid():
    x_size = 100
    y_size = 100

    def __init__(self, x=-1, y=-1):
        self.x_size = x
        self.y_size = y

    #SETTERS AND GETTERS
    def get_x_size(self):
        return self.x_size

    def get_y_size(self):
        return self.y_size