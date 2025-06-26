import win32com.client
import numpy as np
import pandas as pd
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ColorConverter
import matplotlib.text as text

colorConverter = ColorConverter()
import re
import os
import json
import copy

class DSS:
    # """
    # tshort@epri.com 2008-11-17
    # comments: wsunderman@epri.com 2009-10-30

    def __init__(self, filename=""):
        """
        Inputs:
            filename - string - DSS input file
        Side effects:
            start DSS via COM
        Contains the following DSS COM objects:
            engine
            text
            circuit
        """
        # start an embedded DSS engine through COM
        # note: OpenDSSEngine.dll must already be registered
        self.engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
        self.engine.Start("0")

        # use the Text interface to OpenDSS
        self.text = self.engine.Text
        self.text.Command = "clear"
        self.circuit = self.engine.ActiveCircuit

        print(self.engine.Version)

        # if filename is not empty, then compile the .dss file specified
        # note:  filename includes the path and the .dss file name
        # note:  the .dss file compiled is usually the master.dss file
        # note:  an energymeter should be defined at the head of the circuit
        # being modeled
        # note:  if compilation is successful we have a circuit instance
        # that represents the electric circuit that is being modeled
        if filename != "":
            self.text.Command = "compile [" + filename + "]"
            self.text.Command = "solve"
            # self.text.Command = "Buscoords IEEE13Node_BusXY.csv"  # load in bus coordinates
            # self.populate_results()


def get_Y_Bus_info(DSSobj, Y_bus_filename, Y_node_filename):
    DSSobj.text.Command = "batchedit transformer..* wdg=2 tap=1"
    DSSobj.text.Command = "batchedit regcontrol..* enabled=false"
    DSSobj.text.Command = "batchedit vsource..* enabled=false"
    DSSobj.text.Command = "batchedit isource..* enabled=false"
    DSSobj.text.Command = "batchedit load..* enabled=false"
    DSSobj.text.Command = "batchedit generator..* enabled=false"
    DSSobj.text.Command = "batchedit pvsystem..* enabled=false"
    DSSobj.text.Command = "batchedit storage..* enabled=false"

    # DSSobj.text.Command = "BusCoords IEEE13Node_BusXY.csv"
    DSSobj.text.Command = "Solve"

    DSSobj.text.Command = "export y triplet [" + Y_bus_filename + "]"
    DSSobj.text.Command = "export ynodelist [" + Y_node_filename + "]"

    node_df = pd.read_csv(Y_node_filename, header=None)
    Y_bus_df = pd.read_csv(Y_bus_filename)

    node_name = {}
    for idx in range(len(node_df)):
        node_name[node_df[0][idx]] = idx

    N = len(node_name)
    ybus = np.zeros((N, N), dtype=complex)
    for idx in range(len(Y_bus_df)):
        ybus[int(Y_bus_df.Row[idx]) - 1][int(Y_bus_df.Col[idx]) - 1] = ybus[int(Y_bus_df.Col[idx]) - 1][
            int(Y_bus_df.Row[idx]) - 1] = complex(float(Y_bus_df.G[idx]), float(Y_bus_df.B[idx]))

    return ybus, node_name


