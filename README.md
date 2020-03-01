# Beanworks Xero Integration
This application integrates with XERO back-end and fetches the Bank accounts names and Vendor names.

## Background
This application is a web-application that is built using Flask framework.

## Assumption

This application assumes that we need to get data for ONLY the latest created tenant on XERO

## Live Deployment 
To quickly use application, you can navigate to the following link and follow the instructions.
[Link to deployment](https://calm-retreat-69658.herokuapp.com/)
## Deployment
This section demonstrate how to deploy it locally.
## Requirements:
Following tools are required:
* Python 3.8
* pip3

## Installation

It is recommended to use a python virtual environment to run the application


```bash
python3 -m venv ./venv
source venv/bin/activate
```

Clone this repository and run 
`pip3 install beanworks_xero_itegration`
to install the required dependencies

### Setting up the environment variables
You need to setup the following environment variables before you run the application. 
```
CLIENT_ID = <Your_application_client_id>
CLIENT_SECRET = <Your_application_client_secret>
REDIRECT_URI = <Redirect_Uri>  # This MUST match the one you provided in the application. MUST use https
```
Also note that the `REDIRECT_URI` format should be `<your_application_URI>/login/home/` for the application to redirect you
to appropriate location and MUST use https. For example `https`

These values you can get when you setup an application on XERO. For the testing purposes, you can use the following credentials
for the application i have already setup.
```
CLIENT_ID=C3646E7F03C2461AA81174969BAF3ED7
CLIENT_SECRET=Iba2xlbnOWl6MN8zSiJKMSR1HBTYBr390PPu4XNMRn4cJSyI
REDIRECT_URI=https://localhost:5000/login/home
```


## Running the application
Navigate to directory 
```cd beanworks_xero_integration/beanworks_xero_integration```
and Run the file ```python3 app.py```.
(This will start the server). Navigate to the `localhost:5000` and you can view the main page.
All the logs will be stored in `logs/beanworks.log` 

## Application Sequence diagram
The following image will give you an idea of how the application requests flow.

![Application_Sequence_Diagram](/artifacts/Xero_Integration_Sequence.jpg)

## Screenshots
Following are application screenshots

![Page1](/artifacts/SS1.JPG)
![Page2](/artifacts/SS2.JPG)
![Page3](/artifacts/SS3.JPG)

