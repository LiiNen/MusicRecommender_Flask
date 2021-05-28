import os
import librosa
import IPython.display as ipd
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import csv
import sklearn
import spleeter

def getFeature():
    feature_name = ['chroma', 'rms', 'spectral_centroid', 'spectral_bandwidth', 'spectral_rolloff', 'zero_crossing_rate', 'harmony', 'perceptr']
    for i in  range(1, 21):
        feature_name.append('mfccs_' + str(i))
    feature_list = ['filename', 'length']
    for feature in feature_name:
        feature_list.append(feature + '_mean')
        feature_list.append(feature + '_var')
    feature_list.append('bpm')

    y, sr = librosa.load('static/output.wav')
    chromagram = librosa.feature.chroma_stft(y, sr=sr, hop_length=512)
    rms = librosa.feature.rms(y)[0]
    spectral_centroids = librosa.feature.spectral_centroid(y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y, sr=sr)[0]
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
    y_harm, y_perc = librosa.effects.hpss(y)
    bpm, _ = librosa.beat.beat_track(y, sr=sr)
    mfccs = librosa.feature.mfcc(y, sr=sr)
    mfccs = sklearn.preprocessing.minmax_scale(mfccs, axis=1)
    data_list = [chromagram, rms, spectral_centroids, spectral_bandwidth, spectral_rolloff, \
                zero_crossing_rate, y_harm, y_perc]

    filename = 'upload_output'
    row = [str(filename), str(len(y)), str(bpm)]

    for data in data_list:
        row.append(str(np.mean(data)))
        row.append(str(np.var(data)))
    for i in range(1, 21):
        row.append(str(mfccs[i-1].mean()))
        row.append(str(mfccs[i-1].var()))

    print(row)
    return