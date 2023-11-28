"""Tests the settings model
"""
import os
import json
import shutil
import pytest 
import importlib

from pytest import raises

import models.settings as settings
import controller.constants as constants

GOOD_USER_FILE = "good_user_data.json"
@pytest.mark.order(1)
def test_good_user_json():
    """Tests if can read from a good input/user data json
    """
    GOOD_USER_FILE = "good_user_data.json"
    good_user_path = f"tests\\fake_user_data_files\\{GOOD_USER_FILE}"
    settings.USER_DATA_FILE = good_user_path
    
    settings.read_user_json()
    
    hy_key, port = settings.get_api_info()

    assert hy_key == "3a"
    assert port == 5

@pytest.mark.order(2)
def test_no_user_json():
    """Tests if we do not have a user file, we should create one based on hardcoded values
    """
    
    temp_user_file = "temp.json"
    temp_path = f"tests\\fake_user_data_files\\{temp_user_file}"
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    # grab defaults again
    importlib.reload(settings)
    settings.USER_DATA_FILE = temp_path
    
    settings.read_user_json()
    
    assert os.path.exists(temp_path)
    with pytest.raises(ValueError):
        settings.get_api_info()
    os.remove(temp_path) # this appears to be unable to finish before funciton done
    
@pytest.mark.order(3)
def test_corrupt_user_json(monkeypatch):
    """Tests if we have a somehow corrupted file, just clear it and make a new one
    """
    
    temp_user_file = "bad_user_data.json"
    bad_temp_path = f"tests\\fake_user_data_files\\{temp_user_file}"
    
    good_temp_path = f"tests\\fake_user_data_files\\{GOOD_USER_FILE}"
    
    if os.path.exists(bad_temp_path):
        os.remove(bad_temp_path)
        
    # make bad file
    with open(good_temp_path, 'r') as source:
        content = source.read()
    bad_content = content[:len(content)//2]
    with open(bad_temp_path, 'w') as source:
        source.write(bad_content)
        
    # grab defaults again
    importlib.reload(settings)
    settings.USER_DATA_FILE = bad_temp_path
    
    settings.read_user_json()
    
    assert os.path.exists(bad_temp_path)
    with pytest.raises(ValueError):
        assert settings.get_api_info()
    os.remove(bad_temp_path)

@pytest.mark.order(4)
def test_empty_file():
    """Tests if we have a somehow empty file, just clear it and make a new one
        This is a edge case variant of corrupted
    """
    
    # create empty file
    temp_user_file = "nothingz.json"
    empty_file_path = f"tests\\fake_user_data_files\\{temp_user_file}"
    with open(empty_file_path, 'w'):
        pass
    
    # grab defaults again
    importlib.reload(settings)
    settings.USER_DATA_FILE = empty_file_path
    
    settings.read_user_json()
    
    assert os.path.exists(empty_file_path)
    with pytest.raises(ValueError):
        settings.get_api_info() == ('None', None)
    
# @pytest.mark.order(5)
# def test_weird_user_json(monkeypatch):
#     """ This tests for good json but unexpected values
#     """
    
#     temp_user_file = "weird.json"
#     temp_path = f"tests\\fake_user_data_files\\{temp_user_file}"
#     if os.path.exists(temp_path):
#         os.remove(temp_path)
    
#     # grab defaults again
#     importlib.reload(settings)
    
#     def mock_open(*args, **kwargs):
#         class MockFile:
#             def close(self):
#                 pass
#             def __enter__(*args, **kwargs):
#                 pass
#             def __exit__(*args, **kwargs):
#                 pass
#         return MockFile()
    
#     monkeypatch.setattr("builtins.open",mock_open)
    
#     settings.USER_DATA_FILE = temp_path
    
#     settings.read_user_json()
    
#     assert os.path.exists(temp_path)
#     assert settings.get_api_info() == ('None', None)
    