if __name__ == '__main__':

    IEEE_systems = ["IEEE_13", "IEEE_34", "IEEE_37", "IEEE_123"]

    ieee_sys = IEEE_systems[1]

    if ieee_sys == "IEEE_13":
        master_file_name = "IEEE13Nodeckt.dss"
        ckt_name = "ieee13"
    elif ieee_sys == "IEEE_34":
        master_file_name = "ieee34.dss"
        ckt_name = "test_34"
    elif ieee_sys == "IEEE_37":
        master_file_name = "ieee37.dss"
        ckt_name = "ieee37"
    elif ieee_sys == "IEEE_123":
        master_file_name = "master_new_secondary_loads.dss"
        ckt_name = "ieee123"

    master_file_name = "test_3_node.dss"
    ckt_name = "3_node"
    path = os.getcwd()
    master_file_loc = os.path.abspath(master_file_name)

    DSSObj_Y_bus = DSS(master_file_loc)
    Y_bus_filename = "base_ysparse.csv"
    Y_node_filename = "base_nodelist.csv"
    ybus, node_name = get_Y_Bus_info(DSSObj_Y_bus, Y_bus_filename, Y_node_filename)

    os.chdir(path)
    DSSObj = DSS(master_file_loc)
    All_nodes = list(DSSObj.circuit.AllNodeNames)
    n = DSSObj.circuit.NumBuses
    # Generators = DSSObj.circuit.PVsystems.AllNames
    Generators = DSSObj.circuit.Generators.AllNames
    Loads = DSSObj.circuit.Loads.AllNames

    # Bus_info Initialization:
    bus_info = {}
    bus_idx = 0
    node_idx = 0
    for i in range(0, n):
        bus = DSSObj.circuit.Buses(i)
        name = bus.Name

        bus_info[name] = {}
        bus_info[name]['idx'] = bus_idx
        bus_info[name]['kv'] = bus.kVBase
        bus_info[name]['phases'] = [str(phase) for phase in bus.Nodes]
        bus_info[name]['nodes'] = [node_idx + (i) for i in range(len(bus.Nodes))]
        if bus.kVBase > 0.4:
            bus_info[name]['pq'] = [[0, 0], [0, 0], [0, 0]]
            bus_info[name]['pv'] = [[0, 0], [0, 0], [0, 0]]
        else:
            bus_info[name]['pq'] = [0, 0]
            bus_info[name]['pv'] = [0, 0]
        bus_idx += 1
        node_idx += len(bus.Nodes)

    print('Extracting Bus PV information')
    if Generators != ('NONE',):
        for i in range(len(Generators)):
            if i == 0:
                DSSObj.circuit.Generators.First
            else:
                DSSObj.circuit.Generators.Next
            bus_name_phase = DSSObj.circuit.ActiveCktElement.BusNames[0].split('.')
            bus_name = bus_name_phase[0]
            bus_phase = np.int_(bus_name_phase[1:])

            bus_powers = np.round(np.array(DSSObj.circuit.ActiveCktElement.Powers), 2)[:-2]
            idx = 0
            if bus_info[bus_name]['kv'] > 0.4:
                for ph in bus_phase:
                    bus_info[bus_name]['pv'][ph - 1] = [-1 * bus_powers[idx] * 1000, -1 * bus_powers[idx + 1] * 1000]
                    idx += 2
            else:
                bus_info[bus_name]['pv'][0] = -1 * bus_powers[0] * 1000 + -1 * bus_powers[2] * 1000
                bus_info[bus_name]['pv'][1] = 0

    print('Extracting Bus PQ information')
    for i in range(len(Loads)):
        if i == 0:
            DSSObj.circuit.Loads.First
        else:
            DSSObj.circuit.Loads.Next
        bus_name_phase = DSSObj.circuit.ActiveCktElement.BusNames[0].split('.')
        bus_name = bus_name_phase[0]
        bus_phase = np.int_(bus_name_phase[1:])
        bus_powers = np.round(np.array(DSSObj.circuit.ActiveCktElement.Powers), 2)

        idx = 0
        if bus_info[bus_name]['kv'] > 0.4:
            for ph in bus_phase:
                bus_info[bus_name]['pq'][ph - 1] = [bus_powers[idx] * 1000, bus_powers[idx + 1] * 1000]
                idx += 2
        else:
            bus_info[bus_name]['pq'][0] = bus_powers[0] * 1000 + bus_powers[2] * 1000
            bus_info[bus_name]['pq'][1] = bus_powers[1] * 1000 + bus_powers[3] * 1000


    xfmr = DSSObj.circuit.Transformers
    print('Extracting branch information')
    no_el = DSSObj.circuit.NumCktElements
    branch_sw_data = {}
    idx_line = 0

    # --------------------------------------
    # Create a list of OPEN lines/switches
    # open_sw = ['sw7', 'sw8']
    open_sw = []
    # --------------------------------------

    primary_kv = 0.01

    for j in range(0, no_el):
        el = DSSObj.circuit.CktElements(j)
        if not re.search("^Line", el.Name):
            continue  # only pick lines...

        line_name = (el.Name).split(".")[1]
        # print(line_name)
        branch_sw_data[line_name] = {}
        branch_sw_data[line_name]['idx'] = idx_line
        bus1 = DSSObj.circuit.Buses(re.sub(r"\..*", "", el.BusNames[0])).Name
        bus2 = DSSObj.circuit.Buses(re.sub(r"\..*", "", el.BusNames[-1])).Name
        ph = np.unique(el.NodeOrder, axis=0)
        if bus_info[bus1]['kv'] > primary_kv:
            branch_sw_data[line_name]['type'] = 'LINE'
            value = np.empty((), dtype=object)
            value[()] = (0, 0)
            z_prim = np.full((3, 3), value, dtype=object)
            ph = ph.tolist()
        else:
            branch_sw_data[line_name]['type'] = 'TPX_LINE'
            xfmr.name = 'xf' + line_name.split('_')[0]
            branch_sw_data[line_name]['xfmr_rating'] = xfmr.kva
            z_prim = np.zeros((2, 2), dtype=tuple)
            ph = [1, 2]

        # # print(obj['phases']['value'])
        branch_sw_data[line_name]['phases'] = ph
        branch_sw_data[line_name]['from'] = bus_info[bus1]['idx']
        branch_sw_data[line_name]['to'] = bus_info[bus2]['idx']
        branch_sw_data[line_name]['fr_bus'] = bus1
        branch_sw_data[line_name]['to_bus'] = bus2
        fr_node = []
        t_node = []
        for p in ph:
            from_node = bus1.upper() + '.' + str(p)
            to_node = bus2.upper() + '.' + str(p)
            fr_node.append(node_name[from_node])
            t_node.append(node_name[to_node])
        if line_name not in open_sw:
            z = -1 * np.linalg.inv(ybus[np.ix_(fr_node, t_node)])
            # Making the matrix 3 x 3 for non 3-phase line
            for p in range(len(ph)):
                for q in range(len(ph)):
                    z_prim[ph[p] - 1][ph[q] - 1] = [z[p][q].real, z[p][q].imag]
        branch_sw_data[line_name]['zprim'] = z_prim.tolist()
        idx_line += 1

    no_el = DSSObj.circuit.NumCktElements

    # --------------------------------------

    # regs = ['reg3c', 'reg4b', 'reg4c']   # reg of other phases than a
    # regs = ['reg1b','reg1c','reg2b','reg2c']
    regs = []

    # --------------------------------------

    for j in range(0, no_el):
        el = DSSObj.circuit.CktElements(j)
        if not re.search("^Transformer", el.Name):
            continue  # only pick transformer...
        line_name = (el.Name).split(".")[1]
        if line_name not in regs:
            xfmr.name = line_name
            branch_sw_data[line_name] = {}
            branch_sw_data[line_name]['idx'] = idx_line
            bus1 = DSSObj.circuit.Buses(re.sub(r"\..*", "", el.BusNames[0])).Name
            bus2 = DSSObj.circuit.Buses(re.sub(r"\..*", "", el.BusNames[-1])).Name

            branch_sw_data[line_name]['from'] = bus_info[bus1]['idx']
            branch_sw_data[line_name]['to'] = bus_info[bus2]['idx']
            branch_sw_data[line_name]['fr_bus'] = bus1
            branch_sw_data[line_name]['to_bus'] = bus2
            ph = np.unique(el.NodeOrder, axis=0)
            if bus_info[bus2]['kv'] > primary_kv:
                branch_sw_data[line_name]['type'] = 'XFMR'
                ph = np.unique(el.NodeOrder, axis=0)
                branch_sw_data[line_name]['phases'] = [1, 2, 3]
                value = np.empty((), dtype=object)
                value[()] = (0, 0)
                z_prim = np.full((3, 3), value, dtype=object)
                branch_sw_data[line_name]['zprim'] = z_prim.tolist()
            else:
                branch_sw_data[line_name]['type'] = 'SPLIT_PHASE'
                branch_sw_data[line_name]['phases'] = [1, 2]
                branch_sw_data[line_name]['impedance'] = [xfmr.r/2, 0.5 * (xfmr.xhl + xfmr.xht - xfmr.xlt)]
                branch_sw_data[line_name]['impedance1'] = [xfmr.r, 0.5 * (xfmr.xhl + xfmr.xlt - xfmr.xht)]
            idx_line += 1



    network_file_location = "..\..\\ckts"

    # --------------------------------------
    # f_name = 'bus_info_test_34.json'
    f_name = "bus_info_"+ckt_name+".json"
    # --------------------------------------

    json_fp = open(os.path.join(network_file_location, f_name), 'w')
    json.dump(bus_info, json_fp, indent=2)
    json_fp.close()

    # --------------------------------------
    # f_name = 'branch_info_test_34.json'
    f_name = "branch_info_" + ckt_name + ".json"
    # --------------------------------------

    json_fp = open(os.path.join(network_file_location, f_name), 'w')
    json.dump(branch_sw_data, json_fp, indent=2)
    json_fp.close()

