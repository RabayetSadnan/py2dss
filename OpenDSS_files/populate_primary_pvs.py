# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 11:47:47 2021

@author: poud579
"""

import random

n_load = 0
n_pv = 0
# pv_f = open('pv_with_loads.dss', 'w')
# with open('IEEE123Loads.dss') as f:
pv_f = open('pv_with_loads_34.dss', 'w')
with open('IEEE34Loads.dss') as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        if line.strip():
            line_list = line.split()
            if line_list[0] == 'New':
                n_load += 1
                kw = float(line_list[7].split('=')[1])
                kv = line_list[6]
                ld_name = line_list[1].split('.')[1]
                bus = line_list[2]
                rand = random.random()
                if rand <= 0.90:
                    n_pv += 1
                    kwh_mul = 3 + random.random()
                    # pv_f.write('New PVsystem.PV_' + ld_name + ' ' + bus + ' Phases=1 kV=2.4 kVA=' + str(kw) +
                    #            ' Pmpp=' + str(kw) + ' PF=1 irradiance=1' + '\n')
                    # pv_f.write('New Generator.DG_' + ld_name + ' ' + bus + ' Phases=1  '+ kv + '  kW=' + str(kw) +
                    #            ' kvar=' + str(0) + ' model=1 Vmaxpu=2.0 Vminpu=0.1 ' + '\n')
                    pv_f.write('New Generator.DG_' + ld_name + ' ' + bus + "   "+ line_list[3] + "  " + kv + '  kW=' + str(kw) +
                               ' kvar=' + str(0) + ' model=1 Vmaxpu=2.0 Vminpu=0.1 ' + '\n')

print(n_load, n_pv)
pv_f.close()

