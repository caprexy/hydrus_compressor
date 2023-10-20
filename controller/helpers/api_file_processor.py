"""Contains all logic to call API and parse the return values, gives back api results in a nice way
"""
import json
import requests

from PyQt6.QtGui import QPixmap

import constants
from models.file_model import FileModel

def get_files_from_api(api_port:int, hydrus_key:str, tags_list: list[str]):
    """Actually calls the api given the tags to describe what we want like videos, etc

    Args:
        tags (list[str]): list of rules like should be a video, in inbox or archive
    """
    
    res = requests.get(
        url=constants.LOCALHOST+str(api_port)+constants.GET_FILE_SEARCH,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
        },
        params={
            "tags" : json.dumps(tags_list)
        },
        timeout= 10
    )
    file_ids = res.json()[constants.FILE_ID_JSON_KEY][:10]
       
    res = requests.get(
        url=constants.LOCALHOST+str(api_port)+"/get_files/file_metadata",
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
        },
        params={
            constants.FILE_ID_JSON_KEY : json.dumps(file_ids)
        },
        timeout= 10
    )
    
    files_obj_list = []
    
    for file_metadata in res.json()[constants.FILE_LIST_METADATA_KEY]:
        file = FileModel()
        file.parse_api_metadata(file_metadata)
        file.pixmap = get_file_thumbnail(api_port, hydrus_key, file.file_id)
        
        files_obj_list.append(file)
    
    return files_obj_list

# could rewrite to use path directly by having user fed in thumbnail dir
def get_file_thumbnail(api_port:int, hydrus_key:str, file_id:str):
    res = requests.get(
        url=constants.LOCALHOST+str(api_port)+constants.GET_FILE_THUMBNAIL,
        headers={
            constants.HYDRUS_APIKEY_PARAM : hydrus_key,
        },
        params={
            "file_id": file_id
        },
        timeout= 10
    )

    pixmap = QPixmap()
    pixmap.loadFromData(res.content)
    return pixmap
