import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    wavelength, attenuation = np.loadtxt(filename, delimiter=',', skiprows=2, unpack=True)
    return wavelength, attenuation

def load_spectra(filename):
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

    spectra_files = ['tb202311202054s0d00x.0000.dpt',
                     'tb202311202054s0d00x.0000-2.dpt',
                     'tb202311221836s0d00x.0004.dpt']

    chnls, ampls = [], []
    for i in range(len(spectra_files)):
        chnl, ampl = load_spectra(spectra_files[i])
        chnls.append(chnl)
        ampls.append(ampl)

    plt.figure()
    for i in range(len(spectra_files)):
        plt.plot(chnls[i], ampls[i], linewidth=0.5, label=spectra_files[i])
    # not sure what the units are yet
    plt.legend()

    plt.show()
