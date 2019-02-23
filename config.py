import json

datasources = {}
with open('config.json') as config_file:
    configs = json.load(config_file)
    for name in configs['datasources']:
        datasources[name] = configs['datasources'][name]
