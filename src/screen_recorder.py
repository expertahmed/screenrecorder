import cv2
import numpy as np
from PIL import ImageGrab
import threading
import time

class ScreenRecorder(threading.Thread):
    def __init__(self, resolution, fps, filename):
        threading.Thread.__init__(self)
        self.resolution = resolution
        self.fps = fps
        self.filename = filename
        self.is_recording = False
        self.out = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, self.get_screen_resolution())

    def get_screen_resolution(self):
        screen = ImageGrab.grab()
        return screen.size

    def run(self):
        self.is_recording = True
        screen_resolution = self.get_screen_resolution()
        print(f"Screen recording started with resolution {screen_resolution}...")

        try:
            while self.is_recording:
                start_time = time.time()
                
                img = ImageGrab.grab(bbox=(0, 0, screen_resolution[0], screen_resolution[1]))
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                self.out.write(frame)
                print("Frame captured")  # Debug print to check frame capturing

                elapsed_time = time.time() - start_time
                sleep_time = (1.0 / self.fps) - elapsed_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
        except Exception as e:
            print(f"Error during screen recording: {e}")
        finally:
            self.out.release()
            print(f"Screen recording saved as {self.filename}")

    def stop(self):
        self.is_recording = False
        print("Stopping screen recording...")

# Ensure ImageGrab works in the current environment
if not hasattr(ImageGrab, 'grab'):
    raise ImportError("PIL.ImageGrab module is not available in this environment.")
