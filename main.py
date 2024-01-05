print("Firebase")
from firebase import storage, firestore, messaging
print("Configuration")
from configuration import reader_conf as reader
print("Models")
#from models import plants_analyzer as analyzer
print("Sensors")
from raspberry.sensors import DHT11
from raspberry.camera import rasp_camera as Camera
print("Others")
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

    # Init class
    sensor = DHT11.DHTClass()
    camera = Camera.PiCamera()

    while True:

        print("> Starting loop")
        print("> Get Data")

        # Get sensor data
        data = []

        print("> Get temperature and humidity")
        # Temperature and humidity
        temperature, humidity = sensor.read()
        data.append(temperature)
        data.append(humidity)

        print("> Update gardens")
        # Get gardens to update
        gardens = reader.get_gardens()
        update_gardens(gardens, data)

        print("> Get picture")
        camera.capture("./test_photo")

        print("> Analyze the result")
        # Analyze
        # model = analyzer.PlantAnalyzer()
        # model.getWebcamResult()

        print("> Sleep to restart")
        # Pause and restart
        time.sleep(5)

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
