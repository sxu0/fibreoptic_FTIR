import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_spectrum(filename):
    channel, reading = np.loadtxt(filename, delimiter=',', unpack=True)
    return channel, reading

if __name__ == "__main__":
    data_folder = Path.cwd() / 'data'
    spectra_files, ifg_files = [], []
    for file in data_folder.iterdir():
        if 'ifg' in file.name and 'transformedspectrum' not in file.name.lower():
            ifg_files.append(file)
        else:
            spectra_files.append(file)

    spectra_chnls, spectra_ampls = [], []
    spectra_chnls_co, spectra_ampls_co = [], []
    spectra_files_co = []
    for i in range(len(spectra_files)):
        chnl, ampl = load_spectrum(spectra_files[i])
        if chnl[np.argmax(ampl)] < 5000:
            spectra_chnls_co.append(chnl)
            spectra_ampls_co.append(ampl)
            spectra_files_co.append(spectra_files[i])
        else:
            spectra_chnls.append(chnl)
            spectra_ampls.append(ampl)
    spectra_files = [file for file in spectra_files if file not in spectra_files_co]

    plt.figure(figsize=(8, 4))
    for i in range(len(spectra_files)):
        plt.plot(spectra_chnls[i], spectra_ampls[i],
                 linewidth=0.5, label=spectra_files[i].name)
    # not sure what the units are yet
    plt.title('transformed spectra')
    plt.legend(loc='upper right')  # bbox_to_anchor=(1, 1)

    plt.figure(figsize=(8, 4))
    for i in range(len(spectra_files_co)):
        plt.plot(spectra_chnls_co[i], spectra_ampls_co[i],
                 linewidth=0.5, label=spectra_files_co[i].name)
    # not sure what the units are yet
    plt.title('transformed spectra, CO channel')
    plt.legend(loc='upper right')

    ifg_chnls, ifg_ampls = [], []
    for i in range(len(ifg_files)):
        chnl, ampl = load_spectrum(ifg_files[i])
        ifg_chnls.append(chnl)
        ifg_ampls.append(ampl)

    plt.figure(figsize=(8, 4))
    for i in range(len(ifg_files)):
        plt.plot(ifg_chnls[i], ifg_ampls[i], linewidth=0.5, label=ifg_files[i].name)
    # not sure what the units are yet
    plt.title('interferograms')
    plt.legend(loc='upper right')

    plt.show()
