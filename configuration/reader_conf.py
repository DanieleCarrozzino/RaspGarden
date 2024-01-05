import os 
import json

current_folder      = os.path.dirname(__file__)
config_files_folder = os.path.join(current_folder, "files")

# 
#   Need to get all data associated 
#   to this raspberry, every time a 
#   new user linked with this raspberry
#   he uploads a new config file with
#   only 2 informations
#   garden_id
#   user_token 
#
#   garden_id to know on which garden
#   I must update data
#   user_token to be able to send custom
#   notifications
#
#
#   the files are configurated ins this way:
#   
#   {
#       "garden_id":"...",
#       "user_token":"..."
#   }
#
#
class ConfReader:

    def __init__(self) -> None:
        self.token_list     = list()
        self.garden_list    = list()
        pass

    def readConfig(self):
        
        # Get the list of files in the folder
        print(config_files_folder)
        file_list = os.listdir(config_files_folder)
        if file_list == None:
            return

        # Print the list of files
        for file_name in file_list:

            # Get the full path
            file_path = os.path.join(config_files_folder, file_name)

            # Open and read the JSON file
            with open(file_path, 'r') as file:
                json_data = json.load(file)

            # Accessing values from the JSON data
            print("garden_id:", json_data['garden_id'])
            print("user_token:", json_data['user_token'])

            self.token_list.append(json_data['user_token'])
            self.garden_list.append(json_data['garden_id'])
            pass

    def get_tokens(self):

        # To be sure to read all the config.
        # I have not any listener if a new user
        # upload a new config file
        self.readConfig()
        
        return self.token_list
    
    def get_gardens(self):

        # To be sure to read all the config.
        # I have not any listener if a new user
        # upload a new config file
        self.readConfig()
        
        return self.garden_list