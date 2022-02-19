from data_reading import read_token_file, read_from_api_write_to_file
import requests
import datetime


def read_from_api(days=7):
    """
    Description:
        read_from_api is responsible for checking if a token is valid
        then reads all slots from a calender

    Parameters:
        Takes one parameter of type Integer:
            days:Integer

    return:
        returns Boolean or None type:
            True or False:Boolean
            None:None
    """

    current_time = datetime.datetime.utcnow()
    lower_bound = current_time.isoformat()+"Z"
    upper_bound = (current_time + datetime.timedelta(days=days)).isoformat()+"Z"

    url = f"https://www.googleapis.com/calendar/v3/calendars/team210114.b@gmail.com/events?timeMin={lower_bound}&timeMax={upper_bound}"
    user_token = read_token_file.get_token()
    response = requests.get(url, headers={ 'Authorization': f'Bearer {user_token}' })
    if response.status_code == 200:
        read_from_api_write_to_file.read_api_write_to_file(response.json())
        return True
    elif response.status_code == 401:
        print("Access Denied. Please login")
        return False
    else:
        print("Currently there are no slots available. Please check again later.")
        return None
       

