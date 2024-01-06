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
import queue

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
    "temperatures": queue.Queue(MAX_VALUES),
    "humidity": queue.Queue(MAX_VALUES),
    "soil_moistures": queue.Queue(MAX_VALUES)
    }

# New data
avarage_temperature     = 0
avarage_humidity        = 0
avarage_soil_moisture   = 0


#
# Update gardens
#
# update the real time database
# with all the processing data 
# get during this loop
#
def update_gardens(gardens):
    print(">> Update gardens call")
    for garden in gardens:
        print('Send update to:')
        print(garden)

        serializable_data = old_data
        serializable_data["temperatures"]   = list(serializable_data["temperatures"])
        serializable_data["humidity"]       = list(serializable_data["humidity"])
        serializable_data["soil_moistures"] = list(serializable_data["soil_moistures"])
        serializable_data['avarage_temperature']    = avarage_temperature
        serializable_data['avarage_humidity']       = avarage_humidity
        serializable_data['avarage_soil_moisture']  = avarage_soil_moisture
        firebase_database.update_node('gardens', garden, serializable_data)
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

    old_data["temperatures"].put(dict['temperature'])
    old_data["humidity"].put(dict['humidity'])
    old_data["soil_moistures"].put(dict['moisture'])

    avarage_temperature     = 0
    avarage_humidity        = 0
    avarage_soil_moisture   = 0

    for i in range(len(old_data["temperatures"])):
        avarage_temperature += old_data["temperatures"][i]
    avarage_temperature = avarage_temperature / len(old_data["temperatures"])

    for i in range(len(old_data["humidity"])):
        avarage_humidity += old_data["humidity"][i]
    avarage_humidity = avarage_humidity / len(old_data["humidity"])

    for i in range(len(old_data["soil_moistures"])):
        avarage_soil_moisture += old_data["soil_moistures"][i]
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
