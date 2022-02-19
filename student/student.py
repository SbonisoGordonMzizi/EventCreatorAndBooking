import os,json
from urllib import response
import requests
from authorization import authorization
from data_reading import read_data_from_api, read_token_file, read_from_local_data_file


def check_if_booked(event_id): 
    """
    Description:
        check_if_booked is responsible for checking if
        student has alread booked in the slot

    Parameters:
        Takes one parameter of type String:
            event_id:String 
    return:
        returns boolean type:
            True or False:boolean  
    """

    api_data = None
    user_email = None
    absolute_path=f"{os.getenv('HOME')}/.config/code_clinic/.config.json"

    with open(absolute_path) as file_object:
       data = json.load(file_object)
       user_email = data["user_email"]

    api_data = read_from_local_data_file.read_from_file()

    for item in api_data["items"]:
        if item["id"] == event_id:
            if "attendees" in item.keys():
                attendees = item["attendees"]
                for index in range(len(attendees)):
                    if attendees[index]['email'] == user_email:
                        return True
    return False              
    

def read_event():
    """
    Description:
        read_event is responsible for read 
        student booked slots

    Parameters:
        Takes no argument:
            None:None 

    return:
        returns None type:
            None:None  
    """
    
  
    if read_token_file.get_token() != None and authorization.check_if_token_valid():
        status = read_data_from_api.read_from_api()

        if status == True:
            data_from_api = read_from_local_data_file.read_from_file()

            if data_from_api != None:
                print("_"*20 +"LIST OF BOOKED SLOT(S)"+"_"*20)
                print("\n")
                for index in range(len(data_from_api['items'])):
                    event = data_from_api['items'][index]
                    if check_if_booked(event['id']):
                        
                        print(f"""Summary: {event['summary']}
                        Description: {event['description']}
                        Location   : {event['location']}
                        Orgnizer   : {event['creator']['email']}
                        Start Time : {event['start']['dateTime']}
                        End Time   : {event['end']['dateTime']}\n""")
                        
            else:
                print("Currently, you are not booked for any slot.")
    else:
        print("Access Denied. Please Login")
    

def book_slot(summary_user):
    """
    Description:
        book_slot is responsible for slot booking

    Parameters:
        Takes one parameter of type String:
            summary_user:String 

    return:
        returns None type:
            None:None  
    """

    if read_token_file.get_token() != None and authorization.check_if_token_valid():
        status = read_data_from_api.read_from_api()
        data_from_api = read_from_local_data_file.read_from_file()
        if data_from_api != None:
            for index in range(len(data_from_api['items'])):
                summary_api = data_from_api['items'][index]['summary']
                if summary_api == summary_user:
                    if check_if_booked(data_from_api['items'][index]['id']):
                        print("You have aleady booked for this slot.")
                        return
                    else:
                        event_data = data_from_api['items'][index]
                        user_email = read_from_local_data_file.read_config_file()
                        students = {'email': f"{user_email}", "responseStatus": "needsAction"}
                        if "attendees" in event_data.keys():
                            event_data['attendees'].append(students)
                        else:
                            event_data['attendees'] = [students]
                        response_code = attendees(event_data)
                        if response_code == 200:
                            status = read_data_from_api.read_from_api()
                            print("Slot booked successfully!")
                        return
            
            print(f"Slot with Summary: '{summary_user}' not found")
                   
        else:
            print("No slots available.")
    else:
        print("Access Denied. Please login.")


def attendees(event):
    """
    Description:
        add_attender is responsible for 
        booking a student

    Parameters:
        Takes one parameter of type String:
            event:String 

    return:
        returns int type:
            status_code:int  
    """

    update_event = {
    'summary': event['summary'],
    'location': event['location'],
    'description': event['description'],
    'start': {
        'dateTime': event['start']['dateTime'],
        'timeZone': event['start']['timeZone']
    },
    'end': {
        'dateTime': event['end']['dateTime'],
        'timeZone': event['end']['timeZone']
    },
    'attendees': event["attendees"] 
    }
    
    url = f"https://www.googleapis.com/calendar/v3/calendars/team210114.b@gmail.com/events/{event['id']}"
    user_token = read_token_file.get_token()
    response = requests.put(url,data=json.dumps(update_event) ,headers={ 'Authorization': f'Bearer {user_token}' })
    return response.status_code


def cancel_booking(summary):
    """
    Description:
        cancel_booking is responsible for 
        cancel booking

    Parameters:
        Takes one parameter of type String:
            summary:String 

    return:
        returns None type:
            None:None
    """

    if read_token_file.get_token() != None and authorization.check_if_token_valid():
        user_email = read_from_local_data_file.read_config_file()
        status = read_data_from_api.read_from_api()
        read_api_data = read_from_local_data_file.read_from_file()
        list_of_events = read_api_data['items']
        
        for event in list_of_events:
            if event['summary'] == summary:
                if check_if_booked(event['id']):
                    users = event['attendees']
                    for index in range(len(users)):
                        if users[index]['email'] == user_email:
                            event['attendees'].pop(index)
                    response_code = attendees(event)
                    if response_code == 200:
                        status = read_data_from_api.read_from_api()
                        print("Booking cancelled successfully.")


                else:
                    print("You cannot cancel a slot you did not make a booking for. Booking cancellation rights are only permitted for booking attendees.")
                return 
            
        print("Event not found.")

    else:
        print("Access Denied. Please login.")