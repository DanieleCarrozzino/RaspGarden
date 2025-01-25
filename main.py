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
print("Video editing")
from video import editor as VideoEditor
print("Utility")
from utility import utility
from utility import Logger
print("Others")
import time
import shutil
import datetime
import threading
import socket

# Const
MAX_VALUES = 30

# Init class
sensor_temperature  = DHT11.DHTClass()
sensor_moisture     = ADS1115.ADS1115Class()
camera = Camera.PiCamera()
reader = reader_conf.ConfReader()
editor = VideoEditor.Editor()
# Firebase
firebase_database           = database.Database()
firebase_static_database    = firestore.FirebaseDatabase()
storage_manager             = storage.ImagesStorage()
message_manager             = messaging.Messaging()
#Utility
logger = Logger.logger()

# Test and debug
loop_test = 0

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

# Status garden
activated = True


#
# Update gardens
#
# update the real time database
# with all the processing data 
# get during this loop
#
def update_gardens(gardens):
    for garden in gardens:
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
# Get tokens
# get the users' token from firebase 
# by their uid
#
def get_tokens_from_users(users) -> list:
    tokens = list()
    for user in users:
        data = firebase_static_database.get(user, "firebase_token")
        tokens.append(data["token"])
        logger.d(data["token"])
    return tokens


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
    logger.d(temperature)
    sensor_results['temperature']   = temperature
    sensor_results['humidity']      = humidity

    # Soil moisture
    values = sensor_moisture.read()
    logger.d(values)
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
def save_picture(file_path, file_name, folder = "Pictures"):
    storage_manager.save_image_from_file_name(file_path, file_name, folder)
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
    logger.d("Main::main::Take picture as requested")
    logger.d(data)
    try:
        # Capture image
        picture_path    = "./instant_pictures/"
        name            = camera.capture(picture_path)

        # Save image on firebase
        current_time    = datetime.datetime.now()
        new_name        = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        save_picture(picture_path + name, "InstantPictures/" + new_name + name, "InstantPictures")
    except Exception as e:
        logger.d("Take picture EXCEPTION")
        logger.d(e)

def change_status_garden(data):
    logger.d(data)
    global activated
    activated = data

def watering_on_request(data):
    logger.d(f"Main::watering_on_request::{data}")

def observe_changes(param):
    if param == "camera":
        firebase_database.observe_specific_data(param, take_picture_on_request)
    elif param == "activated": 
        firebase_database.observe_specific_data(param, change_status_garden)
    else:
        firebase_database.observe_specific_data("notify_irrigation", watering_on_request)

    # Keep the thread alive
    while activated:
        time.sleep(100)

def create_qr():
    text = "rasp_code:rasp_test_code1"
    path = qr_creator.create_and_save_QR(text)
    save_picture(path, "QR/qr.png")
    pass

def save_ip_adress():
    logger.d("Main::save_ip_address::get the ip form the socket library")
    try:
        # Create a socket to check the IP address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        logger.d(f"Main::save_ip_address::Your Raspberry Pi's IP address is: {ip_address}")

        # Save data
        data = {"ip" : ""}
        data["ip"] = ip_address
        firebase_database.update_personal_node()
    except socket.error as e:
        logger.d(f"Main::save_ip_address::Unable to get IP address: {e}")
    pass

#
# If the actual hour is over the sunset
# or before the dawn I don't want to save
# any picture, because I don't have any 
# light
def check_hour_to_take_a_photo() -> bool:
    current_time = datetime.datetime.now()
    current_hour = current_time.hour

    # Check if the hour is between 8 PM (20) and 6 AM (6)
    # TODO choose a better method to decide if the sun is set or not
    if 20 <= current_hour or current_hour < 7:
        return False
    return True


def start_observer_thread(param) -> threading.Thread:
    thread = threading.Thread(target=observe_changes, args=(param,), name="Observe async thread for async request")
    thread.daemon = True
    thread.start()
    return thread


def main():
    
    utility.printHeading()

    # Create personal qr code to 
    # pair and connect the devices 
    # with this raspberry
    create_qr()

    # Save ip address of this 
    # raspberry inside the 
    # storage of firebase
    # to be able to see any 
    # changes from the console
    save_ip_adress()

    # You can take a picture of the garden
    # every time you want, and it must be async 
    # from the rest of the code, that is slept
    # most of the time
    # Create daemon thread
    thread_camera = start_observer_thread("camera")
    thread_active = start_observer_thread("activated")
    thread_watery = start_observer_thread("water")

    logger.d("Main::main::starting loop")
    loop_count = 0

    while True:

        #
        # Restart the observer threads if they are dead
        #
        if not thread_camera.is_alive():
            thread_camera = start_observer_thread("camera")
        if not thread_active.is_alive():
            thread_active = start_observer_thread("activated")
        if not thread_watery.is_alive():
            thread_watery = start_observer_thread("water")

        #
        # GARDEN UPDATE 
        # I only update the garden every 30 minutes
        #
        if (loop_count >= 11 or loop_count == 0) and activated:
            # Restart the count looper
            loop_count = 1

            logger.d("Main::main::first step of teh loop, getting sensors data")
            # All sensors result
            dict_result = get_new_data()

            logger.d("Main::main::Processing data")
            # Process all data
            processing_data(dict_result)

            logger.d("Main::main::Watering the plants if needed")
            # Check needed
            watering(dict_result)

            logger.d("Main::main::Update gardens")
            # Get gardens to update
            gardens = reader.get_gardens()
            update_gardens(gardens)

            logger.d("Main::main::Print tokens")
            # Get the users' token form firebase
            users   = reader.get_users()
            tokens  = get_tokens_from_users(users)
            
            logger.d("Main::main::Send push notifications")
            # message_manager.sendMessage("Nuovi dati sul giardino", "PUZZETTA", tokens)

        #
        # TIMELAPSE UPDATE
        # I take a picture of the garden every 5 minutes
        #
        if check_hour_to_take_a_photo():
            logger.d("Main::main::Get picture")
            picture_path = "./pictures/"
            name = camera.capture(picture_path)

            logger.d("Main::main::Save photo")
            # OPEN in RELEASE
            # Create a new different name
            current_time = datetime.datetime.now()
            new_name = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            save_picture(picture_path + name, "Pictures/" + new_name + name, "Pictures")

            logger.d("Main::main::Create timelaps")
            output_path_timelaps = create_timelaps(picture_path)

            logger.d("Main::main::Save timelaps")
            save_picture(output_path_timelaps, "Timelaps/" + "timelaps.mp4")

            logger.d("Main::main::Analyze the result")
            # Analyze
            # model = analyzer.PlantAnalyzer()
            # model.getWebcamResult()

            logger.d("Main::main::Remove the local picture")
            shutil.rmtree(picture_path)

        # Pause and restart
        loop_count += 1
        logger.d("Main::main::Sleep to restart")
        time.sleep(300)

if __name__ == "__main__":
    main()

#######################
# Save into Firestore #
#######################
# firestore_manager = firestore.FirebaseDatabse()
# data = {
#     'name': 'John Doe',
#     'age': 30,
#     'email': 'johndoe@example.com'
# }
# firestore_manager.save(data, 'user', 'user1')
# firestore_manager.get('user', 'user1')


##############################
# Save images into storage   #
##############################
# storage_manager = storage.ImagesStorage()
# storage_manager.save_image('C:\\Users\\em-hp2\\Desktop\\Works\\Python\\FirebaseProject\\README.md', 'test/test.md')


#####################
# Send notification #
#####################
# message_manager = messaging.Messaging()
# message_manager.sendMessage('title_test', 'body_test')
