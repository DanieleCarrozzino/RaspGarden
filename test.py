print("Firebase")
from firebase import storage, firestore, messaging, database, main_firebase

db = database.Database()
data = db.get_personal_data()

print(data['activated'])