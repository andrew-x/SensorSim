__author__ = 'Andrew'

from core.Inventory import *
import os, csv


class Audit():

    def __init__(self):
        pass

    @staticmethod
    def set_up():
        if not os.path.exists(Inventory.EXPORT_ROOT):
            os.makedirs(Inventory.EXPORT_ROOT)
        with open(Inventory.EXPORT_ROOT + 'simulation_log.txt', 'w') as f:
            f.close()

    @staticmethod
    def to_log(line):
        if Inventory.AUDIT_MODE:
            with open(Inventory.EXPORT_ROOT + 'simulation_log.txt', 'a') as f:
                f.write(str(Inventory.PERIOD_COUNT) + ':' + str(Inventory.SCHEDULE_INDEX) + ' ' + line + '\n')
                f.close()

    @staticmethod
    def audit_transmission(packet_id, send_id, receive_id):
        line = send_id + ' sent ' + packet_id + ' to ' + receive_id
        Audit.to_log(line)

    @staticmethod
    def audit_send_fail(send_id, power, cost, packet_id=''):
        line = send_id + ' failed to send ' + packet_id + \
            ' because it needed ' + str(cost) + ' but had ' + Inventory.f_str(power) if packet_id is not '' \
            else send_id + ' failed to send ' + ' because it needed ' + str(cost) + ' but had ' + Inventory.f_str(power)
        Audit.to_log(line)

    @staticmethod
    def audit_receive_fail(receive_id, power, cost, packet_id):
        line = receive_id + ' failed to receive ' + packet_id + \
            ' because it needed ' + str(cost) + ' but had ' + Inventory.f_str(power)
        Audit.to_log(line)

    @staticmethod
    def audit_energy_loss(node_id, cost, power):
        line = node_id + ' used up ' + str(cost) + ' now has ' + Inventory.f_str(power)
        Audit.to_log(line)

    @staticmethod
    def audit_recharge(node_id, energizer_id, power, node_dist):
        line = node_id + ' gained ' + Inventory.f_str(power) + ' from ' + \
            energizer_id + ' at a distance of ' + Inventory.f_str(node_dist)
        Audit.to_log(line)

    @staticmethod
    def audit_energy_gather(energizer_id, recharge_amount, power):
        line = energizer_id + ' recharged by ' + Inventory.f_str(recharge_amount) + \
            ' now has ' + Inventory.f_str(power)
        Audit.to_log(line)

    @staticmethod
    def audit_nodes_history():
        for a in Inventory.NODES_TO_AUDIT:
            node = Inventory.find_node(a)
            out = []
            filename = Inventory.EXPORT_ROOT + node.get_id()+'_log.csv'
            try:
                num_lines = sum(1 for line in open(filename))
            except FileNotFoundError:
                num_lines = 0
            if a[0] is Inventory.TYPE_ENERGIZER:
                if num_lines is 0:
                    out += [['Period', 'Schedule run'] + Inventory.get_energizer_export_index()]
                out += [[str(Inventory.PERIOD_COUNT), str(Inventory.SCHEDULE_INDEX)] +\
                        Inventory.get_energizer_export(node)]
            elif a[0] is Inventory.TYPE_SENSOR:
                if num_lines is 0:
                    out += [['Period', 'Schedule run'] + Inventory.get_sensor_export_index()]
                out += [[str(Inventory.PERIOD_COUNT), str(Inventory.SCHEDULE_INDEX)] + \
                        Inventory.get_sensor_export(node)]
            elif a[0] is Inventory.TYPE_RELAY:
                if num_lines is 0:
                    out += [['Period', 'Schedule run'] + Inventory.get_relay_export_index()]
                out += [[str(Inventory.PERIOD_COUNT), str(Inventory.SCHEDULE_INDEX)] + \
                        Inventory.get_relay_export(node)]
            elif a[0] is Inventory.TYPE_SINK:
                if num_lines is 0:
                    out += [['Period', 'Schedule run'] + Inventory.get_sink_export_index()]
                out += [[str(Inventory.PERIOD_COUNT), str(Inventory.SCHEDULE_INDEX)] + \
                        Inventory.get_sink_export(node)]
            with open(filename, 'a', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerows(out)
                f.close()