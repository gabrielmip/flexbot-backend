import json

def get_config():
    with open('config.json') as config_file:
        return json.load(config_file)

config = get_config()

# proxies
datasources = config['datasources']
telegram_url = config['telegram_url'].format(config['api_key'])
webhook_url = config['webhook_url'].format(config['api_key'])
