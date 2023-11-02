"""Tests the input controller's functions except warning
"""

import pytest
from pytest import MonkeyPatch

from controller.input_controller import InputController, UserConfigWindow
from controller.helpers import api_file_processor
import controller.constants as constants


INITAL_HY_KEY = "sdsd"
NEW_HY_KEY = "aaa2"
INITAL_API_PORT = 22
NEW_API_PORT = 0

@pytest.mark.order(1)
@pytest.fixture(scope="module")
def input_controller():
    """Builds a input controller baased off of a json and uses that for all tests
    Yields:
        InputController: controller to test on
    """
    
    good_user_file = "good_user_data.json"
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(constants, "USER_DATA_FILE",f"tests\\fake_user_data_files\\{good_user_file}")
    
    input = InputController()
    
    hy_key, port = api_file_processor.user_info.get_user_info() 
    
    assert hy_key == INITAL_HY_KEY
    assert port == INITAL_API_PORT
    yield input
    
    monkeypatch.undo()

@pytest.mark.order(2)
def test_get_files_metadata(input_controller: InputController, mocker):
    """Just testing if the api_files_metadata got set and a signal is emitted. Cant
        test if the tags created request is made correctly yet.

    Args:
        input_controller (InputController): fixture setting up a inputcontroller
        mocker (_type_): function level mocker from pytest mock
    """
    
    mock_setter = mocker.patch('controller.helpers.api_file_processor.get_filtered_files_metadata_from_api')

    def flip():
        flip.switch = True
    flip.switch = False
    input_controller.get_files_metadata_complete.connect(flip)

    input_controller.get_files_metadata(
        1, "MB", True, True, True, True
    )
    expected = ['system:filesize > 1 MB', 
                'system:filetype is image', 
                'system:filetype is video',
                'system:inbox',
                'system:archive']
    mock_setter.assert_called_once_with(expected)
    
    assert flip.switch
    
    

@pytest.mark.order(2)
def test_set_config_vals(input_controller: InputController, qtbot, mocker):
    """tests user input of config window

    Args:
        input_controller (InputController): fixture input
        qtbot (_type_): qtbot to run qt 
        mocker (_type_): mocker fixture to use
    """
    userConfigWindow = UserConfigWindow(input_controller.userInfo)
    
    assert userConfigWindow.api_input.text() == str(INITAL_API_PORT)
    assert userConfigWindow.hydrus_key_input.text() == INITAL_HY_KEY
    # test possible bad user input
    userConfigWindow.api_input.setText("")
    userConfigWindow.remember_button.click()
    assert userConfigWindow.status_label.text() == "Missing api port"
    
    userConfigWindow.hydrus_key_input.clear()
    userConfigWindow.remember_button.click()
    assert userConfigWindow.status_label.text() == "No values set"
    
    
    userConfigWindow.api_input.setText("asdawdasdwdas")
    userConfigWindow.hydrus_key_input.setText(NEW_HY_KEY)
    userConfigWindow.remember_button.click()
    assert userConfigWindow.status_label.text() == "Need numeric value for port"
    
    userConfigWindow.api_input.setText(str(NEW_API_PORT))
    mock_setter = mocker.patch('models.user_model.UserInfo.set_user_info')
    mock_setter.return_value = True
    
    userConfigWindow.remember_button.click()
    assert userConfigWindow.status_label.text() == "Values set!"
    mock_setter.assert_called_once_with(hydrus_key=NEW_HY_KEY, api_port=NEW_API_PORT)
    
    userConfigWindow.close_button.click()
    userConfigWindow.close()
