import pytest
from controller.input_controller import InputController
from controller.helpers import api_file_processor
import controller.constants as constants

@pytest.mark.order(1)
@pytest.fixture(scope="module")
def make_input_controller(monkeypatch):
    
    good_user_file = "good_user_data.json"
    monkeypatch.setattr(constants, "USER_DATA_FILE",f"tests\\fake_user_data_files\\{good_user_file}")
    
    input = InputController()
    
    hy_key, port = api_file_processor.user_info.get_user_info() 
    
    assert hy_key == "sdsd"
    assert port == 22
    return input

# @pytest.mark.order(2)
# def test_get_files_metadata():
#     input_controller = make_input_controller