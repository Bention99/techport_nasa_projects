from user_input import user_input_information
from api_request import call_api

def main():
    print("Hello from techport-nasa-projects!")
    valid_date = user_input_information()
    print(f"date set to {valid_date}")
    call_api(valid_date)

if __name__ == "__main__":
    main()