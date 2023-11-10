"""Tests the user model
"""
import os
import json
import shutil
import pytest 

from pytest import raises

from models.user_model import UserInfo
import controller.constants as constants


@pytest.fixture(scope="function")
def user_obj(monkeypatch, request):
    UserInfo._instance = None
    good_user_file = "good_user_data.json"
    good_user_path = f"tests\\fake_user_data_files\\{good_user_file}"
    
    user_json_location = request.param or good_user_path
    
    monkeypatch.setattr(constants,"USER_DATA_FILE", user_json_location)
    user = UserInfo()
    yield user
    del user
    UserInfo._instance = None


@pytest.mark.order(1)
@pytest.mark.parametrize('user_obj', [None], indirect=True)
def test_good_user_json(user_obj):
    """Tests if can read from a good input/user data json
    """
    hy_key, port = user_obj.get_api_info()

    assert hy_key == "3a"
    assert port == 5


temp_user_file = "temp.json"
empty_path = f"tests\\fake_user_data_files\\{temp_user_file}"
@pytest.mark.order(2)
@pytest.mark.parametrize('user_obj', [empty_path], indirect=True)
def test_no_user_json(user_obj):
    """Tests if we do not have a user file, we should create one
    """
    assert (None, None) == user_obj.get_api_info()
    
    # assert os.path.exists(empty_path)
    # os.remove(empty_path)

# def test_bad_user_json(monkeypatch):
#     """Tests if bad input should build a new file
#     """
#     bad_user_file_origin = "tests\\fake_user_data_files\\bad_user_data.json"
#     new_path = "tests\\fake_user_data_files\\bad_user_data_temp.json"
#     shutil.copy2(bad_user_file_origin, new_path)
        
#     monkeypatch.setattr(constants, "USER_DATA_FILE",new_path)
    
#     with raises(json.decoder.JSONDecodeError):
#         user = UserInfo()    
#         assert (None, None) == user.get_api_info()
    
#     assert os.path.exists(new_path)
#     os.remove(new_path)

# def test_write_user_data(monkeypatch):
#     """Attempts to create a user and write data to it and get it back
#     """
#     TEST_DATA_FILE_NAME = "temp.json"
#     monkeypatch.setattr(constants, "USER_DATA_FILE",TEST_DATA_FILE_NAME)
    
#     user = UserInfo()
#     with raises(ValueError):
#         user.write_user_data()
        
#     new_key = "3af"
#     new_port = 33
#     user.set_user_info(new_key,new_port)
#     user.write_user_data()

#     with open(TEST_DATA_FILE_NAME, encoding="utf-8") as file:
#         file_json = json.load(file)
    
#     hydrus_key, api_port = user.get_api_info()
    
#     assert hydrus_key == file_json["hydrus_key"] == new_key
#     assert api_port == file_json["port"] == new_port
    
#     if os.path.exists(TEST_DATA_FILE_NAME):
#         os.remove(TEST_DATA_FILE_NAME)

# def test_missing_permutations():
#     """If by chance somehow we are missing data, want to check that we covered it
#     """
#     user = UserInfo()
    
#     with raises(ValueError):
#         user.set_user_info("3af",None)
    
#     with raises(ValueError):
#         user.set_user_info(None, 44)
        
#     with raises(ValueError):    
#         user.set_user_info(None, None)
        
#     with raises(ValueError):
#         user.set_user_info("5","zz")
    
#     user.set_user_info(3, 5)
