__author__ = 'Andrew'

from core.Inventory import *
import os


class Audit():

    def __init__(self):
        pass

    @staticmethod
    def set_up():
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
        line = energizer_id + ' recharged by ' + str(recharge_amount) + \
            ' now has ' + Inventory.f_str(power)
        Audit.to_log(line)