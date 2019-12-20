import io
import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp


def load_mocap_csv(file):
    with open(file, 'r') as f:
        lines = f.read().split('\n')

    data = pd.read_csv(io.BytesIO('\n'.join(lines[3:]).encode()))
    data = data.rename(columns={'Unnamed: 0': 'Frame',
                                'Unnamed: 1': 'Time', 
                                'capo': 'capo.a', 
                                'capo.1': 'capo.b',
                                'capo.2': 'capo.c', 
                                'capo.3': 'capo.d',
                                'capo.4': 'capo.x',
                                'capo.5': 'capo.y', 
                                'capo.6': 'capo.z', 
                                'capo.7': 'capo.Error Per Marker', 
                                'caps': 'caps.a', 
                                'caps.1': 'caps.b',
                                'caps.2': 'caps.c', 
                                'caps.3': 'caps.d',
                                'caps.4': 'caps.x',
                                'caps.5': 'caps.y',
                                'caps.6': 'caps.z',
                                'caps.7': 'caps.Error Per Marker'})
    data = data.loc[:, ['Frame', 'Time', 'capo.a', 'capo.b', 'capo.c', 'capo.d', 'capo.x', 'capo.y', 'capo.z', 'capo.Error Per Marker', 'caps.a', 'caps.b', 'caps.c', 'caps.d', 'caps.x', 'caps.y', 'caps.z', 'caps.Error Per Marker']]
    data = data.iloc[3:]
    data = data.set_index('Frame')
    data = data.astype(float)
    data.index = data.index.astype(int)
    
    return data

#data = load_mocap_csv('Take 2019-12-08 05.03.55 PM Pose 1.csv')
#data = load_mocap_csv('human_data/pose1a.csv')
#print(data.head())
#print(data.iloc[0, 1])

#sns.heatmap(data.isnull(), cbar=False);
def euclidean_distance(first_pos, second_pos):
    if ((len(first_pos) != 3) or (len(second_pos) != 3)):
        print("Pos argument is incomplete")
        return None
    return ((first_pos[0] - second_pos[0])^2 + (first_pos[1] - second_pos[1])^2 + (first_pos[2] - second_pos[2])^2)^0.5

def get_min_distance(data):
    min_dist = 100
    for i in range(len(data.index)):
        o_x = data.iloc[i, 5]
        o_z = data.iloc[i, 7]

        s_x = data.iloc[i, 13]
        s_z = data.iloc[i, 15]

        if np.isnan(o_x) or np.isnan(o_z) or np.isnan(s_x) or np.isnan(s_z):
            continue

        #dist = euclidean_distance([o_x, 0, o_z], [s_x, 0, s_z])
        dist = sp.spatial.distance.euclidean([o_x, o_z], [s_x, s_z])
        min_dist = min(dist, min_dist)
    #print("Minimum distance is ", min_dist)
    return min_dist

def get_xz_one_agent(data):
    ''' Takes in dataframe data that has the cleaned data from OptiTrack
    '''
    list_of_positions = []
    for i in range(len(data.index)):
        time = data.iloc[i][0]
        o_x = data.iloc[i][5]
        o_z = data.iloc[i][7]
        if np.isnan(o_x) or np.isnan(o_z):
            continue
        tupl = (time, o_x, o_z)
        print(tupl)
        
        list_of_positions.append((time, o_x, o_z))
    
    #print(list_of_positions)
    #print("Length: ", len(list_of_positions))
    return list_of_positions
        
print(get_min_distance(data))
print(get_xz_one_agent(data))

