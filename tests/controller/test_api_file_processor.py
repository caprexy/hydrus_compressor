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
        def get_user_info(self) -> (str, int):
            return ("1",2)
    api_file_processor.set_user_info(FakeUserInfo())

FILTERED_FILE_JSON_LOCATION = ".\\tests\\controller\\get_file_metadata_test.json"
def test_get_filtered_files(monkeypatch):
    
    # fake the api call
    class FakeRes(requests.Response):
        def __init__(self) -> None:
            super().__init__()
        def json(self):
            with open(FILTERED_FILE_JSON_LOCATION, 'r') as file:
                return json.load(file)
            
    def fakeGet(url, headers, params, timeout):
        return FakeRes()
    monkeypatch.setattr(requests, "get", fakeGet)
    
    taglist = []
    res = api_file_processor.get_filtered_files_metadata_from_api(taglist)
    
    json_data = None
    with open(FILTERED_FILE_JSON_LOCATION, 'r') as file:
        json_data =  json.load(file)

    assert res == json_data[constants.FILE_LIST_METADATA_KEY]