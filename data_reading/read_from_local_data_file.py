from data_reading import read_from_api_write_to_file
import os,json

def read_from_file():
    """
    Description:
        read_from_file is responsible for opening a json file
        and reading the data from the json file.

    Parameters:
        Takes No Parameters:
            None:None 

    return:
        returns data of dictionary type:
            data:dict
    """
    
    absolute_path=f'{os.getenv("HOME")}/.config/code_clinic/'
    file_name = "schedule.json"
    
    if os.path.exists(absolute_path) and os.path.isdir(absolute_path):
        with open(f'{absolute_path}/{file_name}',"r") as schedule:
            data = json.load(schedule)
        return data
    else:
        return None


def read_config_file():
    """
    Description:
        read_config_file is responsible for reading
        data from the api saved in the config file

    Parameters:
        Takes No Parameters:
            None:None 
    return:
        returns user_email of String type:
            user_email:String
    """
    user_email = None
    absolute_path=f"{os.getenv('HOME')}/.config/code_clinic/.config.json"

    with open(absolute_path) as file_object:
       data = json.load(file_object)
       user_email = data["user_email"]

    return user_email


def read_user_config_file():
    """
    Description:
        read_user_config_file is responsible for reading
        user .config.json file 

    Parameters:
        Takes no paramenters:
            None:None
             
    return:
        returns usertype of String type:
            usertype:String
    """
    home_path = os.getenv("HOME")
    config_path = f'{home_path}/.config/code_clinic'

    data = ""
    with open(f"{config_path}/.config.json","r") as file_config:
        data = json.load(file_config)

    return data["user_type"]