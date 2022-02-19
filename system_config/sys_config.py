import os,json

absolute_path=f'{os.getenv("HOME")}/.config/code_clinic/'
file_name = ".config.json"


def auto_create_config_file(data):
    """
    Description:
        auto_create_config_file is responsible for creating a user
        configuration file that stores the users information
        which will be used for login purposes.

    Parameters:
        Takes one parameter of dictionary type:
            data:dict
        
    return:
        returns Integer data type:
            1:Integer
    """
    if os.path.exists(absolute_path) and os.path.isdir(absolute_path):
        with open(f'{absolute_path}/{file_name}',"w") as config:
            json.dump(data,config)
        return 1
    else:
        os.makedirs(absolute_path)
        with open(f'{absolute_path}/{file_name}',"w") as config:
            json.dump(data,config)
        return 1
    

def check_if_config_exist():
    """
    Description:
        check_if_config_exist is responsible for checking if
        a configuration file exists.

    Parameters:
        Takes no parameters:
            None:None
        
    return:
        returns Boolean data type:
            True or False:Boolean
    """
    if os.path.exists(f'{absolute_path}/{file_name}'):
        return True
    else:
        return False





