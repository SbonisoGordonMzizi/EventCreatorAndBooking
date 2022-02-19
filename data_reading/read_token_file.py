import os,json

absolute_path = f'{os.getenv("HOME")}/.config/code_clinic/.token.json'

def get_token():
    """
    Description:
        get_token is responsible for reading
        token from token.json file

    Parameters:
        Takes No Parameters:
            None:None 
    return:
        returns token of String type or None:
            token:String
            None:None  
    """

    if os.path.exists(absolute_path):
        with open(absolute_path,"r") as file_object:
            json_file = json.load(file_object)
        return json_file["token"]
    else:
        return None


