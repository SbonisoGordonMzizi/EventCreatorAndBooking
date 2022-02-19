import sys
from system_config import sys_config
from authorization import authorization
from user_interface import user_interface
from student import student
from data_reading import read_data_from_api
from data_reading import read_from_api_write_to_file
from data_reading import read_from_local_data_file
from volunteer import volunteer
arg_len = len(sys.argv)


if sys_config.check_if_config_exist() is False:
 
    data = user_interface.user_prompt()
    if data != None:
        status = sys_config.auto_create_config_file(data)
        if status == 1:
            print("<> Configuration done <>")

elif arg_len == 1 or sys.argv[1].lower() in ["-h","--help","help"]:
    user_interface.help()

else:
    if arg_len == 2 and sys.argv[1].lower() == "login":
        user_interface.start_system()
       
    elif arg_len == 2 and sys.argv[1].lower() == "logout":
        user_interface.exit_system()
        
    elif arg_len == 3 and sys.argv[1].lower() == "cancel_booking":
        student.cancel_booking(sys.argv[2])

    elif arg_len == 3 and sys.argv[1].lower() == "book":
        student.book_slot(sys.argv[2])

    elif arg_len == 2 and sys.argv[1].lower() == "read_event":
        student.read_event()

    elif (arg_len == 2 or arg_len == 3) and sys.argv[1].lower() == "check_slot":
        if arg_len == 2:
            user_interface.check_slot()
        else:
            if sys.argv[2].isdigit() == True:
                user_interface.check_slot(int(sys.argv[2]))
            else:
                print("Please enter the number of days you require.")    

    elif arg_len == 2 and sys.argv[1].lower() == "create_slot":
        volunteer.create_slot()

    elif arg_len == 3 and sys.argv[1].lower() == "cancel_slot":
       volunteer.cancel_slot(sys.argv[2])
    
    elif arg_len == 2 and sys.argv[1].lower() in ["-v","--version"]:
        print("\nCodeCliniApp 0.0.1\n")

    else:
        print(f"error: Found argument '{sys.argv[1]}' isn't valid \n")
        user_interface.help()
        

