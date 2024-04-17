from firebase_admin import firestore
from firebase import main_firebase as firebase

class FirebaseDatabase:

    def __init__(self) -> None:
        # init firebase
        firebase.initialize_firebase()

        # init database
        self.db = firestore.client()
        pass

    #
    # Example data
    # data = {
    #            'name': 'John Doe',
    #            'age': 30,
    #            'email': 'johndoe@example.com'
    #        }
    # Example collection
    # 'users'
    # Example document
    # 'user1'
    def save(self, data, collection, document):
        doc_ref = self.db.collection(collection).document(document)
        doc_ref.set(data)
        pass

    def get(self, collection, document):
        doc_ref = self.db.collection(collection).document(document)
        doc  = doc_ref.get()
        data = doc.to_dict()
        return data