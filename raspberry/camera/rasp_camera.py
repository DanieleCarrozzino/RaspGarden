import picamera
import time
import datetime
import os

class PiCamera():

    def __init__(self) -> None:
        self.photo_extension = '.png'
        self.video_extension = '.h264'
        pass

    def capture(self, photo_path):
        os.makedirs(photo_path, exist_ok=True)
        with picamera.PiCamera() as camera:
            # Give the camera time to warm up
            time.sleep(2)

            # Capture a photo
            name = "1" + self.photo_extension 
            camera.capture(photo_path + name)
        return name

    def video_capture(self, video_path):
        with picamera.PiCamera() as camera:
            # Give the camera time to warm up
            time.sleep(2)

            # Capture a video
            camera.start_recording(video_path + self.video_extension)  # Start recording
            camera.wait_recording(10)  # Record for 10 seconds
            camera.stop_recording()
        pass