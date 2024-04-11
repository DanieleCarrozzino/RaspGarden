from firebase_admin import storage
from firebase import main_firebase as firebase
import os

# Save images inside my personal 
# storage space

class ImagesStorage:

    def __init__(self) -> None:
        # init firebase
        firebase.initialize_firebase()

        # Get personal code
        self.code = firebase.getPersonalCode()

        # Access your storage bucket
        self.bucket = storage.bucket()
        pass

    def save_image(self, file_path, destination_path):
        blob = self.bucket.blob(destination_path)
        blob.upload_from_filename(file_path)
        pass

    def save_image_from_file_name(self, file_path, file_name, folder = "Pictures"):
        blob = self.bucket.blob(f"{self.code}/{file_name}")
        blob.upload_from_filename(file_path)

        # delete the oldest
        self.delete_the_oldest(folder)
        pass

    def delete_the_oldest(self, folder):        
        # Get the entire list of instant pictures 
        blobs = list(self.bucket.list_blobs(prefix=f"{self.code}/{folder}"))

        # If the length is more than 20 
        # I have to delete all the oldest 
        # images stored into my storage
        if(len(blobs) > 20):
            count = len(blobs) - 20
            for i in range(0, count):
                print(blobs[i].name)
                blobs[i].delete()
                pass
        pass

    def downloadFile(self):
        blob = self.bucket.blob('smartgarden-d7604.appspot.com/rasp_test_code1/Timelaps/timelaps.mp4')
        
        # Download the file to a local file
        destination_path = os.path.join(os.getcwd(), "timelaps.mp4")
        blob.download_to_filename(destination_path)
        pass

    pass