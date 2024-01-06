from firebase_admin import db
from firebase import main_firebase as firebase

class Database:

    def __init__(self) -> None:
        # init firebase
        firebase.initialize_firebase()
        pass

    def update_node(self, node, key, dict):
        # Reference to your database
        ref = db.reference(f'/{node}/{key}')

        # Save data to the database
        ref.update(dict)
        pass