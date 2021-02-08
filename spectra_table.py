### Read the original Spitzer spectra and format to the deblendIRS table
### Initial Date: 2021.02.03, v0.01

import numpy as np
from astropy.table import Table
from astropy.io import ascii
import os
import pandas as pd
import glob


class Spec():
    def __init__(self, key=None, wave=None, flux=None, err=None):
        
        self.key = key
        self.flux = flux
        self.wave = wave
        self.err = err
       

    def resampleSpec(self, wave=None, flux=None,err=None, startwave=None, endwave=None, num=None):
        
        """
        Resample 1D spectrum which contains wavelength, flux and error.

        Parameters
        ----------

        wave: 'numpy.ndarray'
               The wavelength of 1D spectrum
        flux: 'numpy. ndarray'
               The flux of 1D spectrum
        err: 'numpy.ndarray'
              The error of 1D spectrum
        startwave: float
              The selected start wavelength to be resampled
        endwave: float
              The selected end wavelength to be resampled
        num: int
             The number of elements contains to be resampled
  
        """

        self.wave = wave
        self.flux = flux
        self.err = err
        wave_val = np.linspace(startwave,endwave,num)
        flux_val = np.interp(wave_val, self.wave, self.flux)
        err_val = np.interp(wave_val, self.wave, (self.flux + self.err)) - flux_val
        test_num = wave_val
            

        return wave_val, flux_val, err_val
    
    def loadTxtData(self, filename=None):

        """
        Load input files in txt/dat data with ipac table format

        Parameters
        ----------

        filename: 'string'
                  Name or Path of the input data table with ipac table format.

        """

        file_in = Table.read(filename, format='ipac')
        key = file_in.meta['keywords'].get('AORKEY').get('value')
        self.key = key[0:9].strip()
        self.wave = file_in['wavelength']
        self.flux = file_in['flux_density']
        self.err = file_in['error']

    def writeTxtData(self, filename=None, wave=None, flux=None, err=None):

        """
        write output files in data with ascii format

        Parameters
        ----------

        filename: 'string'
                  Name or Path of the input data table with ascii format.
        wave: 'numpy.ndarray'
              The wavelength of 1D spectrum
        flux: 'numpy. ndarray'
               The flux of 1D spectrum
        err: 'numpy.ndarray'
              The error of 1D spectrum

        """

        self.wave = wave
        self.flux = flux
        self.err = err
        file_out = {'# wave': self.wave, 'flux': self.flux, 'error': self.err}
        df_file_out = pd.DataFrame(file_out)
        df_file_out.to_csv(filename + '.ascii', sep='\t', index=0)
        




# test files

if __name__ == '__main__':

    path = '/Users/m.lam/MIR_H2/water_megamaser_H2/water_spectra/masers_spectra/'
    dirs = glob.glob(path+'**/' + 'enhanced/*.tbl')

    inputdata = Spec()

    for filename in dirs:
        if 'SPITZER_S5' in filename:

            inputdata.loadTxtData(filename)

            output_wave, output_flux, output_err = inputdata.resampleSpec(inputdata.wave, inputdata.flux, inputdata.err, startwave=5, endwave=35, num=len(inputdata.wave))

            print(output_wave.shape)
            print(min(output_wave),max(output_wave))
            print(min(inputdata.wave),max(inputdata.wave))

            inputdata.writeTxtData(filename= path + 'test2/' + inputdata.key, wave=output_wave, flux=output_flux, err=output_err)
        

