#!/usr/bin/env python
"""
Developed by Gunarto Sindoro Njoo
v.0.1 [5 Oct 2017 ]
"""
import json

### Configuration
def read_config(filename='config.json'):
    try:
        with open(filename) as data_file:
            config = json.load(data_file)
            return config
    except Exception as ex:
        print('Exception in init config file : %s' % ex)
        return None