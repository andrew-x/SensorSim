__author__ = 'Andrew'
from tkinter import *
from datatypes.Sink import *
from core.Controller import *


class GraphFrame(Frame):
    master = None
    canvas = None

    def __init__(self, master=None):
        self.master = master
        super(GraphFrame, self).__init__(self.master)
        self.canvas = Canvas(self.master, width=Inventory.convert_values(Inventory.X_SIZE)
                             , height=Inventory.convert_values(Inventory.Y_SIZE))
        self.canvas.grid(columnspan=3)
        self.refresh(0)
        self.init_window()

    def init_window(self):
        self.master.update_idletasks()

    def refresh(self, mode):
        self.canvas.delete('all')
        self.render(mode)

    def render(self, mode):
        if mode == Inventory.STEP_THROUGH_MODE:
            self.render_step()
        else:
            self.render_links()

        self.render_nodes()

    def render_step(self):
        for s in Inventory.SUCCESSFUL_LINKS:
            link_dimensions = self.get_link_dimensions(s)
            self.canvas.create_line(link_dimensions[0], link_dimensions[1], link_dimensions[2],
                                    link_dimensions[3], fill=Inventory.COLOR_LINK_SUCCESS)
        for f in Inventory.FAILED_LINKS:
            link_dimensions = self.get_link_dimensions(f)
            self.canvas.create_line(link_dimensions[0], link_dimensions[1], link_dimensions[2],
                                    link_dimensions[3], fill=Inventory.COLOR_LINK_FAIL, dash=(4,4))

    def render_links(self):
        for r in Inventory.RELAYS:
            link_dimensions = self.get_link_dimensions(r)
            self.canvas.create_line(link_dimensions[0], link_dimensions[1], link_dimensions[2],
                                    link_dimensions[3], fill=Inventory.COLOR_LINK_DEFAULT)

        for s in Inventory.SENSORS:
            link_dimensions = self.get_link_dimensions(s)
            self.canvas.create_line(link_dimensions[0], link_dimensions[1], link_dimensions[2],
                                    link_dimensions[3], fill=Inventory.COLOR_LINK_DEFAULT)

    def render_nodes(self):
        for r in Inventory.RELAYS:
            dimensions = self.get_rectangle_dimensions(r.get_x(), r.get_y())
            self.canvas.create_rectangle(dimensions[0], dimensions[1], dimensions[2],
                                         dimensions[3], fill=Inventory.COLOR_RELAY)

        for s in Inventory.SENSORS:
            dimensions = self.get_rectangle_dimensions(s.get_x(), s.get_y())
            self.canvas.create_rectangle(dimensions[0], dimensions[1], dimensions[2],
                                         dimensions[3], fill=Inventory.COLOR_SENSOR)

        for e in Inventory.ENERGIZERS:
            dimensions = self.get_rectangle_dimensions(e.get_x(), e.get_y())
            self.canvas.create_rectangle(dimensions[0], dimensions[1], dimensions[2],
                                         dimensions[3], fill=Inventory.COLOR_ENERGIZER)

        for i in Inventory.SINKS:
            dimensions = self.get_rectangle_dimensions(i.get_x(), i.get_y())
            self.canvas.create_rectangle(dimensions[0], dimensions[1], dimensions[2],
                                         dimensions[3], fill=Inventory.COLOR_SINK)

    def get_rectangle_dimensions(self, x, y):
        return Inventory.convert_values(x)-Inventory.SCALE_FACTOR, Inventory.convert_values(y)-Inventory.SCALE_FACTOR,\
            Inventory.convert_values(x)+Inventory.SCALE_FACTOR, Inventory.convert_values(y)+Inventory.SCALE_FACTOR

    def get_link_dimensions(self, node):
        parent = None
        parentId = node.get_parent()
        if parentId[0] == Inventory.TYPE_SINK:
            parent = Inventory.SINKS[Inventory.find_sink(parentId)]
        elif parentId[0] == Inventory.TYPE_SENSOR:
            parent = Inventory.SENSORS[Inventory.find_sensor(parentId)]
        elif parentId[0] == Inventory.TYPE_RELAY:
            parent = Inventory.RELAYS[Inventory.find_relay(parentId)]

        if parent is None:
            raise NotFoundException

        return Inventory.convert_values(node.get_x()), Inventory.convert_values(node.get_y()), \
               Inventory.convert_values(parent.get_x()), Inventory.convert_values(parent.get_y())



