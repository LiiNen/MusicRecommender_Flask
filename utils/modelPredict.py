import torch
import pandas as pd
import numpy as np
import xgboost
from sklearn.preprocessing import MinMaxScaler

feature_list=[]
feature_name = ['chroma', 'rms', 'spectral_centroid', 'spectral_bandwidth', 'spectral_rolloff', 'zero_crossing_rate', 'harmony', 'perceptr']
for feature in feature_name:
    feature_list.append(feature + '_mean')
    feature_list.append(feature + '_var')
feature_list.append('bpm')

xgb_PATH='./model/xgb_2.tar'
K_Fold_PATH='./model/K_Fold_2.tar'
xgb=torch.load(xgb_PATH)
csv_PATH='./model/result50_2.csv'
df = pd.read_csv(csv_PATH)

K_Fold=torch.load(K_Fold_PATH)

def modelPredict(search_type):
    droplist = []
    for i in range(1, 21):
        droplist.append('mfccs_' + str(i) + '_mean')
        droplist.append('mfccs_' + str(i) + '_var')
    if search_type == 'upload':
        output_path='./static/output.csv'
        output_df = pd.read_csv(output_path)
        output_df = output_df.drop(droplist, axis=1)

        dataset = pd.read_csv('./utils/dataset_new.csv')
        dataset = dataset.drop(columns=['filename', 'length'])
        dataset = dataset.drop(droplist, axis=1)
        scaler = MinMaxScaler()
        scaler.fit(dataset)

        scaled_df = scaler.transform(output_df)

        return RF(scaled_df)
    else:
        music_id = search_type.split('_')[0]
        for i in range(0, len(df)):
            if str(df.iloc[i]['Index']).zfill(4) == music_id:
                print('fiond!')
                break
            if i == len(df) - 1:
                return []
        
        output_df = df.iloc[[i]].copy()
        output_df = output_df.drop(columns=['filename', 'Index'])
        print(output_df)
        return RF(output_df)

def XGB(data):
    input_df=pd.DataFrame(data, columns=feature_list)
    cluster=xgb.predict(input_df)[0]
    recommends_df=df[df['Cluster']==cluster]
    recommends=list(np.array(recommends_df['filename']))
    return recommends

def RF(data):
    df = pd.read_csv(csv_PATH)

    input_df=pd.DataFrame(data, columns=feature_list)
    cluster=K_Fold.predict(input_df)[0]
    recommends_df=df[df['Cluster']==cluster]
    recommends=list(np.array(recommends_df['filename']))
    print(cluster)
    return recommends