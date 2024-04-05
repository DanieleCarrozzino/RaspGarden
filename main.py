print("Firebase")
from firebase import storage, firestore, messaging, database, main_firebase
print("Configuration")
from configuration import reader_conf, qr_creator
print("Models")
#from models import plants_analyzer as analyzer
print("Sensors")
from raspberry.sensors import DHT11
from raspberry.sensors import ADS1115
from raspberry.camera import rasp_camera as Camera
print("Vidoe editing")
from video import editor as VideoEditor
print("Others")
import time
import shutil
import datetime

# Const
MAX_VALUES = 30

# Init class
sensor_temperature  = DHT11.DHTClass()
sensor_moisture     = ADS1115.ADS1115Class()
camera = Camera.PiCamera()
reader = reader_conf.ConfReader()
editor = VideoEditor.Editor()
# Firebase
firebase_database   = database.Database()
storage_manager     = storage.ImagesStorage()

# Old data to analyze
old_data = {
    "temperatures": list(),
    "humidity": list(),
    "soil_moistures": list()
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
        serializable_data["temperatures"]   = serializable_data["temperatures"]
        serializable_data["humidity"]       = serializable_data["humidity"]
        serializable_data["soil_moistures"] = serializable_data["soil_moistures"]
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

    # Define a maximum size for the lists
    # remove the first element if the list
    # is more than MAX_VALUES length
    if len(old_data["temperatures"]) > MAX_VALUES:
        old_data["temperatures"].pop(0)

    if len(old_data["humidity"]) > MAX_VALUES:
        old_data["humidity"].pop(0)

    if len(old_data["soil_moistures"]) > MAX_VALUES:
        old_data["soil_moistures"].pop(0)

    old_data["temperatures"].append(dict['temperature'])
    old_data["humidity"].append(dict['humidity'])
    old_data["soil_moistures"].append(dict['moisture'])

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
        avarage_soil_moisture += old_data["soil_moistures"][i][0]
    avarage_soil_moisture = avarage_soil_moisture / len(old_data["soil_moistures"])
    
    print(old_data)
    print(avarage_humidity)
    print(avarage_soil_moisture)
    print(avarage_temperature)


def watering(dict):

    # Get personal data and thresholds
    personal = firebase_database.get_personal_data()
    if personal['min_watering'] > 0 and personal['max_watering'] < 100: # TODO dict['watering']:
        print("WATER")
    else:
        print("NO WATER")
    pass


#
# SAVE PICTURE
#
# save the resulting picture inside 
# the storage of firebase
# into the folder of this raspberry code
#
def save_picture(file_path, file_name):
    print(">> File name of the new picture")
    print(file_name)
    print(">> File path of the picture")
    print(file_path)
    storage_manager.save_image_from_file_name(file_path, file_name)
    pass

#
# CREATE TIMELAPS
# create the new video with the new image
# and then caoncat the video with the main
# video
#
def create_timelaps(images_path):
    editor.create_video(images_path)
    return editor.concat_video()


# Take picture
# take a picture after a user
# explicit request
def take_picture_on_request(data):
    print("> Take picture")
    picture_path = "./instant_pictures/"
    name = camera.capture(picture_path)

    print("> Save photo")
    current_time = datetime.datetime.now()
    new_name = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    save_picture(picture_path + name, "InstantPictures/" + new_name + name)
    pass

def observe_changes():
    firebase_database.observe_specific_data("camera", take_picture_on_request)


def create_qr():
    text = "rasp_code:rasp_test_code1"
    path = qr_creator.create_and_save_QR(text)
    save_picture(path, "QR/qr.png")
    pass

def check_hour_to_take_a_photo():
    # Get the current date and time
    current_time = datetime.now()

    # Get the hour from the current time
    current_hour = current_time.hour

    # Check if the hour is between 8 PM (20) and 6 AM (6)
    if 20 <= current_hour or current_hour < 6:
        return False
    return True

def main():

    print("|***********************|")
    print('| Start watching garden |')
    print("|***********************|")
    print("| - Daniele carrozzino  |")
    print("|_______________________|")

    print("\n\nCreate qr to provide something")
    create_qr()
    print("\n\n")

    print("Observe raspberry changes")
    print("- Camera request")
    observe_changes()
    print("-----------------")

    print("> Starting loop")
    while True:

        print("> Get sensors result")
        # All sensors result
        dict_result = get_new_data()

        print("> Processing data")
        # Process all data
        processing_data(dict_result)

        print("> Watering the plants if needed")
        # Check needed
        watering(dict_result)

        print("> Update gardens")
        # Get gardens to update
        gardens = reader.get_gardens()
        update_gardens(gardens)

        if check_hour_to_take_a_photo():
            print("> Get picture")
            picture_path = "./pictures/"
            name = camera.capture(picture_path)

            print("> Save photo")
            # OPEN in RELEASE
            # Create a new different name
            current_time = datetime.datetime.now()
            new_name = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            save_picture(picture_path + name, "Pictures/" + new_name + name)

            print("> Create timelaps")
            output_path_timelaps = create_timelaps(picture_path)

            print("> Save timelaps")
            save_picture(output_path_timelaps, "Timelaps/" + "timelaps.mp4")

            print("> Analyze the result")
            # Analyze
            # model = analyzer.PlantAnalyzer()
            # model.getWebcamResult()

            print("> Remove the local picture")
            shutil.rmtree(picture_path)

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
