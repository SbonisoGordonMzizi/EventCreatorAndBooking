import os,json, requests
from urllib import response
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from data_reading import read_token_file

home_path = os.getenv("HOME")
config_path = f'{home_path}/.config/code_clinic'


def read_user_config_file():
    """
    Description:
        read_user_config_file is responsible for reading
        user .config.json file 

    Parameters:
        Takes no paramenters:
            None:None
             
    return:
        returns usertype of type String:
            usertype:String
    """

    data = ""
    with open(f"{config_path}/.config.json","r") as file_config:
        data = json.load(file_config)

    return data["user_type"]


def auto_create_sys_config_file():
    """
    Description:
        auto_create_sys_config_file is responsible for creating
        sys_config.json file.

    Parameters:
        Takes no paramenters:
            None:None
             
    return:
        returns None type:
            None:None
    """

    config_data = {"installed":
        {"client_id":"",
        "project_id":"",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"",
        "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}


    if os.path.exists(config_path) and os.path.isdir(config_path):
        with open(f'{config_path}/.sys_config.json',"w") as config:
            json.dump(config_data,config)
    else:
        os.makedirs(config_path)
        with open(f'{config_path}/.sys_config.json',"w") as config:
            json.dump(config_data,config)


def select_scope(user_type=None):
    """
    Description:
        select_scope is responsible for selecting the
        scope the user must get.
        student   <> read scope only
        volunteer <> read and write scope

    Parameters:
        Takes one argument of type string:
            user_type:string 

    return:
        returns list data type:
            SCOPES:list
    """
    
    if user_type == "student":
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    else:
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    return SCOPES


def client_authorization():
    """
    Description:
        client_authorization is responsible for generating and encoding
        urls for code authorization endpoint and token endpoint and authorize 
        client app and store access_token and refresh_token to token.json file. 

    Parameters:
        Takes No Parameters:
            None:None 

    return:
        returns Boolean type:
            True:Boolean         
    """

    creds = None
    auto_create_sys_config_file()
    SCOPES = select_scope(read_user_config_file())
   
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{config_path}/.sys_config.json', SCOPES)
            creds = flow.run_local_server(port=0,
            authorization_prompt_message="\nCheck your browser for login page.\n",
            success_message="Login successful. Close webpage and continue on terminal.")
        
        with open(f'{config_path}/.token.json', 'w') as token:
            token.write(creds.to_json())

    return True


def revoke_tokens():
    """
    Description:
        revoke_token is responsible for the removal of the user's 
        permissions to the calendar associated with the token.

    Parameters:
        Takes No Parameters:
            None:None 

    return:
        returns Boolean type:
            True or False: Boolean
    """

    revoke_url = "https://accounts.google.com/o/oauth2/revoke"
    if os.path.exists(f'{config_path}/.token.json'):
        with open(f'{config_path}/.token.json') as access_token:
            token_items = json.load(access_token)

        for key, value in token_items.items():
            if key == 'token':
                token_to_revoke = {key: value}

        requests.post(revoke_url, data=token_to_revoke)

        return True
    return False


def delete_token():
    """
    Description:
        delete_token is responsible for the removal of the user's 
        access token.

    Parameters:
        Takes No Parameters:
            None:None 

    return:
        returns Boolean type:
            True:Boolean
    """
    if os.path.exists(f'{config_path}/.token.json'):
        if os.path.exists(f'{config_path}/.token.json'):
            os.remove(f'{config_path}/.token.json')
            return True


def check_if_token_valid():
    """
    Description:
        check_if_token_valid is responsibile for verifying the
        valididty of a token.

    Parameters:
        Takes No Parameters:
            None:None 
    
    return:
        returns Boolean type:
            True or False:Boolean
    """
    access_token = read_token_file.get_token()
    url ="https://www.googleapis.com/oauth2/v1/tokeninfo"
    data={"access_token":f"{access_token}"}
    response = requests.post(url,data=data)    
    data = response.json().keys()
    if "expires_in" in data:
        return True
    elif "error" in data:
        return False
