"""This will help handle intercommunication between the two input and output pane, etc
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

    input_controller_obj.get_files_complete.connect(trigger_build_file_grid)

def trigger_build_file_grid():
    """Function to pass data from input controller to output controller
    """
    output_controller_obj.set_file_options(
        input_controller_obj.size_type,
    )
    
    output_controller_obj.set_files(input_controller_obj.api_file_objects)
    output_controller_obj.build_file_table()