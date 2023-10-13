import constants
import json
import os

class UserInfo:
    hydrus_key = None
    api_port = None

    def __init__(self) -> None:
        self.read_user_info()
    
    def set_user_info(self, hydrus_key: str, api_port: int)-> bool:
        self.hydrus_key = hydrus_key
        self.api_port = api_port

        return self.write_user_data()

    def get_user_info(self)->(str,int):
        return self.hydrus_key, self.api_port
    
    def write_user_data(self)->bool:
        if self.hydrus_key == None and self.api_port == None:
            print("Hdyrus key and api port not set/read!")
            return False
        if self.hydrus_key == None:
            print("Hydrus key missing or unreadable")
            return False
        if self.api_port == None:
            print("Api port missing or unreadable")
            return False
        
        print(self.hydrus_key, self.api_port)
        try:
            self.api_port = int(self.api_port)
        except ValueError:
            print(f"The port value couldnt be coverted into a number")
            return False
        try:
            with open(constants.USER_DATA_FILE, "w") as json_file:
                data = {
                    constants.HYDRUS_APIKEY_KEY: self.hydrus_key, 
                    constants.HYDRUS_PORT_KEY : self.api_port
                }
                json.dump(data, json_file)
                return True
        except Exception as e:
            print(f"Failed due to : {e}")
        return False

    def read_user_info(self)->(str,int):
        try:
            with open(constants.USER_DATA_FILE, "r") as json_file:
                file_size = os.path.getsize(constants.USER_DATA_FILE)
                if file_size == 0:
                    print("The file is empty.")
                    return ("TFIE", None)
                data = json.load(json_file)
                self.hydrus_key = data[constants.HYDRUS_APIKEY_KEY]
                self.api_port = data[constants.HYDRUS_PORT_KEY]
            return data
        except FileNotFoundError:
            print(f"File not found: ", constants.USER_DATA_FILE)
            return ("FNF", None)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return ("FTDJ", None)