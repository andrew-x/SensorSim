__author__ = 'Andrew'

from gui.editFrames.SinkEditFrame import *
from gui.editFrames.EnergizersEditFrame import *
from gui.editFrames.SensorsEditFrame import *
from gui.editFrames.RelaysEditFrame import *

from gui.infoFrames.PacketsInfoFrame import *
from gui.infoFrames.SinkInfoFrame import *
from gui.infoFrames.RelaysInfoFrame import *
from gui.infoFrames.SensorsInfoFrame import *
from gui.infoFrames.EnergizersInfoFrame import *
from gui.generateFrames.GenerateNodesFrame import *
from core.Controller import *
from gui.GraphFrame import *

import _thread
import time
import os


class MainFrame(Frame):
    control = None

    packet_info_frame = None
    energizers_info_frame = None
    relays_info_frame = None
    sensors_info_frame = None
    sink_info_frame = None

    scheduled_label = None
    scheduled_label_text = None
    period_label = None
    period_label_text = None

    play_button = None
    step_through_button = None
    next_period_button = None

    mode = 0

    graph = None

    playing = False
    threads_stop = True

    def __init__(self, master=Tk()):
        super(MainFrame, self).__init__(master)

        self.control = Controller()

        self.init_window()

        self.set_widgets()

        self.mainloop()

    def init_window(self):
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.master.update_idletasks()
        self.master.title('Wireless Networks Simulation')

    def exit(self):
        self.master.destroy()
        sys.exit(True)

    def set_widgets(self):
        menubar = Menu(self)

        file_menu = Menu(menubar, tearoff=1)
        file_menu.add_command(label='Edit Nodes', command=self.open_nodes)
        file_menu.add_command(label='Edit Schedule', command=self.open_schedule)
        file_menu.add_command(label='Edit Settings ', command=self.open_settings)
        file_menu.add_command(label='Reset', command=self.reset)
        file_menu.add_command(label='Export Data ', command=self.export_data)
        file_menu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(label='File', menu=file_menu)

        edit_menu = Menu(menubar, tearoff=1)
        edit_menu.add_command(label='Edit Sink Information', command=self.edit_sink_info)
        edit_menu.add_command(label='Edit Energizers Information', command=self.edit_energizers_info)
        edit_menu.add_command(label='Edit Sensors Information', command=self.edit_sensors_info)
        edit_menu.add_command(label='Edit Relays Information', command=self.edit_relays_info)
        menubar.add_cascade(label='Edit', menu=edit_menu)

        view_menu = Menu(menubar, tearoff=1)
        view_menu.add_command(label='View Sink Information', command=self.view_sink_info)
        view_menu.add_command(label='View Energizers Information', command=self.view_energizers_info)
        view_menu.add_command(label='View Sensors Information', command=self.view_sensors_info)
        view_menu.add_command(label='View Relays Information', command=self.view_relays_info)
        menubar.add_cascade(label='View', menu=view_menu)

        generate_menu = Menu(menubar, tearoff=1)
        generate_menu.add_command(label='Generate Nodes', command=self.generate_nodes)
        menubar.add_cascade(label='Generate', menu=generate_menu)

        try:
            self.master.config(menu=menubar)
        except AttributeError:
            self.master.tk.call(self.master, "config", "-menu", menubar)

        self.scheduled_label_text = StringVar()
        self.scheduled_label = Label(self.master, textvariable=self.scheduled_label_text)
        self.scheduled_label.grid(row=0, columnspan=3)

        self.period_label_text = StringVar()
        self.period_label = Label(self.master, textvariable=self.period_label_text)
        self.period_label.grid(row=1, columnspan=3)

        self.play_button = Button(self.master, text='Play', command=self.on_play)
        self.play_button.grid(row=2, column=0, pady=10, padx=5)

        self.step_through_button = Button(self.master, text='Step Through', command=self.on_step)
        self.step_through_button .grid(row=2, column=1, pady=10, padx=15)

        self.next_period_button = Button(self.master, text='Next Period', command=self.on_next_period)
        self.next_period_button.grid(row=2, column=2, pady=10, padx=5)

        self.graph = GraphFrame(self.master)

        self.refresh()

    # CONTROL OPTIONS
    def refresh(self):
        self.refresh_labels()
        self.graph.refresh(self.mode)

        # self.refresh_info_frames()

    def refresh_info_frames(self):
        if not self.relays_info_frame is None:
            self.relays_info_frame.destroy()
            self.relays_info_frame.set_widgets()

    def refresh_labels(self):
        self.scheduled_label_text.set('Scheduled: ' + ', '.join(x.get_id() for x in self.control.get_scheduled()))
        self.period_label_text.set('Period Count: ' + str(self.control.get_period_count()+1))

    def on_play(self):
        self.mode = Inventory.PLAY_MODE
        if self.threads_stop:
            self.threads_stop = False
            _thread.start_new_thread(self.main_loop, ())

        self.play_button.configure(text='Stop', command=self.on_stop)
        self.playing = True

    def on_stop(self):
        self.mode = Inventory.NEUTRAL_MODE
        self.play_button.configure(text='Play', command=self.on_play)
        self.playing = False

    def on_next_period(self):
        self.mode = Inventory.PERIOD_MODE
        if not self.playing:
            self.control.fire()
            self.refresh()

    def on_step(self):
        self.mode = Inventory.STEP_THROUGH_MODE
        if not self.playing:
            try:
                self.control.step_through()
            except DoneScheduleException:
                pass
            self.refresh()

    # THREAD OPTIONS

    def main_loop(self):
        while not self.threads_stop:
            if self.playing:
                self.control.fire()
                self.refresh()
                time.sleep(Inventory.REFRESH_DELAY)

    # MENU OPTIONS

    def view_sink_info(self):
        self.sink_info_frame = SinkInfoFrame()

    def view_energizers_info(self):
        self.energizers_info_frame = EnergizersInfoFrame()

    def view_relays_info(self):
        self.relays_info_frame = RelaysInfoFrame()

    def view_sensors_info(self):
        self.sensors_info_frame = SensorsInfoFrame()

    def edit_sink_info(self):
        root = Tk()
        sink_info = SinkEditFrame(master=root)
        sink_info.set_widgets()
        sink_info.mainloop()
        root.destroy()

    def edit_energizers_info(self):
        root = Tk()
        energizers_info = EnergizersEditFrame(master=root)
        energizers_info.mainloop()
        root.destroy()

    def edit_relays_info(self):
        root = Tk()
        relays_info = RelaysEditFrame(master=root)
        relays_info.mainloop()
        root.destroy()

    def edit_sensors_info(self):
        root = Tk()
        sensors_info = SensorsEditFrame(master=root)
        sensors_info.mainloop()
        root.destroy()

    def open_nodes(self):
        os.system("start " + Inventory.NODES_FILENAME)

    def open_schedule(self):
        os.system("start " + Inventory.SCHEDULE_FILENAME)

    def open_settings(self):
        os.system("start " + Inventory.SETTINGS_FILENAME)

    def reset(self):
        self.control = Controller()
        self.refresh()

    def export_data(self):
        self.control.export_data()

    def generate_nodes(self):
        GenerateNodesFrame()