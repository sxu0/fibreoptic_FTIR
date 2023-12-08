import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_data(filename):
    wavelength, attenuation = np.loadtxt(filename, delimiter=',', skiprows=2, unpack=True)
    return wavelength, attenuation

def load_spectrum(filename):
    channel, reading = np.loadtxt(filename, delimiter=',', unpack=True)
    return channel, reading

def wavelen2wavenum(wavelength):
    return 1 / (wavelength / 1e7)

def transmission(attenuation, length):
    '''
    attenuation in dB/km
    length in m
    '''
    total_att = -attenuation / 1e3 * length  # dB
    transmission = np.exp(total_att / 10) * 100  # percent
    return transmission


if __name__ == "__main__":
    wl, a = load_data('TECS_0.22_NA_Low_OH.csv')
    wn = wavelen2wavenum(wl)

    plt.figure()
    plt.semilogy(wn, a)
    plt.xlabel('wavenumber [cm$^{-1}$]')
    plt.ylabel('attenuation [dB/km]')
    plt.title('fibre attenuation')

    T = transmission(a, 2.0)

    plt.figure()
    plt.plot(wn, T)
    plt.xlabel('wavenumber [cm$^{-1}$]')
    plt.ylabel('transmission [%]')
    plt.title('fibre transmission')

    data_folder = Path.cwd() / 'data'
    spectra_files, ifg_files = [], []
    for file in data_folder.iterdir():
        if 'ifg' in file.name and 'transformedspectrum' not in file.name.lower():
            ifg_files.append(file)
        else:
            spectra_files.append(file)

    spectra_chnls, spectra_ampls = [], []
    for i in range(len(spectra_files)):
        chnl, ampl = load_spectrum(spectra_files[i])
        spectra_chnls.append(chnl)
        spectra_ampls.append(ampl)

    plt.figure()
    for i in range(len(spectra_files)):
        plt.plot(spectra_chnls[i], spectra_ampls[i], linewidth=0.5, label=spectra_files[i].name)
    # not sure what the units are yet
    plt.legend()

    ifg_chnls, ifg_ampls = [], []
    for i in range(len(ifg_files)):
        chnl, ampl = load_spectrum(ifg_files[i])
        ifg_chnls.append(chnl)
        ifg_ampls.append(ampl)

    plt.figure()
    for i in range(len(ifg_files)):
        plt.plot(ifg_chnls[i], ifg_ampls[i], linewidth=0.5, label=ifg_files[i].name)
    # not sure what the units are yet
    plt.legend()

    plt.show()
