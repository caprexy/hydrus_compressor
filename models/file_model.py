"""Models a file and all relevant information to that file
"""

class FileModel:
    """One individual file and all relevant data, may or may not have all data from the actual api call
    """
    file_id = size = -1
    mime = ""
    display_tags  = []
    pixmap = None
    
    def parse_api_metadata(self, file_data: dict):
        """takes the result of the api call for getting file metadata and processes it into the file object values

        Args:
            file_data (dict): given file data, is json as a dict
        """
        # using https://hydrusnetwork.github.io/hydrus/developer_api.html#get_files_file_hashes
        # we will use several hard coded values based on the json/list value of metadata/constants.FILE_ID_JSON_KEY
        self.file_id = file_data["file_id"]
        self.file_type, self.extension = file_data["mime"].split("/")
        self.size_bytes = file_data["size"]
        self.display_tags = file_data["tags"]["616c6c206b6e6f776e2074616773"] 
        
        #number is service key, see here https://hydrusnetwork.github.io/hydrus/developer_api.html#services_object
