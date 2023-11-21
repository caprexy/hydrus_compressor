"""Models the user of the program to store program specific data in a user_data json
"""
import json
import os
import atexit

import controller.constants as constants

"""Models the user of the program
Stores the key for hydrus api and the according port number
Stores other program settings
"""


# name/path of the user datafile
USER_DATA_FILE = "user_data.json" # if changed, add to gitignore

# api settings
hydrus_key = None
api_port = None

# program settings

# compressed image quality options

compressed_img_quality = 95


# resize options
should_resize = False
should_resize_by_percentage = False
resize_by_percentage = 75
resize_by_pixel_height = 3840
resize_by_pixel_width = 2180


def set_api_info(hydrus_key_in: str, api_port_in: int):
    """Sets the key and api port, can be manually entered or solved somehow

    Args:
        hydrus_key (str): api key from hydrus
        api_port (int): port for the localhost:port

    Returns:
        bool: if write suceeded or not
    """
    if hydrus_key_in is None and api_port_in is None:
        raise ValueError("Hdyrus key and api port not set/read!")
    if hydrus_key_in is None:
        raise ValueError("Hydrus key missing or unreadable")
    if api_port_in is None:
        raise ValueError("Api port missing or unreadable")
    try:
        api_port_in = int(api_port_in)
    except ValueError:
        raise ValueError("The port value couldnt be coverted into a number")
    
    global hydrus_key, api_port
    hydrus_key = hydrus_key_in
    api_port = api_port_in
    return write_user_data()

def get_api_info()->(str,int):
    """Returns hydrus key and api port
    Returns:
        _type_: tuple of the hydrus key and api port as (str,int)
    """ 
    if api_port == None and hydrus_key == None:
        raise ValueError("Missing both api port and hydrus key in settings")
    if hydrus_key == None:
        raise ValueError("Missing hydrus key")
    if api_port == None:
        raise ValueError("Missing api port")
    return str(hydrus_key), int(api_port)

def write_user_data():
    """Writes the user data/all known and saved data to the user_data.json file
    Returns:
        bool: sucessful or not
    """
    try:
        with open(USER_DATA_FILE, "w", encoding="utf-8") as json_file:
            data = {
                "api_opts" : {
                        "hydrus_key" : hydrus_key,
                        "api_port" : api_port,
                    },
                "compression_opts" : {
                        "compressed_img_quality" : compressed_img_quality,
                    }, 
                "resize_opts" : {
                    "should_resize" : should_resize,
                    "should_resize_by_percentage" : should_resize_by_percentage,
                    "resize_by_percentage" : resize_by_percentage,
                    "resize_by_pixel_height" : resize_by_pixel_height,
                    "resize_by_pixel_width" : resize_by_pixel_width,
                    },
            }
            json.dump(data, json_file)
    except FileNotFoundError as e:
        raise e
# write on close
atexit.register(write_user_data)

def read_user_json()->(str,int):
    """Method to read the JSON file for user data and set the according values found from there
    Returns:
    _type_: if sucessful will return a tuple of (str,int) that contains (hydrus api key, port number). 
    Otherwise wil return (reason for error: str, None)
    """
    try:
        with open(USER_DATA_FILE, "r", encoding="utf-8") as json_file:
            file_size = os.path.getsize(USER_DATA_FILE)
            if file_size == 0:
                raise FileNotFoundError
            data = json.load(json_file)
    except FileNotFoundError:
        print("Making new user data file!")
        json_file = open(USER_DATA_FILE, "w", encoding="utf-8").close()
        return
    except json.JSONDecodeError as ex:
        print("Found a corrupted datafile, making a new one")
        os.remove(USER_DATA_FILE)
        open(USER_DATA_FILE, "w", encoding="utf-8").close()
        raise ex
    
    # parse the data/json abd turn them into vars
    try:
        api_opts = data["api_opts"]
        for key, val in api_opts.items():
            globals()[key] = val
        
        compression_opts = data["compression_opts"]
        for key, val in compression_opts.items():
            globals()[key] = val
            
        resize_opts = data["resize_opts"]
        for key, val in resize_opts.items():
            globals()[key] = val
            
    except KeyError:
        print("Failed to read, so just overwriting with plain user data")
        write_user_data()
