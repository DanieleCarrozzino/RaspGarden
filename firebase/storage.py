from firebase_admin import storage
from firebase import main_firebase as firebase

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

        print("File uploaded to Firebase Storage successfully.")
        pass

    def save_image_from_file_name(self, file_path, file_name):

        print(f">>> Final destination path : {self.code}/{file_name}")
        blob = self.bucket.blob(f"{self.code}/{file_name}")
        blob.upload_from_filename(file_path)
        print(">>> File uploaded to Firebase Storage successfully.")
        pass

    pass