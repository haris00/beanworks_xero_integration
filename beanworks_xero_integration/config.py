config = {
    'API_BASE_URL': "https://api.xero.com/api.xro/2.0/",
    'LOGIN_URL': "https://login.xero.com/identity/connect/authorize",
    'TOKEN_END_POINT': "https://identity.xero.com/connect/token",
    'CONNECTION_END_POINT': "https://api.xero.com/connections",
    'SCOPE': ['accounting.contacts.read', 'accounting.settings.read'],
    'CONTACTS_API_PATH': 'Contacts',
    'ACCOUNTS_API_PATH': 'Accounts',
    'PATH_TO_LOG_FILE': 'logs/beanworks.log',
    'LOG_FORMAT': '%(asctime)s - %(message)s',
    'CLIENT_ID': "", # To be set from Env Variable
    'CLIENT_SECRET': "", # To be set from Env Variable
    'FLASK_PORT': 5000
}