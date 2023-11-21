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

# @pytest.fixture(scope="function")
# def override_open_w(monkeypatch):
#     def mock_open(*args, **kwargs):
#         class MockFile:
#             def close(self):
#                 if "w" not in args:
#                     super()
#             def __enter__(*args, **kwargs):
#                 if "w" not in args:
#                     super(args, kwargs)
#             def __exit__(*args, **kwargs):
#                 if "w" not in args:
#                     super(args)
#         return MockFile()
    
#     monkeypatch.setattr("builtins.open",mock_open)

@pytest.mark.order(1)
def test_good_user_json():
    """Tests if can read from a good input/user data json
    """
    good_user_file = "good_user_data.json"
    good_user_path = f"tests\\fake_user_data_files\\{good_user_file}"
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
    assert settings.get_api_info() == ('None', None)
    os.remove(temp_path)
    
@pytest.mark.order(3)
def test_corrupt_user_json(monkeypatch):
    """Tests if we have a somehow corrupted file, just clear it and make a new one
    """
    
    temp_user_file = "bad_user_data.json"
    temp_path = f"tests\\fake_user_data_files\\{temp_user_file}"
    
    # grab defaults again
    importlib.reload(settings)
    settings.USER_DATA_FILE = temp_path
    
    
     
    settings.read_user_json()
    
    assert os.path.exists(temp_path)
    assert settings.get_api_info() == ('None', None)

# @pytest.mark.order(4)
# def test_empty_file():
#     """Tests if we have a somehow empty file, just clear it and make a new one
#         This is a edge case variant of corrupted
#     """
    
#     temp_user_file = "nothingz.json"
#     temp_path = f"tests\\fake_user_data_files\\{temp_user_file}"
    
#     # grab defaults again
#     importlib.reload(settings)
#     settings.USER_DATA_FILE = temp_path
    
#     settings.read_user_json()
    
#     assert os.path.exists(temp_path)
#     assert settings.get_api_info() == ('None', None)
    
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
    
    # def mock_open(*args, **kwargs):
    #     class MockFile:
    #         def close(self):
    #             pass
    #         def __enter__(*args, **kwargs):
    #             pass
    #         def __exit__(*args, **kwargs):
    #             pass
    #     return MockFile()
    
    # monkeypatch.setattr("builtins.open",mock_open)
    
#     settings.USER_DATA_FILE = temp_path
    
#     settings.read_user_json()
    
#     assert os.path.exists(temp_path)
#     assert settings.get_api_info() == ('None', None)
    