import sys
import os
import datetime
import pyaudio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QComboBox, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from audio_recorder import AudioRecorder
from screen_recorder import ScreenRecorder

class RecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_recording = False  # Track recording state

    def initUI(self):
        self.setWindowTitle('Screen and Audio Recorder')
        self.setGeometry(100, 100, 800, 600)

        self.start_button = QPushButton('Start Recording', self)
        self.stop_button = QPushButton('Stop Recording', self)
        self.file_label = QLabel('Output files will be saved in the selected directory.', self)

        self.file_location_button = QPushButton('Select File Location', self)
        self.file_location_button.clicked.connect(self.select_file_location)

        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems(['1920x1080', '1280x720', '640x480'])

        self.audio_device_combo = QComboBox(self)
        self.audio_device_combo.addItems(self.get_audio_devices())

        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.file_location_button)
        layout.addWidget(QLabel('Select Screen Resolution:', self))
        layout.addWidget(self.resolution_combo)
        layout.addWidget(QLabel('Select Audio Input Device:', self))
        layout.addWidget(self.audio_device_combo)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.file_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add keyboard shortcuts
        self.start_shortcut = QShortcut(QKeySequence('Ctrl+R'), self)
        self.start_shortcut.activated.connect(self.start_recording)

        self.stop_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        self.stop_shortcut.activated.connect(self.stop_recording)

    def get_audio_devices(self):
        devices = AudioRecorder.list_audio_devices()
        return [f"{name} (Index {index})" for index, name in devices]

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
            self.file_location = os.getcwd()

        resolution_str = self.resolution_combo.currentText()
        width, height = map(int, resolution_str.split('x'))
        resolution = (width, height)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.audio_filename = os.path.join(self.file_location, f"output_{timestamp}.mp3")
        self.screen_filename = os.path.join(self.file_location, f"output_{timestamp}.mp4")
        self.combined_filename = os.path.join(self.file_location, f"combined_{timestamp}.mp4")

        audio_device_index = self.audio_device_combo.currentIndex()

        self.audio_recorder = AudioRecorder(pyaudio.paInt16, 2, 44100, 1024, self.audio_filename, device_index=audio_device_index)
        self.screen_recorder = ScreenRecorder(resolution, 20, self.screen_filename)

        self.audio_recorder.start()
        self.screen_recorder.start()

        self.file_label.setText("Recording...")
        self.is_recording = True  # Set recording state to True

    def stop_recording(self):
        if self.is_recording:  # Check if recording is in progress
            self.audio_recorder.stop()
            self.screen_recorder.stop()
            self.audio_recorder.join()
            self.screen_recorder.join()
            self.file_label.setText("Recording stopped. Combining files...")

            self.combine_audio_video(self.audio_filename, self.screen_filename, self.combined_filename)

            # Remove temporary files
            self.remove_temp_files(self.audio_filename, self.screen_filename)

            self.file_label.setText(f"Files combined and saved as: {self.combined_filename}")
            self.is_recording = False  # Reset recording state
        else:
            self.file_label.setText("No recording in progress.")

    def combine_audio_video(self, audio_file, video_file, output_file):
        command = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -strict experimental "{output_file}"'
        result = os.system(command)
        if result != 0:
            print(f"FFmpeg command failed with result code {result}")
            QMessageBox.critical(self, "Error", f"Combining audio and video failed with code {result}")
        else:
            print(f"Combined file saved as {output_file}")

    def remove_temp_files(self, *files):
        for file in files:
            try:
                os.remove(file)
                print(f"Removed temporary file: {file}")
            except Exception as e:
                print(f"Error removing temporary file {file}: {e}")

def main():
    app = QApplication(sys.argv)
    ex = RecorderApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
