from firebase import storage, firestore, messaging
from configuration import reader_conf as reader
#from models import plants_analyzer as analyzer
import DHT11
import time

def update_gardens(gardens, data):
    print("Update gardens call")
    pass

reader = reader.ConfReader()
def main():

    print('Init main')

    # Get sensor data
    data = [10, 2, 4] # Fake data


    while True:

        sensor = DHT11.DHTClass()
        sensor.read()
        time.sleep(2)

        pass


    # Get gardens to update
    gardens = reader.get_gardens()
    update_gardens(gardens, data)

    # Analyze
    model = analyzer.PlantAnalyzer()
    model.getWebcamResult()
    
    # Pause and restart
    time.sleep(10)
    pass

if __name__ == "__main__":
    main()

#######################
# Save into Firestore #
#######################
firestore_manager = firestore.FirebaseDatabse()
data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'johndoe@example.com'
}
firestore_manager.save(data, 'user', 'user1')
firestore_manager.get('user', 'user1')


##############################
# Save images into storage   #
##############################
storage_manager = storage.ImagesStorage()
storage_manager.save_image('C:\\Users\\em-hp2\\Desktop\\Works\\Python\\FirebaseProject\\README.md', 'test/test.md')


#####################
# Send notification #
#####################
message_manager = messaging.Messaging()
message_manager.sendMessage('title_test', 'body_test')
