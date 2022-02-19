from authorization import authorization
from data_reading import read_data_from_api,read_token_file,read_from_local_data_file
from prettytable import PrettyTable
import datetime

table = PrettyTable()


def user_prompt():
    """
    Description:
        user_prompt is responsible for asking a user if they are
        a student or a volunteer.

    Parameter:
        Takes no Parameters:
            None:None

    return:
        returns None or dictionary type:
            None:None
            dict:dict
    """
    
    user_type = input("Are you a student? Y/N: ").upper()
    email = input("Please enter your email address: ")
    if user_type.lower() == "y":
        return {"user_type": "student", "user_email": email}
    elif user_type.lower() =="n":
        return {"user_type": "volunteer", "user_email": email}
    else:
        return None


def get_date():
    """
    Description:
        get_date is responsible for getting user input and verify if it is
        a valid date.

    Parameters:
        Takes no Parameters:
            None:None

    return:
        returns None or date of type String:
            None:None
            date:String
    """
    
    date = input("Enter date (yyyy-mm-dd): ")
    date_list = date.split("-",2)
    if len(date_list) == 3:
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
 
        if (year.isdigit() and len(year) == 4) and (month.isdigit() and len(month) == 2) and (day.isdigit() and len(day) == 2):
            return f"{year}-{month}-{day}"
        else:
            print("Wrong date")
            return None
    else:
        print("Wrong date")
        return None
   

def get_time():
    """
    Description:
        get_time is responsible for getting user input and verify if it is
        a valid time.

    Parameters:
        Takes no Parameters:
            None:None

    return:
        returns None or time of type String:
            None:None
            time:String
    """

    time = input("Enter start time between 09:00-16:00 (hh:mm): ")
    time_list = time.split(":")
    if len(time_list) == 2:
        hours = time_list[0]
        minutes = time_list[1]
        if (hours.isdigit() and int(hours) in range(9,16+1)) and (minutes.isdigit() and int(minutes) in range(60)):
            return f"{hours}:{minutes}"
        else:
            print("Wrong time")
            return None
    else:
        print("Wrong time")
        return None


def get_datetime():
    """
    Description:
        get_datetime is responsible for verifying if a date is a current
        or future date.

    Parameters:
        Takes no Parameters:
            None:None

    return:
        returns None or start_time and end_time of type datetime:
            None:None
            start_time:datetime
            end_time:datetime
    """
    
    date = get_date()
    if date != None:
        time = get_time()
        if time != None:
            year = date.split("-")[0]
            month = date.split("-")[1]
            day = date.split("-")[2]
            hours = time.split(":")[0]
            minutes = time.split(":")[1]

            current_date = str(datetime.datetime.now()).split()[0]

            if date >= current_date:
                start_time = datetime.datetime(int(year),int(month),int(day),int(hours),int(minutes),00).isoformat()
                end_time = (datetime.datetime(int(year),int(month),int(day),int(hours),int(minutes),00) + datetime.timedelta(minutes=30)).isoformat()
                return start_time,end_time
            else:
                print("Provide new date")
                return None
        else:
            print("Provide correct time")
            return None
    else:
        print("Provide correct date")
        return None

        
def start_system():
    """
    Description:
        start_system is responsible for the authorization of the client.

    Parameters:
        Takes no parameters:
            None:None

    return:
        returns None type:
            None:None
    """
    if authorization.client_authorization():
        print("Login succesful.\nWelcome To WethinkCode Code Clinic Booking System\n")


def exit_system():
    """
    Description:
        exit_system is responsible for revoking and deleting an access token.

    Parameters:
        Takes no parameters:
            None:None

    return:
        returns None type:
            None:None
    """
    if authorization.revoke_tokens() == True and authorization.delete_token() == True:
        print("You have logged out of the WeThinkCode Code Clinic Booking System.")


def help():
    """
    Description:
        help is used to print the allowable commands when the user enters "help".

    Parameters:
        Takes no parameters:
            None:None

    return:
        returns None type:
            None:None
    """

    print("""Code Clinic Booking System 0.0.1

USAGE:
    code-clinic [FLAGS] [SUBCOMMAND]

FLAGS:
    -h, --help       Prints help information
    -V, --version    Prints version information

SUBCOMMANDS:
    login                                           Logs user into the code clinic booking system
    logout                                          Logs user out the code clinic booking system
    create_slot                                     Allows a volunteer to create a slot
    book [slot name]                                Allows a student to book a slot
    read_event                                      Allows the user to view slots they are confirmed for
    check_slot [number of days being viewed]        Checks the availability of slots
    cancel_slot [slot name]                         Allows a volunteer to cancel slot
    cancel_booking [slot name]                      Cancels booking made by student
""")


def check_slot(days=7):
    """
    Description:
        check_slot is responsible for checking available slots for the next 7 days.

    Parameters:
        Takes one parameter of type String:
            days:String

    return:
        returns None type:
            None:None
    """

    status = read_data_from_api.read_from_api(days)
    if status == True:
        read_api_data = read_from_local_data_file.read_from_file()
        print("-"*25, "LIST OF AVAILABLE SLOTS", "-"*25)
        print("\n")
        for index in range(len(read_api_data["items"])):
            event = read_api_data["items"][index]
            print(f"""Summary: {event['summary']}
            
            description:    {event['description']}
            volunteer:      {event['creator']['email']}
            location:       {event['location']}
            start:          {event['start']['dateTime']}
            end:            {event['end']['dateTime']}""")
            print("-"*75)

