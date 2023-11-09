import pytest
import requests
import json
from controller.helpers import api_file_processor
from controller import constants

from models.user_model import UserInfo

@pytest.mark.order(1)
@pytest.fixture(autouse=True)
def mock_user_info():
    class FakeUserInfo(UserInfo):
        def __init__(self):
            pass
        def get_api_info(self) -> (str, int):
            return ("1",2)
    api_file_processor.set_user_info(FakeUserInfo())

FILTERED_FILE_JSON_LOCATION = ".\\tests\\fake_user_data_files\\request_metadata_raw.json"
FILE_SEARCH_JSON_LOCATION = ".\\tests\\fake_user_data_files\\raw_get_file_search.json"
@pytest.mark.order(2)
def test_get_filtered_files(monkeypatch):
    # fake the api call
    class FilteredFakeRes(requests.Response):
        def __init__(self) -> None:
            super().__init__()
        def json(self):
            with open(FILTERED_FILE_JSON_LOCATION, 'r') as file:
                return json.load(file)
    class SearchFakeRes(requests.Response):
        def __init__(self) -> None:
            super().__init__()
        def json(self):
            with open(FILE_SEARCH_JSON_LOCATION, 'r') as file:
                return json.load(file)
    def fakeGet(url, headers, params, timeout):
        if api_file_processor.GET_FILE_SEARCH in url:
            return SearchFakeRes()
        return FilteredFakeRes()
    
    monkeypatch.setattr(requests, "get", fakeGet)
    
    # build tags
    tags_list = [
                "system:filesize > "+str(10) + " MB",
                ]
        
    tags_list.append("system:filetype is image")
    tags_list.append("system:archive")
    
    api_file_processor.get_filtered_files_metadata_from_api(tags_list)
    # print(res)
    # json_data = None
    # with open(FILTERED_FILE_JSON_LOCATION, 'r') as file:
    #     json_data =  json.load(file)

    # assert res == json_data[constants.FILE_LIST_METADATA_KEY]