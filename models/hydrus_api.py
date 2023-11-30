"""Contains all logic to call API and parse the return values, 
    gives back api results in a nice way but does not format for UI use, that's 
    the controller's responsibility
"""
import json
import requests
import numpy as np
import cv2
from urllib3.exceptions import NewConnectionError

from PyQt6.QtCore import Qt, QThreadPool, QRunnable
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication, QPushButton
import controller.constants as constants
import models.settings as settings

# API endpoints
GET_FILE_SEARCH = "/get_files/search_files"
GET_FILE_METADATA = "/get_files/file_metadata"
GET_FILE_THUMBNAIL = "/get_files/thumbnail"
GET_FULL_FILE = "/get_files/file"
POST_FILE = "/add_files/add_file"
ADD_TAGS = "/add_tags/add_tags"
DELETE_FILE = "/add_files/delete_files"
EDIT_RATINGS = "/edit_ratings/set_rating"
ADD_NOTES = "/add_notes/set_notes"

def warning(reason:str, exec=True):
    """Creates a warning popup with given reason

    Args:
        reason (str): Text to be put into warning box
        exec (bool): if to use exec or open
    """
    warning_window = QDialog()
    warning_window.setWindowTitle("Warning!!!!!")
    warning_window_layout = QVBoxLayout()
    warning_window.setLayout(warning_window_layout)


    reason_label = QLabel(reason)
    warning_window_layout.addWidget(reason_label)

    close_button = QPushButton('Close', warning_window)
    close_button.clicked.connect(warning_window.accept)
    warning_window_layout.addWidget(close_button)
    
    if exec:
        warning_window.exec()
    else:
        warning_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        warning_window.open()
    return warning_window

def get_filtered_files_metadata_from_api(tags_list: list[str])->[]:
    """Actually calls the api given the tags to describe what we want like videos, etc.
        Since is specialized we will be using a thread to not block main.

    Args:
        tags (list[str]): list of rules like should be a video, in inbox or archive
    """
    
    warning_window = warning("Getting files", exec=False)
    QApplication.processEvents()
    
    try:
        hydrus_key, api_port  = settings.get_api_info()
        res = requests.get(
            url=constants.LOCALHOST+str(api_port)+GET_FILE_SEARCH,
            headers={
                constants.HYDRUS_APIKEY_PARAM : hydrus_key,
            },
            params={
                "tags" : json.dumps(tags_list)
            },
            timeout= 5
        )
        file_ids = res.json()[constants.FILE_ID_JSON_KEY]
        
        res = requests.get(
            url=constants.LOCALHOST+str(api_port)+GET_FILE_METADATA,
            headers={
                constants.HYDRUS_APIKEY_PARAM : hydrus_key,
            },
            params={
                constants.FILE_ID_JSON_KEY : json.dumps(file_ids),
                "include_notes" : "true",
            },
            timeout= 5
        )
        
        return res.json()[constants.FILE_LIST_METADATA_KEY]
    except ValueError as e:
        warning(e)
    except requests.exceptions.ConnectionError as e:
        warning("Is hydrus running?")
    except KeyError as e:
        warning("Nothing found for the given settings")
    except Exception as e:
        print("Caught an exception of type:", type(e).__name__, f" and error message: {e}")
    finally:
        warning_window.close()
    return None
        

def get_file_thumbnail(file_id:str)-> QPixmap:
    """Grabs a file's thumbnail as generated by hydrus. Uses API call for now

    Args:
        api_port (int): port of client api
        hydrus_key (str): key for hydrus api program
        file_id (str): id of file

    Returns:
        QPixmap: pixmap of the thumbnail
    """
    hydrus_key, api_port = settings.get_api_info()
    res = requests.get(
        url=constants.LOCALHOST+str(api_port)+GET_FILE_THUMBNAIL,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
        },
        params={
            "file_id": file_id
        },
        timeout= 10
    )

    pixmap = QPixmap()
    pixmap.loadFromData(res.content) #loading from bytes of contenta
    return pixmap

def get_full_image(file_id:str):
    """Grabs a file's full resolution image. Uses API call for now and also uses PIL's image objects

    Args:
        api_port (int): port of client api
        hydrus_key (str): key for hydrus api program
        file_id (str): id of file

    Returns:
        Image: full sized Image object based on API response
    """
    hydrus_key, api_port = settings.get_api_info()
    res = requests.get(
        url=constants.LOCALHOST+str(api_port)+GET_FULL_FILE,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
        },
        params={
            "file_id": file_id
        },
        timeout= 10
    )
    
    img_array = np.frombuffer(res.content, dtype=np.uint8)
    img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
    
    return img

def send_to_hydrus(file_path: str):
    hydrus_key, api_port = settings.get_api_info()
    res = requests.post(
        url=constants.LOCALHOST+str(api_port)+POST_FILE,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
            "Content-Type" : "application/json",
        },
        data =json.dumps({
            "path": file_path
        }),
        timeout= 10
    )
    return res.json()

def add_tags_hash(new_hash, storage_tags):
    hydrus_key, api_port = settings.get_api_info()
    reformatted_tags = {}
    
    res = requests.get(
        url=constants.LOCALHOST + str(api_port) + "/get_services",
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,        
        },
        timeout= 10
    ) 
    data = res.json()
    
    wanted_services = []
    for item in data["local_tags"]:
        wanted_services.append(item["service_key"])

    for service_id in storage_tags:
        if service_id not in wanted_services:
            continue
        reformatted_tags[service_id] = {}
        if storage_tags[service_id].get('0', -1) != -1:
            reformatted_tags[service_id]['0'] = storage_tags[service_id]['0']
        if storage_tags[service_id].get('1', -1) != -1:
            reformatted_tags[service_id]['2'] = storage_tags[service_id]['1']
        if storage_tags[service_id].get('2', -1) != -1:
            reformatted_tags[service_id]['1'] = storage_tags[service_id]['2']  
        if storage_tags[service_id].get('3', -1) != -1:
            reformatted_tags[service_id]['4'] = storage_tags[service_id]['3']
    
    res = requests.post(
        url=constants.LOCALHOST+str(api_port)+ADD_TAGS,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,        
        },
        json ={
            "service_keys_to_actions_to_tags": reformatted_tags,
            "hash": new_hash,
        },
        timeout= 10
    )
    return res

def add_ratings(new_hash, rating_services):
    hydrus_key, api_port = settings.get_api_info()
    for service in rating_services:
        res = requests.post(
            url=constants.LOCALHOST+str(api_port)+EDIT_RATINGS,
            headers={
                constants.HYDRUS_APIKEY_PARAM : hydrus_key,        
            },
            json ={
                "rating_service_key": service,
                "hash": new_hash,
                "rating": rating_services[service]
            },
            timeout= 10
        )
    return res

def add_notes(new_hash, notes):
    hydrus_key, api_port = settings.get_api_info()

    res = requests.post(
        url=constants.LOCALHOST+str(api_port)+ADD_NOTES,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,        
        },
        json ={
            "notes": notes,
            "hash": new_hash,
        },
        timeout= 10
    )

def delete_file(file_id):
    hydrus_key, api_port = settings.get_api_info()
    
    res = requests.post(
        url=constants.LOCALHOST+str(api_port)+DELETE_FILE,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
            "Content-Type" : "application/json",
        },
        data =json.dumps({
            "file_id" : file_id
        }),
        timeout= 10
    )