import firebase_admin
from firebase_admin import credentials

# Firebase cerdentials
print("|***************|")
print("| Init firebase |")
print("|_______________|")
firebase_credential = credentials.Certificate('firebase_credential/smartgarden-d7604-firebase-adminsdk-3jub3-f91a3cb778.json')

initialized = False
def init_private_firebase():
    global initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(firebase_credential, {
            'storageBucket': 'smartgarden-d7604.appspot.com'
        })
        initialized = True

def initialize_firebase():
    global initialized
    if not initialized:
        init_private_firebase()