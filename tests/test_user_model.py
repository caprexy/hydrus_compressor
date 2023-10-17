"""Tests the user model
"""

from unittest.mock import patch, mock_open
import os

from models.user_model import UserInfo

TEST_DATA_FILE_NAME = "test.json"

def test_good_user_json():
    """Tests if can read from a good input/user data json
    """
    with open("tests\\fake_user_data_files\\good_user_data.json", encoding="utf-8") as json_file:
        file = json_file
        
        with patch("builtins.open", mock_open(read_data=file.read())):
            user = UserInfo()
    
    hy_key, port = user.get_user_info()

    assert hy_key == "sdsd"
    assert port == 22

def test_no_user_json():
    """Tests if bad input should get none back
    """
    with patch("constants.USER_DATA_FILE", new="Not a datafile") :
        user = UserInfo()
        assert (None, None) == user.get_user_info()

def test_bad_user_json():
    """Tests if bad input should get none back
    """
    with patch("constants.USER_DATA_FILE", new="tests\\fake_user_data_files\\bad_user_data.json") :

        user = UserInfo()    
        assert (None, None) == user.get_user_info()

def test_write_user_data():
    """Attempts to create a user with some fake file name then actually write data.
    """
    if os.path.exists(TEST_DATA_FILE_NAME):
        os.remove(TEST_DATA_FILE_NAME)
    with patch("constants.USER_DATA_FILE", new=TEST_DATA_FILE_NAME) :
        user = UserInfo()
        assert user.write_user_data() is False
        user.set_user_info("3af",33)
    
    with open(TEST_DATA_FILE_NAME, encoding="utf-8") as file:
        file = file.read()
    
    if os.path.exists(TEST_DATA_FILE_NAME):
        os.remove(TEST_DATA_FILE_NAME)

def test_missing_permutations():
    """If by chance somehow we are missing data, want to check that we covered it
    """
    user = UserInfo()
    user.set_user_info("3af",None)
    assert user.write_user_data() is False
    
    
    user.set_user_info(None, 44)
    assert user.write_user_data() is False
    
    user.set_user_info(None, None)
    assert user.write_user_data() is False
    
    
    user.set_user_info("5","zz")
    assert user.write_user_data() is False
    
    user.set_user_info(3, 5)
    assert user.write_user_data() is True
    
    