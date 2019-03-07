# -*- coding: utf-8 -*-
import numpy as np

from raincoat.scatTable import water
from raincoat.scatTable.TMMrain import scatTable
from pytmatrix import tmatrix_aux

frequencies = [94.0]
temperatures = [273.15]
sizes = np.arange(0.01, 8.5, 0.01)

for T in temperatures:
	for f in frequencies:
		table = scatTable(frequency=f,
						  n=water.n(T, f*1.e9),
						  sizes=sizes,
						  canting=10.0,
						  elevation=90.0,
						  aspect_ratio_func=tmatrix_aux.dsr_thurai_2007)

		table.compute(verbose=True, procs=1)
		table.save_text_scat_table(str(T) + '_' + str(f) + 'GHz.csv')