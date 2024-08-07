import pyaudio
import wave
import threading
import os
from pydub import AudioSegment

class AudioRecorder(threading.Thread):
    def __init__(self, format, channels, rate, chunk, filename, device_index=None):
        threading.Thread.__init__(self)
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.filename = filename
        self.frames = []
        self.is_recording = False
        self.device_index = device_index

    def run(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True,
                            frames_per_buffer=self.chunk, input_device_index=self.device_index)
        self.is_recording = True

        while self.is_recording:
            data = stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save as WAV first
        wav_filename = self.filename.replace('.mp3', '.wav')
        with wave.open(wav_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        # Convert WAV to MP3
        audio_segment = AudioSegment.from_wav(wav_filename)
        audio_segment.export(self.filename, format='mp3')
        os.remove(wav_filename)
        print(f"Audio saved as {self.filename}")

    def stop(self):
        self.is_recording = False

    @staticmethod
    def list_audio_devices():
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        devices = []
        for i in range(device_count):
            info = audio.get_device_info_by_index(i)
            devices.append((i, info.get('name')))
        audio.terminate()
        return devices
