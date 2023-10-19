"""Models the user of the program to store program specific data in a user_data json
"""
import json
import os

import constants

class UserInfo:
    """Models the user of the program
    Stores the key for hydrus api and the according port number
    """
    hydrus_key = None
    api_port = None

    def __init__(self) -> None:
        """By default will attempt to find a user_data.json to read keys from
        """
        self.read_user_info()
    
    def set_user_info(self, hydrus_key: str, api_port: int)-> bool:
        """Sets the key and api port, can be manually entered or solved somehow

        Args:
            hydrus_key (str): api key from hydrus
            api_port (int): port for the localhost:port

        Returns:
            bool: if suceeded or not
        """
        self.hydrus_key = hydrus_key
        self.api_port = api_port
        return self.write_user_data()

    def get_user_info(self)->(str,int):
        """Returns hydrus key and api port
        Returns:
            _type_: tuple of the hydrus key and api port as (str,int)
        """
        return self.hydrus_key, self.api_port
    
    def write_user_data(self)->bool:
        """Writes the user data to the user_data.json file
        Returns:
            bool: sucessful or not
        """
        
        if self.hydrus_key is None and self.api_port is None:
            print("Hdyrus key and api port not set/read!")
            return False
        if self.hydrus_key is None:
            print("Hydrus key missing or unreadable")
            return False
        if self.api_port is None:
            print("Api port missing or unreadable")
            return False
        try:
            self.api_port = int(self.api_port)
        except ValueError:
            print("The port value couldnt be coverted into a number")
            return False
            
        with open(constants.USER_DATA_FILE, "w", encoding="utf-8") as json_file:
            data = {
                constants.HYDRUS_APIKEY_KEY: self.hydrus_key, 
                constants.HYDRUS_PORT_KEY : self.api_port
            }
            json.dump(data, json_file)
            return True

    def read_user_info(self)->(str,int):
        """Method to read the JSON file for user data
        Returns:
        _type_: if sucessful will return a tuple of (str,int) that contains (hydrus api key, port number). 
        Otherwise wil return (reason for error: str, None)
        """
        try:
            with open(constants.USER_DATA_FILE, "r", encoding="utf-8") as json_file:
                file_size = os.path.getsize(constants.USER_DATA_FILE)
                if file_size == 0:
                    print("The file is empty.")
                    return ("TFIE", None)
                data = json.load(json_file)
                self.hydrus_key = str(data[constants.HYDRUS_APIKEY_KEY])
                self.api_port = data[constants.HYDRUS_PORT_KEY]
            return data
        except FileNotFoundError:
            print("File not found: ", constants.USER_DATA_FILE)
            return ("FNF", None)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return ("FTDJ", None)
