# mmwave-python-api

This repo contains several scripts to save, read and parse raw data from DCA1000 EVM from Texas Instruments using compatible mmWave radar boards (60GHz and 77GHz) such as XWR12xx, XRW14xx, XWR16xx, xWR6843 and xWR1843.

# Acknowledgments

The `dca1000.py` script is a modified version from the [openradar](https://github.com/PreSenseRadar/OpenRadar) library to automatically read configuration parameters from lua script file and convert radar data from two's complement to int16.

# Installation

- Simply copy this folder wherever you prefer and copy lua script from `mmWave Studio Scripts` folder to `MMWAVE_STUDIO_INSTALLATION_PATH\mmWaveStudio\Scripts` and load it using mmWave Studio. No connection or reset is required as it is done in the script.
- Modify PARAMS class to point to your config file (change mmwave studio path if needed)

# Configuration

Modify emission and radar parameters in lua script and they will be automatically loaded in `PARAMS` class in Python.

By default, infinite measuring mode is used (number of frames set to 0). Three transmission antennas are configured and chirp emissions are in the order TX1 -> TX3 -> TX2. This can be changed in chirps configuration enabling or disabling TX antennas.

# Saving data

An example script is provided to save data frames and the parameters used to configure the radar. Data is saved using `pickle` library.

# Reading data

A reading script is provided to return the radar data cube as a NumPy array with the shape `(numChirpsPerFrame, numVxAntennas, numADCSamples)` where each chirp contains the following `numVxAntennas` arrays:

```
[ [TX1-RX1], [TX1-RX2], [TX1-RX3], [TX1-RX4], [TX3-RX1], [TX3-RX2], ... , [TX2-RX4] ]
```

Each `[TXa-RXb]` array is the signal emitted by TX antenna `a` received on RX antenna `b` with a total of `numADCSamples` samples.
