
from controller.helpers import api_file_processor
from models.user_model import UserInfo

api_file_processor.set_user_info(UserInfo())

tags_list = [
        "system:filesize > "+str(10) + " "+ "MB",
        ]

tags_list.append("system:filetype is image")

api_file_processor.get_filtered_files_metadata_from_api(tags_list)