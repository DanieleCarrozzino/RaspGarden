import picamera
import time
import datetime

class PiCamera():

    def __init__(self) -> None:
        self.photo_extension = '.jpg'
        self.video_extension = '.h264'
        pass

    def capture(self, photo_path):
        with picamera.PiCamera() as camera:
            # Give the camera time to warm up
            time.sleep(2)

            # Capture a photo
            current_time = datetime.datetime.now()
            name = current_time.strftime("%Y-%m-%d_%H-%M-%S") + self.photo_extension 

            print(">>> Final path destination")
            print(photo_path + name)
            camera.capture(photo_path + name)

        print(f">>> Return value {name}")
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