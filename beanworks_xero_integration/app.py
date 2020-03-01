# Third-party libraries
from flask import Flask, redirect, request, url_for, render_template, jsonify, abort
from oauthlib.oauth2 import WebApplicationClient
import requests
import json

from beanworks_xero_integration.config import config
import os
from beanworks_xero_integration.lib import get_environment_variables
import logging
import beanworks_xero_integration.constants as constants

# --------------------------   SETUP  -------------------------------
config = get_environment_variables(os, config)
for cf in config.values():
    if cf is None:
        print("Required environment variables are not set. Exiting...")
        exit(0)


logging.basicConfig(filename=config['PATH_TO_LOG_FILE'], level=logging.INFO, format=config['LOG_FORMAT'])
LOGGER = logging.getLogger()

LOGGER.info("All the environment variable required are set")

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# OAuth 2 client setup
CLIENT = WebApplicationClient(config['CLIENT_ID'])



# --------------------------   ROUTES  -------------------------------
@app.route("/")
def home():
    LOGGER.info("Home page accessed")
    return render_template('connect.html')


@app.route("/login")
def login():
    LOGGER.info("Client requested to connect to Xero. Fetching Xero request URL from Xero")
    request_uri = CLIENT.prepare_request_uri(
        config['LOGIN_URL'],
        redirect_uri=config['REDIRECT_URI'],
        scope=config['SCOPE'],
    )
    LOGGER.info("Request URL successfully received. Redirecting to url: {0}".format(request_uri))
    return redirect(request_uri)


@app.route("/login/home")
def setup_client():
    LOGGER.info("Xero credentials accepted. Successfully redirected back. Getting the token and setting up the oauth client")
    code = request.args.get(constants.CODE)
    token_url, headers, body = CLIENT.prepare_token_request(
        config['TOKEN_END_POINT'],
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(config['CLIENT_ID'], config['CLIENT_SECRET']),
    )
    LOGGER.info("Token received. Client is ready to fetch xero data")
    if token_response.status_code != 200:
        status_code = token_response.status_code
        xero_error = json.loads(token_response.text)[constants.ERROR]
        error = 'Error fetching token from xero. Error Status code: {}. Error from Xero {}'.format(status_code, xero_error)
        LOGGER.error(error)
        return render_template('error.html', error=error)
    # Parse the tokens!
    LOGGER.info("Token successfully received from Xero. Application is ready to fetch data from Xero")
    CLIENT.parse_request_body_response(json.dumps(token_response.json()))
    return render_template('application_home.html')


# --------------------------   API  -------------------------------

@app.route("/vendors", methods=["GET"])
def get_vendors():
    LOGGER.info("Client requested to fetch vendor data")
    endpoint = "{0}{1}".format(config['API_BASE_URL'], config['CONTACTS_API_PATH'])
    contacts_info = get_data_xero(endpoint)
    if contacts_info is None:
        LOGGER.error('Error. Cannot get vendors data')
        return abort(500)
    # Vendor is any contact who is a supplier too
    vendor_names = [contact[constants.NAME] for contact in contacts_info[constants.CONTACTS] if contact[constants.IS_SUPPLIER]]
    return jsonify(vendor_names)


@app.route("/accounts", methods=["GET"])
def get_accounts():
    LOGGER.info("Client requested to fetch accounts data")
    endpoint = "{0}{1}".format(config['API_BASE_URL'], config['ACCOUNTS_API_PATH'])
    accounts_info = get_data_xero(endpoint)
    if accounts_info is None:
        LOGGER.error('Error. Cannot get accounts data')
        return abort(500)
    account_names = [account[constants.NAME] for account in accounts_info[constants.ACCOUNTS]]
    return jsonify(account_names)


# --------------------------   Helper Functions  -------------------------------
def get_data_xero (endpoint):
    uri, headers, body = CLIENT.add_token(endpoint)
    # Assumption: We need the data for the latest tenant only
    latest_tenant_id = requests.get(config['CONNECTION_END_POINT'], headers=headers, data=body).json()[0][constants.TENANT_ID]
    headers[constants.TENANT_ID_HEADER] = latest_tenant_id
    headers[constants.ACCEPT] = constants.JSON_HEADER
    response = requests.get(uri, headers=headers, data=body).json()
    if response['Status'] != 'OK':
        LOGGER.error('Error fetching data from URL: {}'.format(endpoint))
        return None
    LOGGER.info("Data successfully received")
    return response


# --------------- RUN FLASK ----------------------
if __name__ == "__main__":
    app.run(ssl_context="adhoc", port = config['FLASK_PORT'])

