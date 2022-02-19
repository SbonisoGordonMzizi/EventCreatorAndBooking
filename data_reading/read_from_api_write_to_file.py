import os,json

def read_api_write_to_file(data):
    """
    Description:
        read_api_write_to_file is responsible for reading
        data from the api and storing it in a json file.

    Parameters:
        Takes one parameter of type dictionary:
            data:dict

    return:
        returns Integer typer:
            1:Integer
    """

    absolute_path=f'{os.getenv("HOME")}/.config/code_clinic/'
    file_name = "schedule.json"
    
    if os.path.exists(absolute_path) and os.path.isdir(absolute_path):
        with open(f'{absolute_path}/{file_name}',"w") as schedule:
            json.dump(data,schedule)
        return 1 
    else:
        os.makedirs(absolute_path)
        with open(f'{absolute_path}/{file_name}',"w") as schedule:
            json.dump(data,schedule)
        return 1