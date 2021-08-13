### Read the original Spitzer spectra and format to the deblendIRS table
### Initial Date: 2021.07.12, v0.01

import numpy as np
from astropy.table import Table
from astropy.io import ascii
import os
import pandas as pd
import glob
import copy

class FluxTable():

    def __init__(self, key=None, name=None,wave=None,amp=None):

        self.key = key
        self.name = name
        self.wave = wave
        self.amp = amp

    
    def loadIpacData(self, filename=None):

        """
        Load input files in txt/dat data with ipac table format

        Parameters
        ----------

        filename: 'string'
                  Name or Path of the input data table with ipac table format.

        """


        file_in = Table.read(filename, format='ipac')
        self.name = file_in['Name']
        self.wave = file_in['x_0']
        self.amp = file_in['amp']

    #def UnitConversion(self, flux=None, z=None):

        
    

# test files

if __name__ == '__main__':

    path = '/Users/m.lam/MIR_H2/water_megamaser_H2/water_spectra/masers_spectra/resample_new/'
    dirs = glob.glob(path+'*.ipac')

    inputdata = FluxTable()
    key, flux = [], []    
    table_column = []
    table_row = []

    for filename in dirs:
        if 'output' in filename:
            inputdata.loadIpacData(filename)
            oldkey = copy.copy(filename)
            oldkey1 = oldkey.replace(path,'')
            key.append(oldkey1.replace('_output.ipac',''))
            table_row.append(list(inputdata.amp))
            
       
    df = pd.DataFrame(table_row, columns=inputdata.name)
    df.insert(0,'#aorkey',key, True)
    df.to_csv(path + 'control_flux_test' + '.csv', sep=',', index=0)
    

        
    

