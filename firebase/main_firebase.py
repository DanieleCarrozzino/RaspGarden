import firebase_admin
from firebase_admin import credentials

# Firebase cerdentials
print("|***************|")
print("| Init firebase |")
print("|_______________|")
personal_firebase_code = "rasp_test_code1"
firebase_credential = credentials.Certificate('firebase_credential/smartgarden-d7604-firebase-adminsdk-3jub3-f91a3cb778.json')

initialized = False
def init_private_firebase():
    global initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(firebase_credential, {
            'storageBucket': 'smartgarden-d7604.appspot.com',
            'databaseURL': "https://smartgarden-d7604-default-rtdb.europe-west1.firebasedatabase.app/"
        })
        initialized = True

def initialize_firebase():
    global initialized
    if not initialized:
        init_private_firebase()

def getPersonalCode():
    return personal_firebase_code