"""

HEATMAPS GENERATION
===================

Included functions:
    - Range Heatmap
    - Doppler-Range Heatmap
    - Azimuth-Range Heatmap
    - Elevation-Range Heatmap

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dca1000 import DCA1000

from params import PARAMS
from fourier import rangeFFT, dopplerFFT, azimuthFFT, elevationFFT


def generateRangeHeatmap(raw_data):
    # Average antennas
    avg = np.mean(raw_data, axis=1)

    # Only keeping positive ranges
    matrix = np.zeros((avg.shape[0], avg.shape[1]//2), dtype=complex)

    # Do FFT along each chirp's samples (range)
    # Shift zero freq.
    for i in range(avg.shape[0]):
        matrix[i, :], bins = rangeFFT(avg[i])

    # Find vertical bins
    chirps = np.arange(avg.shape[0])

    return bins, chirps, matrix


def generateDopplerRangeHeatmap(raw_data):
    # Average antennas
    avg = np.mean(raw_data, axis=1)

    matrix = np.zeros((avg.shape[0], avg.shape[1]//2), dtype=complex)

    # Do FFT along each chirp's samples (range)
    for i in range(avg.shape[0]):
        matrix[i, :], range_bins = rangeFFT(avg[i])

    # Do FFT along chirps (doppler)
    for i in range(avg.shape[1]//2):
        matrix[:, i], doppler_bins = dopplerFFT(matrix[:, i])

    return range_bins, doppler_bins, matrix


def generateAzimuthRangeHeatmap(raw_data):
    # TX emissions are in the order TX1->TX3->TX2, and TX1,TX3 are
    # in the same horizontal line. Thus, these are used for azimuth.
    # Then for each chirp, the first 8 VX antennas are for azimuth

    avg = np.mean(raw_data[:, :8, :], axis=0)

    matrix = np.zeros((PARAMS.NUM_AZIM_BINS, avg.shape[1]//2), dtype=complex)

    # Do FFT along each chirp's samples (range)
    for i in range(avg.shape[0]):
        matrix[i, :], range_bins = rangeFFT(avg[i])

    # Do FFT along antennas (azimuth)
    for i in range(avg.shape[1]//2):
        matrix[:, i], azimuth_bins = azimuthFFT(matrix[:, i])

    # Angular resolution is not at > 75 degrees, we remove the first
    # bin to remove -90 degrees and keep the rest
    return range_bins, azimuth_bins[1:], matrix[1:]


def generateElevationRangeHeatmap(raw_data):
    # TX emissions are in the order TX1->TX3->TX2. For elevation,
    # chirps from TX1 and TX3 can be averaged and concatenated with
    # chirp from TX2.
    # Then for each chirp, the first 8 VX antennas are for azimuth
    # and the mean of all these with the remainder 9, 10 11 and 12 VX
    # antennas are for elevation

    avg = np.mean(raw_data, axis=0)

    avg = np.concatenate([(avg[:4] + avg[4:8])/2, avg[8:]])

    matrix = np.zeros((PARAMS.NUM_ELEV_BINS, avg.shape[1]//2), dtype=complex)

    # Do FFT along each chirp's samples (range)
    for i in range(avg.shape[0]):
        matrix[i, :], range_bins = rangeFFT(avg[i])

    # Do FFT along antennas (elevation)
    for i in range(avg.shape[1]//2):
        matrix[:, i], elevation_bins = elevationFFT(matrix[:, i])

    return range_bins, elevation_bins[1:], matrix[1:]


def plotRangeHeatmap(signal):
    '''
    Plot range heatmap
    '''

    bins, chirps, matrix = generateRangeHeatmap(signal)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(bins, chirps, np.abs(matrix))
    fig.colorbar(c, ax=ax)
    ax.set_title('Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Chirp #')

    plt.show()

    return matrix


def plotDopplerRangeHeatmap(raw_data):
    '''
    Plot Doppler-Range heatmap
    '''
    range_bins, doppler_bins, matrix = generateDopplerRangeHeatmap(raw_data)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, doppler_bins, np.abs(matrix))
    fig.colorbar(c, ax=ax)
    ax.set_title('Doppler-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Doppler (m/s)')

    plt.show()

    return matrix


def plotAzimuthRangeHeatmap(raw_data):
    '''
    Plot Azimuth-Range heatmap
    '''

    range_bins, azimuth_bins, matrix = generateAzimuthRangeHeatmap(raw_data)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, azimuth_bins, np.abs(matrix))
    fig.colorbar(c, ax=ax)
    ax.set_title('Azimuth-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Azimuth (°)')

    plt.show()

    return matrix


def plotElevationRangeHeatmap(raw_data):
    '''
    Plot Elevation-Range heatmap
    '''

    range_bins, elevation_bins, matrix = generateElevationRangeHeatmap(
        raw_data)

    fig, ax = plt.subplots()

    c = ax.pcolormesh(range_bins, elevation_bins, np.abs(matrix))
    fig.colorbar(c, ax=ax)
    ax.set_title('Elevation-Range Heatmap')
    ax.set_xlabel('Range (m)')
    ax.set_ylabel('Elevation (°)')

    plt.show()

    return matrix