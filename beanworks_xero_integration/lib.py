
def get_environment_variables(os, config):
    config['CLIENT_ID'] = os.getenv('CLIENT_ID')
    config['CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')
    config['REDIRECT_URI'] = os.getenv('REDIRECT_URI')
    return config
