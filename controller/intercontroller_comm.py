"""This will help handle intercommunication between the two input and output pane, etc.
    Allows connection of signals between input/output controllers
"""
from controller import input_controller, output_controller

input_controller_obj = None
output_controller_obj = None

def connect_input_output_controllers(
    input_controller_obj_in:input_controller.InputController, 
    output_controller_obj_in:output_controller.OutputController):
    """Connect all needed function emitters, etc

    Args:
        input_controller_obj (input_controller.InputController): controller for input or left panel
        output_controller_obj (output_controller.OutputController): controller for output or right panel
    """
    global input_controller_obj, output_controller_obj
    input_controller_obj = input_controller_obj_in
    output_controller_obj = output_controller_obj_in

    input_controller_obj.get_files_onclick_complete.connect(build_new_file_grid)

def build_new_file_grid():
    """Function to pass data from input controller to output controller.
        Called when we need to rebuild the file grid because the get files button has been clicked and new metadata is passed in.
    """
    output_controller_obj.size_type = input_controller_obj.size_type
    
    output_controller_obj.process_api_files_metadata(input_controller_obj.api_files_metadata)