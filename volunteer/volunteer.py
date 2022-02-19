import os,json
from urllib import response
import requests
from authorization import authorization
from data_reading import read_data_from_api, read_token_file, read_from_local_data_file
from user_interface import user_interface

def check_slot_exist(start_time,end_time):
    """
    Description:
        check_slot_exists is responsible for checking that a slot exists
        before a volunteer can create it.

    Parameters:
        Takes two parameters of type datetime:
            start_time:datetime
            end_time:datetime

    return:
        returns Boolean type:
            True or False:Boolean
    """

    slot_data = read_from_local_data_file.read_from_file()
    slots = slot_data['items']
    for slot in slots:
        end_time_slot = slot["end"]["dateTime"]
        start_time_slot = slot["start"]["dateTime"]
        if start_time >= start_time_slot.split("+",1)[0] and start_time <= end_time_slot.split("+",1)[0]:
            if end_time >= start_time_slot.split("+",1)[0] and end_time <= end_time_slot.split("+",1)[0]:
                return True
    return False
       
        
def create_slot():
  
    """
    Description:
        create_slot is responsible for allowing volunteers to create a code clinic event.

    Parameters:
        Takes no paramenters:
            None:None

    return:
        returns None type:
            None:None
    """

    if read_from_local_data_file.read_user_config_file() == "volunteer":
        if read_token_file.get_token() != None and authorization.check_if_token_valid():
            summary = input("Enter slot summary: ")
            location = input("Enter location: ")
            description = input("Enter slot description: ")
            dates = user_interface.get_datetime()
            if dates != None:
            
                startDate = dates[0]
                endDate = dates[1]
                if not check_slot_exist(startDate,endDate):
                    event = {
                    'summary': f'{summary}',
                    'location': f'{location}',
                    'description': f'{description}',
                    'start': {
                        'dateTime': f'{startDate}',
                        'timeZone': 'Africa/Johannesburg'
                    },
                    'end': {
                        'dateTime': f'{endDate}',
                        'timeZone': 'Africa/Johannesburg'
                    }
                    }

                    url = f"https://www.googleapis.com/calendar/v3/calendars/team210114.b@gmail.com/events"
                    user_token = read_token_file.get_token()
                    response = requests.post(url,data=json.dumps(event) ,headers={ 'Authorization': f'Bearer {user_token}' })
                    if response.status_code == 200:
                        read_data_from_api.read_from_api()
                        print("Slot created successfully")
                else:
                    print(f"\nfrom {startDate}  to {endDate} is blocked")
        else:
            print("Access Denied. Please Login")
    else:
        print("You are not a volunteer. Slot creation rights are only permitted for volunteers.")
   

def check_slot_ownership(event_id):
    """
    Description:
        check_slot_ownership is responsible for checking which volunteer
        the slot belongs to.

    Parameters:
        Takes one parameter of type String:
            event_id:String

    return:
        returns Boolean type:
            True or False:Boolean
    """

    absolute_path=f"{os.getenv('HOME')}/.config/code_clinic/.config.json"
    status = read_data_from_api.read_from_api()
    api_data = read_from_local_data_file.read_from_file()
    with open(absolute_path) as file_object:
       data = json.load(file_object)
       user_email = data["user_email"]

    for item in api_data["items"]:
        if item["id"] == event_id:
            if item["creator"]["email"] == user_email:
                return True
    return False
    

def cancel_slot(summary):
    """
    Description:
        cancel_slot is responsible for canceling a code clinics slot.

    Parameters:
        Takes one parameter of type String:
            summary:String

    return:
        returns None type:
            None:None
    """

    if read_from_local_data_file.read_user_config_file() == "volunteer":
        if read_token_file.get_token() != None and authorization.check_if_token_valid():
            read_data_from_api.read_from_api()
            read_api_data = read_from_local_data_file.read_from_file()
            list_of_events = read_api_data['items']
            user_token = read_token_file.get_token()

            for event in list_of_events:
                if event['summary'] == summary:
                    if check_slot_ownership(event['id']):
                        requests.delete(f"https://www.googleapis.com/calendar/v3/calendars/team210114.b@gmail.com/events/{event['id']}", headers={ 'Authorization': f'Bearer {user_token}' })
                        print("SLOT deleted")
                    else:
                        print('You cannot cancel a slot you did not create. Slot cancellation rights are only permitted for slot creators.')
            print("Slot not found")
        else:
            print("Access Denied. Please Login")
    else:
        print("You are not a volunteer. Slot cancellation rights are only permitted for volunteers.")