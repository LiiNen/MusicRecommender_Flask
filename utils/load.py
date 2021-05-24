import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import sklearn
from glob import glob
import spleeter
from tqdm import tqdm
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns
from scipy.spatial.distance import cdist

def getMusicList():
    data = pd.read_csv('dataset.csv', encoding='cp949')
    music_list = data['filename'].values.tolist()

    return music_list

if __name__ == '__main__':
    getMusicList()