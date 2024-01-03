from firebase import storage, firestore, messaging
from configuration import reader_conf as reader
from models import plants_analyzer as analyzer
from raspberry.sensors import DHT11
import time

def update_gardens(gardens, data):
    print(">> Update gardens call")
    pass

reader = reader.ConfReader()
def main():

    print("|***********************|")
    print('| Start watching garden |')
    print("|***********************|")
    print("| - Daniele carrozzino  |")
    print("|_______________________|")

    while True:

        print("> Starting loop")
        print("> Get Data")

        # Get sensor data
        data = []

        # Temperature and humidity
        sensor = DHT11.DHTClass()
        temperature, humidity = sensor.read()
        data.append(temperature)
        data.append(humidity)

        print("> Updtae gardens")

        # Get gardens to update
        gardens = reader.get_gardens()
        update_gardens(gardens, data)

        print("> Analyze the result")

        # Analyze
        model = analyzer.PlantAnalyzer()
        model.getWebcamResult()

        print("> Sleep to restart")

        # Pause and restart
        time.sleep(10)

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
