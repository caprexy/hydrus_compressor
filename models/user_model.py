"""Models the user of the program to store program specific data in a user_data json
"""
import json
import os

import controller.constants as constants

class UserInfo:
    """Models the user of the program
    Stores the key for hydrus api and the according port number
    Stores other program settings
    """
    # api settings
    api_opts = {
        "hydrus_key" : None,
        "api_port" : None,
    }

    # program settings
    
    # compressed image quality
    compression_opts = {
        "compressed_img_quality" : 95,
    }
    
    # resize
    resize_opts = {
        "should_resize" : False,
        "should_resize_by_percentage" : False,
        "resize_by_percentage" : 75,
        "resize_by_pixel_height" : 3840,
        "resize_by_pixel_width" : 2180,
    }

    
    # creates a python singleton
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserInfo, cls).__new__(cls)
            cls._read_user_json(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """By default will attempt to find a user_data.json to read keys from
        """
        self._read_user_json()
    
    
    def set_user_info(self, hydrus_key: str, api_port: int)-> bool:
        """Sets the key and api port, can be manually entered or solved somehow

        Args:
            hydrus_key (str): api key from hydrus
            api_port (int): port for the localhost:port

        Returns:
            bool: if write suceeded or not
        """
        if hydrus_key is None and api_port is None:
            raise ValueError("Hdyrus key and api port not set/read!")
        if hydrus_key is None:
            raise ValueError("Hydrus key missing or unreadable")
        if api_port is None:
            raise ValueError("Api port missing or unreadable")
        try:
            api_port = int(api_port)
        except ValueError:
            raise ValueError("The port value couldnt be coverted into a number")
        
        self.api_opts["hydrus_key"] = str(hydrus_key)
        self.api_opts["api_port"] = api_port
        return self.write_user_data()

    def get_api_info(self)->(str,int):
        """Returns hydrus key and api port
        Returns:
            _type_: tuple of the hydrus key and api port as (str,int)
        """ 
        return str(self.api_opts["hydrus_key"]), self.api_opts["api_port"]
    
    def write_user_data(self):
        """Writes the user data/all known and saved data to the user_data.json file
        Returns:
            bool: sucessful or not
        """
        try:
            with open(constants.USER_DATA_FILE, "w", encoding="utf-8") as json_file:
                data = {
                    "api_opts" : self.api_opts,
                    "compression_opts" : self.compression_opts, 
                    "resize_opts" : self.resize_opts,
                }
                json.dump(data, json_file)
        except FileNotFoundError as e:
            raise e

    def _read_user_json(self)->(str,int):
        """Method to read the JSON file for user data and set the according values found from there
        Returns:
        _type_: if sucessful will return a tuple of (str,int) that contains (hydrus api key, port number). 
        Otherwise wil return (reason for error: str, None)
        """
        try:
            with open(constants.USER_DATA_FILE, "r", encoding="utf-8") as json_file:
                file_size = os.path.getsize(constants.USER_DATA_FILE)
                if file_size == 0:
                    raise FileNotFoundError
                data = json.load(json_file)
        except FileNotFoundError:
            print("Making new user data file!")
            json_file = open(constants.USER_DATA_FILE, "w", encoding="utf-8").close()
            return
        except json.JSONDecodeError as ex:
            print("Found a corrupted datafile, making a new one")
            os.remove(constants.USER_DATA_FILE)
            open(constants.USER_DATA_FILE, "w", encoding="utf-8").close()
            raise ex
        
        # parse the data/json
        try:
            self.api_opts = data["api_opts"]
            self.compression_opts = data["compression_opts"]
            self.resize_opts = data["resize_opts"]
        except KeyError:
            print("Failed to read, so just overwriting with plain user data")
            self.write_user_data()
            

    ## setters and getters    
    # Setter methods for api_opts
    def set_api_key(self, key):
        self.api_opts["hydrus_key"] = key
        self.write_user_data()

    def set_api_port(self, port):
        self.api_opts["api_port"] = port
        self.write_user_data()

    # Getter methods for api_opts
    def get_api_key(self):
        return self.api_opts["hydrus_key"]

    def get_api_port(self):
        return self.api_opts["api_port"]

    # Setter methods for compression_opts
    def set_compressed_img_quality(self, quality):
        self.compression_opts["compressed_img_quality"] = quality
        self.write_user_data()

    # Getter methods for compression_opts
    def get_compressed_img_quality(self):
        return self.compression_opts["compressed_img_quality"]

    # Setter methods for resize_opts
    def set_should_resize(self, should_resize):
        self.resize_opts["should_resize"] = should_resize
        self.write_user_data()

    def set_should_resize_by_percentage(self, should_resize_by_percentage):
        self.resize_opts["should_resize_by_percentage"] = should_resize_by_percentage
        self.write_user_data()

    def set_resize_percentage(self, percentage):
        self.resize_opts["resize_by_percentage"] = percentage
        self.write_user_data()

    def set_resize_pixel_height(self, pixel_height):
        self.resize_opts["resize_by_pixel_height"] = pixel_height
        self.write_user_data()

    def set_resize_pixel_width(self, pixel_width):
        self.resize_opts["resize_by_pixel_width"] = pixel_width
        self.write_user_data()

    # Getter methods for resize_opts
    def get_should_resize(self):
        return self.resize_opts["should_resize"]

    def get_should_resize_by_percentage(self):
        return self.resize_opts["should_resize_by_percentage"]

    def get_resize_percentage(self):
        return self.resize_opts["resize_by_percentage"]

    def get_resize_pixel_height(self):
        return self.resize_opts["resize_by_pixel_height"]

    def get_resize_pixel_width(self):
        return self.resize_opts["resize_by_pixel_width"]