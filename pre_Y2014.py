#!/usr/bin/env python
"""
Developed by Gunarto Sindoro Njoo
v.0.1 [5 Oct 2017 ]
"""
### General libraries
import pandas as pd
import numpy as np
import csv
import os
### Custom libraries
import functions as fu

### Main function ###
if __name__ == '__main__':
    config = fu.read_config()
    dataset = config['dataset']
    active_dataset = config['active_dataset']
    general_folder = config['dataset_folder']
    output_folder = config['dataset_processed_folder']
    for d in active_dataset:
        print(d)
        dataset_folder = '/'.join((general_folder, config[d]['folder']))
        checkin_file = config[d].get('checkin')
        user_file = config[d].get('user')
        venue_file = config[d].get('venue')
        category_file = config[d].get('category')
        delimiter = config[d].get('delimiter')
        header = config[d].get('header')

        dateparse = lambda x: pd.datetime.strptime(x, '%a %b %d %H:%M:%S %z %Y')
        df = pd.read_csv('/'.join((dataset_folder, checkin_file)), header=header, delimiter=delimiter, encoding='latin-1', parse_dates=[7], converters={7: lambda x: dateparse(x).timestamp()})
        print(df.head())
        print(df.shape)
        print(df.dtypes)

        df[8] = df.apply(lambda row: int(float(row[7]) + row[6]*60), axis=1)
        df.drop(df.columns[[6, 7]], axis=1, inplace=True)

        print(df.head())
        print(df.shape)
        print(df.dtypes)

        users = df[0].unique().tolist()
        venues = dict(zip(df[1],df[2]))
        categories = dict(zip(df[2],df[3]))

        # print(len(df[0].unique()))
        # print(len(df[1].unique()))
        # print(len(df[2].unique()))
        # print(len(users))
        # print(len(venues))

        # print(df[2].value_counts())

        output_name = '/'.join((output_folder, user_file))
        if not os.path.isfile(output_name):
            if not os.path.exists(os.path.dirname(output_name)):
                try:
                    os.makedirs(os.path.dirname(output_name))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(output_name, 'w') as f:
                for x in users:
                    f.write(''.join((str(x), '\n')))

        output_name = '/'.join((output_folder, venue_file))
        if not os.path.isfile(output_name):
            with open(output_name, 'w') as f:
                w = csv.writer(f)
                w.writerows(venues.items())

        output_name = '/'.join((output_folder, category_file))
        if not os.path.isfile(output_name):
            with open(output_name, 'w') as f:
                w = csv.writer(f)
                w.writerows(categories.items())

        output_name = '/'.join((output_folder, checkin_file))
        if not os.path.isfile(output_name):
            df.to_csv(output_name, header=False, sep=',')