import sys
import os
import datetime
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QComboBox, QAction, QMenu, QSystemTrayIcon, QStyle)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import pyaudio
from audio_recorder import AudioRecorder
from screen_recorder import ScreenRecorder

class CameraFeedThread(QThread):
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(self.camera_index)
        self.running = True
        self.frame = None
    
    def run(self):
        while self.running:
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
        self.capture.release()

    def stop(self):
        self.running = False

    def get_frame(self):
        return self.frame

class RecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Default settings
        self.audio_format = pyaudio.paInt16
        self.audio_channels = 2
        self.audio_rate = 44100
        self.audio_chunk = 1024
        self.screen_resolution = (1920, 1080)
        self.fps = 20

    def initUI(self):
        self.setWindowTitle('Screen and Audio Recorder')

        # Create actions for system tray
        self.show_action = QAction("Show", self)
        self.show_action.triggered.connect(self.restore_from_tray)
        
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(QApplication.instance().quit)
        
        # Create the system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon("icon.png"), self)
        tray_menu = QMenu()
        tray_menu.addAction(self.show_action)
        tray_menu.addAction(self.exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

        self.start_button = QPushButton('Start Recording', self)
        self.stop_button = QPushButton('Stop Recording', self)
        self.file_label = QLabel('Output files will be saved in the selected directory.', self)
        
        self.file_location_button = QPushButton('Select File Location', self)
        self.file_location_button.clicked.connect(self.select_file_location)

        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems(['1920x1080', '1280x720', '640x480'])
        
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        
        layout = QVBoxLayout()
        layout.addWidget(self.file_location_button)
        layout.addWidget(self.resolution_combo)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.file_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.resize(400, 300)
        
        # Set up keyboard shortcuts
        self.start_shortcut = QShortcut(QKeySequence('Ctrl+R'), self)
        self.start_shortcut.activated.connect(self.start_recording)
        
        self.stop_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.stop_shortcut.activated.connect(self.stop_recording)

        # Initialize Camera Feed Thread
        self.camera_thread = CameraFeedThread()
        self.camera_feed = None
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera_feed)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.restore_from_tray()  # Restore the app if the tray icon is clicked

    def select_file_location(self):
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", options=options)
        if folder:
            self.file_location = folder
            self.file_label.setText(f"Output files will be saved in: {folder}")
        else:
            self.file_label.setText("No folder selected.")

    def start_recording(self):
        if not hasattr(self, 'file_location'):
            self.file_location = os.getcwd()  # Default to current working directory
        
        resolution_str = self.resolution_combo.currentText()
        width, height = map(int, resolution_str.split('x'))
        resolution = (width, height)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_filename = os.path.join(self.file_location, f"output_{timestamp}.mp3")
        screen_filename = os.path.join(self.file_location, f"output_{timestamp}.mp4")
        combined_filename = os.path.join(self.file_location, f"combined_{timestamp}.mp4")
        
        self.audio_recorder = AudioRecorder(self.audio_format, self.audio_channels, self.audio_rate, self.audio_chunk, audio_filename)
        self.screen_recorder = ScreenRecorder(resolution, self.fps, screen_filename)
        
        self.audio_recorder.start()
        self.screen_recorder.start()
        
        # Start camera feed
        self.camera_thread.start()
        self.camera_timer.start(30)  # Update camera feed every 30 ms
        
        self.file_label.setText("Recording...")
        self.hide()  # Minimize the main window to the taskbar

        # Schedule combining the audio and video files after stopping
        self.combined_filename = combined_filename

    def stop_recording(self):
        try:
            self.audio_recorder.stop()
            self.screen_recorder.stop()
            self.camera_thread.stop()
            self.camera_timer.stop()
            self.file_label.setText("Recording stopped. Combining files...")

            # Combine audio and video
            self.combine_audio_video(self.audio_recorder.filename, self.screen_recorder.filename, self.combined_filename)
            
            self.file_label.setText(f"Files combined and saved as: {self.combined_filename}")
            self.restore_from_tray()  # Restore the main window after stopping
        except Exception as e:
            self.file_label.setText(f"Error: {e}")
            print(f"Error during stopping recording: {e}")

    def update_camera_feed(self):
        frame = self.camera_thread.get_frame()
        if frame is not None:
            # Resize and overlay camera feed
            frame = cv2.resize(frame, (160, 120))  # Resize to small rectangle
            # Use the OpenCV API to overlay the camera feed on the screen recording
            # Implement as needed based on the screen recording setup

    def combine_audio_video(self, audio_file, video_file, output_file):
        try:
            # Command to combine audio and video using ffmpeg
            command = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -strict experimental "{output_file}"'
            os.system(command)
            print(f"Combined file saved as: {output_file}")
        except Exception as e:
            print(f"Error during combining audio and video: {e}")

    def restore_from_tray(self):
        self.show()  # Show the main window
        self.activateWindow()  # Bring the window to the foreground
        self.raise_()  # Ensure the window is above other windows

def main():
    app = QApplication(sys.argv)
    ex = RecorderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
