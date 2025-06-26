import opendssdirect as dss
from opendssdirect.utils import Iterator
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import pandas as pd


# Direct the DSS files
dss.run_command('Redirect OpenDSS_files/master_new_secondary_loads.dss')
dss.run_command('Compile OpenDSS_files/master_new_secondary_loads.dss')

dss.Text.Command('set loadmult = 0.6')

dss.Solution.Solve()

# Extract nodal voltages
node_names = dss.Circuit.AllNodeNames()
nodeA_names = []
nodeB_names = []
nodeC_names = []
for node in node_names:
    if ".1" in node:
        nodeA_names.append(node)
    elif ".2" in node:
        nodeB_names.append(node)
    elif ".3" in node:
        nodeC_names.append(node)

bus_voltages = {}
bus_A = []
bus_B = []
bus_C = []
phases = [1, 2, 3]
for p in phases:
    for idx, voltage in enumerate(dss.Circuit.AllNodeVmagPUByPhase(p)):
        if p == 1:
            bus_A.append(voltage)
            bus_voltages[nodeA_names[idx]] = voltage
        elif p == 2:
            bus_B.append(voltage)
            bus_voltages[nodeB_names[idx]] = voltage
        elif p == 3:
            bus_C.append(voltage)
            bus_voltages[nodeC_names[idx]] = voltage


data = {'Va': bus_A,
                'Vb': bus_B,
                'Vc': bus_C}

PV_names = []
PV_buses = []
for i in Iterator(dss.PVsystems, 'Name'):
    pv_name = dss.PVsystems.Name()
    dss.Circuit.SetActiveElement(f"PVsystem.{pv_name}")
    pv_bus = dss.CktElement.BusNames()[0]
    PV_names.append(pv_name)
    PV_buses.append(pv_bus)



Load_names = []
Load_buses = []
for i in Iterator(dss.Loads, 'Name'):
    load_name = dss.Loads.Name()
    dss.Circuit.SetActiveElement(f"Load.{load_name}")
    load_bus = dss.CktElement.BusNames()[0]
    Load_names.append(load_name)
    Load_buses.append(load_bus)


print("ssssss")
## 77777777777777777777777777777777777
# dss.Text.Command('calcv')
#
# Script to control PV system
# dss.run_command('Generator.' + 'DG_S10a' + '.kW=' + str(100))

# dss.run_command("new Generator.DG_7  bus1=7.1 phases=1 kV=2.4 kW=1000  kvar=0  Vmaxpu=2.0 Vminpu=0.1")
# dss.run_command('PVSystems.DG_6.kW=500')

# dss.Text.Command('Set Controlmode=OFF')

# Solve the circuit
# dss.run_command('solve')
# dss.run_command('show voltages LN Nodes')
# # file_path = os.getcwd()
# file_path = '../../solutions//voltage_opendss.json'
# with open(file_path, 'w') as json_file:
#     json.dump(data, json_file)
#
# # Extract line flows. Example is shown for a line connected to source bus
# print('\n..........Substation Flow.............')
# # line_flow_sensors = ['l115']
# line_flow_sensors = ['l3']
# for line in line_flow_sensors:
#     element = 'Line.' + line
#     dss.Circuit.SetActiveElement(element)
#     s_flow = dss.CktElement.Powers()
#     power_len = int(len(s_flow) / 2)
#     p_flow = []
#     q_flow = []
#     for k in range(0,power_len,2):
#         p_flow.append(s_flow[k])
#         q_flow.append(s_flow[k+1])
#         print("P flow: ", str(s_flow[k]), "   Q flow: ", str(s_flow[k+1]) )
#     # print(complex(dss.CktElement.Powers()[0], dss.CktElement.Powers()[1]))
#     # print(complex(dss.CktElement.Powers()[2], dss.CktElement.Powers()[3]))
#     # print(complex(dss.CktElement.Powers()[4], dss.CktElement.Powers()[5]))
#
# # print transformers tap
# print('\n..........Transformer Taps.............')
# for i in Iterator(dss.Transformers, 'Name'):
#     print(dss.Transformers.Name(), dss.Transformers.Tap())
#
# # Min, Max voltage and profile plot
# print('\n..........Voltage Min-Max.............')
# print(max(bus_A), max(bus_B), max(bus_C))
# print(min(bus_A), min(bus_B), min(bus_C))
# plt.scatter(range(len(bus_A)), bus_A, c='blue', edgecolor='blue')
# plt.scatter(range(len(bus_B)), bus_B, c='green', edgecolor='green')
# plt.scatter(range(len(bus_C)), bus_C, c='red', edgecolor='red')
#
# max_node = max(len(bus_A),len(bus_B),len(bus_C))
#
# min_y = min(min(bus_A), min(bus_B), min(bus_C))
# max_y = max(max(bus_A), max(bus_B), max(bus_C))
# # plt.ylim([min_y - 0.01, max_y + 0.01])
# plt.ylim([0.94, 1.06])
#
# plt.xlabel('Bus Index')
# plt.ylabel('Voltage (p.u.)')
# plt.legend(['Phase-A', 'Phase-B', 'Phase-C'])
# plt.xticks([0, 1,2,3,4],["150", "1","2", "3","S3C_2"])
# plt.plot(np.ones(max_node+1)*1.05, 'r--')
# plt.plot(np.ones(max_node+1)*0.95, 'r--')
# plt.show()
