from user_input import user_input_information
from api_request import call_api
from db import init_db

def main():
    init_db()
    print("Hello from techport-nasa-projects!")
    valid_date = user_input_information()
    print(f"Date set to {valid_date}")
    
    print(f"Calling API {valid_date}")
    call_api(valid_date)

if __name__ == "__main__":
    main()