print("Firebase")
from firebase import storage, firestore, messaging, database
print("Configuration")
from configuration import reader_conf
print("Models")
#from models import plants_analyzer as analyzer
print("Sensors")
from raspberry.sensors import DHT11
from raspberry.sensors import ADS1115
from raspberry.camera import rasp_camera as Camera
print("Others")
import time
from collections import deque

# Const
MAX_VALUES = 30

# Init class
sensor_temperature  = DHT11.DHTClass()
sensor_moisture     = ADS1115.ADS1115Class()
camera = Camera.PiCamera()
reader = reader_conf.ConfReader()
# Firebase
firebase_database = database.Database()

# Old data to analyze
old_data = {
    "temperatures": deque(maxlen = MAX_VALUES),
    "humidity": deque(maxlen = MAX_VALUES),
    "soil_moistures":deque(maxlen = MAX_VALUES)
    }

# New data
avarage_temperature     = 0
avarage_humidity        = 0
avarage_soil_moisture   = 0



def update_gardens(gardens):
    print(">> Update gardens call")
    for garden in gardens:
        print('Send uodate to:')
        print(garden)
        firebase_database.update_node('gardens', garden, old_data)
    pass



#
# Get new data
#
# get new data from all the sensors,
# connected to the raspberry and return
# a dictionary with the results
#
# Temperature
# Humidity
# Soil moisture
#
def get_new_data():

    # Dictionary of results
    sensor_results = dict()

    # Temperature
    # Humidity
    temperature, humidity = sensor_temperature.read()
    sensor_results['temperature']   = temperature
    sensor_results['humidity']      = humidity

    # Soil moisture
    values = sensor_moisture.read()
    sensor_results['moisture'] = values
    
    return sensor_results


def processing_data(dict : dict):

    old_data["temperatures"].append(dict['temperature'])
    old_data["humidity"].append(dict['humidity'])
    old_data["soil_moistures"].append(dict['moisture'])

    avarage_temperature     = 0
    avarage_humidity        = 0
    avarage_soil_moisture   = 0

    for temperature in old_data["temperatures"]:
        avarage_temperature += temperature
    avarage_temperature = avarage_temperature / len(old_data["temperatures"])

    for humidity in old_data["humidity"]:
        avarage_humidity += humidity
    avarage_humidity = avarage_humidity / len(old_data["humidity"])

    for soil_moisture in old_data["soil_moistures"]:
        avarage_soil_moisture += soil_moisture[0]
    avarage_soil_moisture = avarage_soil_moisture / len(old_data["soil_moistures"])
    
    print(old_data)


def main():

    print("|***********************|")
    print('| Start watching garden |')
    print("|***********************|")
    print("| - Daniele carrozzino  |")
    print("|_______________________|")

    print("> Starting loop")
    while True:

        print("> Get sensors result")
        # All sensors result
        dict_result = get_new_data()

        print("> Processing data")
        # Process all data
        processing_data(dict_result)

        print("> Update gardens")
        # Get gardens to update
        gardens = reader.get_gardens()
        update_gardens(gardens)

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
