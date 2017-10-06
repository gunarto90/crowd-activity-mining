#!/usr/bin/env python
"""
Developed by Gunarto Sindoro Njoo
v.0.1 [5 Oct 2017 ]
Libraries required:
- json
- pandas
- numpy
"""
### General libraries
import json
import pandas as pd
### Custom libraries
import functions

### Configuration
RESOLUTION = 1000    ### N-digits of decimals   (3 digits = Street/Neigborhood (100m), 4 digits = Land parcel(10m))
def read_config(filename='config.json'):
    try:
        with open(filename) as data_file:
            config = json.load(data_file)
            return config
    except Exception as ex:
        print('Exception in init config file : %s' % ex)
        return None

### Main function ###
if __name__ == '__main__':
    config = read_config()
    dataset = config['dataset']
    active_dataset = config['active_dataset']
    general_folder = config['dataset_processed_folder']
    for d in active_dataset:
        print(d)
        dataset_folder = '/'.join((general_folder, config[d]['folder']))
        checkin_file = config[d].get('checkin')
        user_file = config[d].get('user')
        venue_file = config[d].get('venue')
        category_file = config[d].get('category')
        delimiter = config[d].get('delimiter')
        header = config[d].get('header')

        users = pd.read_csv('/'.join((dataset_folder, user_file)), header=None, delimiter=',', encoding='latin-1')
        # print(users.head())
        print(users.shape)
        # print(users.dtypes)

        checkins = pd.read_csv('/'.join((dataset_folder, checkin_file)), header=None, names=['UID', 'VID', 'CID', 'category', 'latitude', 'longitude', 'timestamp'], delimiter=',', encoding='latin-1')
        checkins['lat_norm'] = checkins.apply(lambda row: int(float(row[5])*RESOLUTION), axis=1)
        checkins['lon_norm'] = checkins.apply(lambda row: int(float(row[6])*RESOLUTION), axis=1)
        # checkins.sort_values(by=['UID', 'timestamp'], inplace=True)
        print(checkins.head())
        print(checkins.shape)
        print(checkins.dtypes)

        ### Put all checkins of each respective user on the users_checkin dictionary so that every user will have a set of his checkins
        users_checkin = {}
        for ir in users.itertuples():
            users_checkin[ir[1]] = checkins.loc[checkins['UID'] == ir[1]]
        ### Display the checkin distribution of each user
        for key, value in users_checkin.items():
            print('UID:{:4d} #Checkins: {}'.format(key, len(value.index)))