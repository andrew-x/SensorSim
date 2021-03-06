__author__ = 'Andrew'
from core.Audit import *
import csv, math
import pygraphviz as pgv
import plotly.plotly as py
from plotly.graph_objs import *
from urllib.request import *


class Controller():
    packet_count = 0

    dead_nodes = []
    dropped_packets = []
    dead_nodes_count = 0
    recharged_count = 0

    period_limit = -1

    scheduled = []
    period_initialized = False

    def __init__(self):
        Inventory.load_settings()
        Inventory.load_nodes()
        Inventory.load_schedule()

        Audit.set_up()

        Inventory.SCHEDULED = Inventory.SCHEDULE[0]
        Inventory.PACKETS = []
        Inventory.PERIOD_COUNT = 0

        self.packet_count = 0
        self.dead_nodes = []
        self.period_initialized = False
        self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
        self.schedule_run_count = 0

    def fire(self):
        """
        None -> None

        Runs a period
        """
        if Inventory.SCHEDULE_INDEX is 0:
            self.period_initialized = False
            Inventory.SCHEDULE_INDEX = 0
            self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]

            count = 0
            while True:
                count += 1
                try:
                    self.step_through()
                except DoneScheduleException:
                    break
            if Inventory.AUDIT_PERIOD_LENGTH:
                Inventory.PERIOD_LENGTHS += [count]
        else:
            while True:
                try:
                    self.step_through()
                except DoneScheduleException:
                    break
            self.fire()

    def step_through(self):
        """
        None -> None

        Runs scheduled slot
        """
        try:
            if not self.period_initialized:
                self.dead_nodes = []
                self.energize()
                self.generate_packets()
                self.period_initialized = True
            if not self.done_schedule():
                self.run_slot()
                Inventory.SCHEDULE_INDEX += 1
                if Inventory.SCHEDULE_INDEX >= len(Inventory.SCHEDULE):
                    Inventory.SCHEDULE_INDEX = 0
                self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
            else:
                self.collect_energy()
                Inventory.PERIOD_COUNT += 1
                self.period_initialized = False
                Inventory.SCHEDULE_INDEX = 0
                self.scheduled = Inventory.SCHEDULE[Inventory.SCHEDULE_INDEX]
                self.dead_nodes_count += len(self.dead_nodes)
                raise DoneScheduleException
        finally:
            Audit.audit_nodes_history()

    def done_schedule(self):
        """
        None -> None

        Checks if the schedule is done. As in, all packets that can be delivered this time has been delivered.
        """
        for p in Inventory.PACKETS:
            if p.get_delivered() is False and p.get_current() not in self.dead_nodes and p.get_lost() is False:
                return False
        return True

    def energize(self):
        """
        None -> None

        Energizes all nodes based on distance
        """
        for e in Inventory.ENERGIZERS:
            for r in Inventory.RELAYS:
                dist = math.sqrt(abs(r.get_x() - e.get_x()) ** 2 + abs(r.get_x() - e.get_y()) ** 2)
                to_charge = e.energize(dist)
                r.recharge(to_charge)
                self.recharged_count += to_charge
                Audit.audit_recharge(r.get_id(), e.get_id(), to_charge, dist)
            for s in Inventory.SENSORS:
                dist = math.sqrt(abs(s.get_x() - e.get_x()) ** 2 + abs(s.get_x() - e.get_y()) ** 2)
                to_charge = e.energize(dist)
                s.recharge(to_charge)
                self.recharged_count += to_charge
                Audit.audit_recharge(s.get_id(), e.get_id(), to_charge, dist)

    def collect_energy(self):
        """
        None -> None

        Recharge energizers
        """
        for e in Inventory.ENERGIZERS:
            gather_amount = e.gather_energy(Inventory.SEED)
            Audit.audit_energy_gather(e.get_id(), gather_amount, e.get_battery())

    def generate_packets(self):
        """
        None -> None

        Generates packets from sensors.
        """
        for s in Inventory.SENSORS:
            packet_id = "p" + str(self.packet_count+1)
            try:
                if s.generate_packet(packet_id):
                    Inventory.PACKETS += [Packet(packet_id, s.get_id())]
                    self.packet_count += 1
            except NotEnoughEnergyException:
                continue

    def run_slot(self):
        """
        None -> None

        Runs scheduled slot.
        """
        slot = self.scheduled

        Inventory.FAILED_LINKS = []
        Inventory.SUCCESSFUL_LINKS = []

        self.schedule_run_count += 1
        for sender_id in slot:
            sender = Inventory.find_node(sender_id)
            sender.increment_energy_count()
            if sender.get_id() not in self.dead_nodes:
                packet_id = ''
                parent_id = ''
                #Send
                try:
                    packet_id, parent_id = sender.send()
                    sender.increment_lifetime()
                except EmptyQueueException:
                    continue
                except NotEnoughEnergyException:
                    self.dead_nodes += [sender_id]
                    Inventory.FAILED_LINKS += [sender_id]
                    sender.increment_send_lost_count()
                    try:
                        Audit.audit_send_fail(sender_id, sender.get_battery(),
                            sender.get_e_use_out(), sender.get_to_send())
                    except EmptyQueueException:
                        Audit.audit_send_fail(sender_id, sender.get_battery(),
                            sender.get_e_use_out())
                    continue

                #Hand Off
                receiver = Inventory.find_node(parent_id)
                packet = Inventory.find_packet(packet_id)

                #Receive
                if parent_id[0] == Inventory.TYPE_SINK:
                    packet.set_delivered()
                    packet.set_current(parent_id)
                    packet.increment_hop_count()

                    Audit.audit_transmission(packet_id, sender_id, parent_id)

                    Inventory.SUCCESSFUL_LINKS += [sender_id]
                else:
                    try:
                        receiver.receive(packet_id)
                        packet.set_current(parent_id)
                        packet.increment_hop_count()

                        Audit.audit_transmission(packet_id, sender_id, parent_id)

                        Inventory.SUCCESSFUL_LINKS += [sender_id]
                    except NotEnoughEnergyException:
                        self.dead_nodes += [parent_id]
                        Inventory.FAILED_LINKS += [sender_id]
                        Audit.audit_receive_fail(parent_id, receiver.get_battery(),
                                                 receiver.get_e_use_in(), packet_id)

                        receiver.increment_receive_lost_count()
                        Inventory.PACKET_LOST_COUNT += 1
                        packet.set_lost()

    def export_data(self):
        """
        None -> None

        Exports data to csv files.
        """
        if Inventory.PERIOD_COUNT <= 0:
            raise NullPeriodException

        data = []
        data += [Inventory.get_packet_export_index()]
        for p in Inventory.PACKETS:
            data += [Inventory.get_packet_export(p)]
        with open(Inventory.EXPORT_ROOT + 'packets.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            f.close()

        data = []
        data += [Inventory.get_energizer_export_index()]
        for e in Inventory.ENERGIZERS:
            data += [Inventory.get_energizer_export(e)]
        with open(Inventory.EXPORT_ROOT + 'energizers.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            f.close()

        data = []
        data += [Inventory.get_relay_export_index()]
        for r in Inventory.RELAYS:
            data += [Inventory.get_relay_export(r)]
        with open(Inventory.EXPORT_ROOT + 'relays.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            f.close()

        data = []
        data += [Inventory.get_sensor_export_index()]
        for s in Inventory.SENSORS:
            data += [Inventory.get_sensor_export(s)]
        with open(Inventory.EXPORT_ROOT + 'sensors.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            f.close()

        data = []
        data += [Inventory.get_sink_export_index()]
        for s in Inventory.SINKS:
            data += [Inventory.get_sink_export(s)]
        with open(Inventory.EXPORT_ROOT + 'sinks.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            f.close()

        data = []
        data += [['Average Period Length', 'Packet Count', 'Lost Packets Count', 'Packet Loss Rate',
                  'Average Dead Nodes', 'Average energy recharged']]
        avg_period_length = self.schedule_run_count / Inventory.PERIOD_COUNT
        packet_lost_rate = Inventory.PACKET_LOST_COUNT / len(Inventory.PACKETS) * 100
        avg_dead_nodes = self.dead_nodes_count / Inventory.PERIOD_COUNT
        avg_energy_recharged = self.recharged_count / Inventory.PERIOD_COUNT
        data += [[Inventory.f_str(avg_period_length), str(len(Inventory.PACKETS)), str(Inventory.PACKET_LOST_COUNT),
                  Inventory.f_str(packet_lost_rate), Inventory.f_str(avg_dead_nodes),
                 Inventory.f_str(avg_energy_recharged)]]
        with open(Inventory.EXPORT_ROOT + 'simulation.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(data)
            f.close()

    def export_standard_graph(self):
        """
        None -> None

        Renders and exports the entire topology.
        """
        G = pgv.AGraph()
        G.graph_attr.update(size=str(Inventory.X_SIZE)+','+str(Inventory.Y_SIZE))
        for node in Inventory.get_all_nodes():
            G.add_node(node.get_id())
            G.get_node(node.get_id()).attr['label'] = node.get_id()
            G.get_node(node.get_id()).attr['pos'] = str(node.get_x()) + ',' + str(100-node.get_y())+'!'
        for node in Inventory.SENSORS:
            G.add_edge(node.get_id(), node.get_parent())
        for node in Inventory.RELAYS:
            G.add_edge(node.get_id(), node.get_parent())
        G.layout()
        G.draw(Inventory.EXPORT_ROOT + 'standard_graph.png', format='png')

    def export_hierarchical_graph(self):
        """
        None -> None

        Renders the hierarchy.
        """
        levels = [[]]
        for s in Inventory.SENSORS:
            levels[0] += [s]
        while True:
            levels += [[]]
            done = True
            for n in levels[len(levels)-2]:
                if n.get_id()[0] is not Inventory.TYPE_SINK:
                    done = False
                    levels[len(levels)-1] += [Inventory.find_node(n.get_parent())]
                else:
                    continue
            if done:
                break
        G = pgv.AGraph()
        G.graph_attr.update(size=str(Inventory.X_SIZE)+','+str(Inventory.Y_SIZE))
        for y in range(len(levels)):
            for x in range(len(levels[y])):
                n = levels[y][x]
                G.add_node(n.get_id())
                G.get_node(n.get_id()).attr['label'] = n.get_id()
                G.get_node(n.get_id()).attr['pos'] = str(x*2) + ',' + str(y*2) + '!'
        for node in Inventory.SENSORS:
            G.add_edge(node.get_id(), node.get_parent())
        for node in Inventory.RELAYS:
            if self.check_levels_membership(levels, node):
                G.add_edge(node.get_id(), node.get_parent())
        count = 0
        for n in Inventory.get_all_nodes():
            if not self.check_levels_membership(levels, n):
                G.add_node(n.get_id())
                G.get_node(n.get_id()).attr['label'] = n.get_id()
                G.get_node(n.get_id()).attr['pos'] = str(count*2) + ',' + str(len(levels) + 2) + '!'
                count += 1
        G.layout()
        G.draw(Inventory.EXPORT_ROOT + 'hierarchical_graph.png', format='png')

    def check_levels_membership(self, levels, node):
        """
        (Arr of Str, Node) -> bool

        Checks if the node is in the current tree.
        """
        for y in range(len(levels)):
            for x in range(len(levels[y])):
                if node.get_id() is levels[y][x].get_id():
                    return True
        return False

    def export_period_length_trend(self):
        """
        None -> None

        Renders trend-line, launches plot.ly and renders picture locally.
        """
        if not Inventory.AUDIT_PERIOD_LENGTH:
            raise ImproperSettingsException
        if not self.check_internet():
            raise ConnectionException
        x = []
        for i in range(Inventory.PERIOD_COUNT):
            x += [i+1]
        trace = Scatter(x=x, y=Inventory.PERIOD_LENGTHS)
        data = Data([trace])
        py.plot(data, filename='Period_length_trend')
        py.image.save_as({'data':data}, Inventory.EXPORT_ROOT + '\Period_Length_Trend.png')


    def check_internet(self):
        """
        None -> bool

        Checks connection to plot.ly website.
        """
        try:
            urlopen('http://www.plot.ly/')
            return True
        except Exception:
            return False

    # SETTERS AND GETTERS

    def get_scheduled(self):
        return self.scheduled

    @staticmethod
    def get_period_count():
        return Inventory.PERIOD_COUNT

    @staticmethod
    def set_energizers(energizers):
        Inventory.ENERGIZERS = energizers

    @staticmethod
    def set_relays(relays):
        Inventory.RELAYS = relays

    @staticmethod
    def set_sensors(sensors):
        Inventory.SENSORS = sensors

    @staticmethod
    def set_sinks(sinks):
        Inventory.SINKS = sinks