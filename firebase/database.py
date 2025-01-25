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

    # Update a value of this raspberry
    # Inside the module "raspberry/my_code"
    def update_personal_node(self, data):
        ref = db.reference(f'/raspberry/{firebase.getPersonalCode()}')
        old_data = self.get_personal_data()
        ref.update(old_data | data)
        pass

    # Observe node
    # observe a specific node to 
    # be able to react instantly 
    # to the changes
    def observe_node(self, node, callback):
        ref = db.reference(f'/{node}')
        def stream_handler(message):
            callback(message.data)
        ref.listen(stream_handler)

    def observe_specific_data(self, element, callback):
        ref = db.reference(f'/raspberry/{firebase.getPersonalCode()}/{element}')
        def stream_handler(message):
            callback(message.data)
        ref.listen(stream_handler)

    def get_personal_data(self):
        ref     = db.reference(f'/raspberry/{firebase.getPersonalCode()}')
        data    = ref.get()
        return data