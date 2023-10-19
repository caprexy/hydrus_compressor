"""Contains all logic to call API and parse the return values, gives back api results in a nice way
"""
import json
import requests

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
    file_ids = res.json()[constants.FILE_ID_JSON_KEY][:2] ### IMPORTANT WE'VE LIMITED FOR TESTING
    
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
        files_obj_list.append(file)
    
    return files_obj_list