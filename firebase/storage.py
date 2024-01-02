from firebase_admin import storage
from firebase import main_firebase as firebase

# Save images inside my personal 
# storage space

class ImagesStorage:

    def __init__(self) -> None:
        # init firebase
        firebase.initialize_firebase()

        # Access your storage bucket
        self.bucket = storage.bucket()
        pass

    def save_image(self, file_path, destination_path):

        blob = self.bucket.blob(destination_path)
        blob.upload_from_filename(file_path)

        print("File uploaded to Firebase Storage successfully.")
        pass

    pass