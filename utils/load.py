import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import sklearn
from glob import glob
from tqdm import tqdm
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

data = pd.read_csv('dataset.csv', encoding='cp949')

def getMusicList():    
    music_list = data['filename'].values.tolist()
    return music_list

def getMusicInfo(music_name):
    music_info = data[(data['filename'] == music_name)]
    if len(music_info) == 0:
        return 'not exist'
    music_info = music_info.to_json()
    return music_info

if __name__ == '__main__':
    getMusicList()