# Built-in modules
import os
import time

# External libraries
import pyaudio
import wave

# Custom module
from Util.DataClass import DataClass


class Soundfile(DataClass):
    def __init__(self):
        super().__init__()  # Call the base class __init__ method

        # Constants for audio settings
        self.end_time = self.end_time
        self.format = pyaudio.paInt16
        self.channels = 2
        self.sample_rate = 44100  # Normal wave length for normal sound quality
        self.chunk = 1024
        self.frames = []

        # Generate a unique filename for the sub-folders
        self.current_time = time.strftime("%Y%m%d-%H%M%S")

        # Folder path and filename
        self.folder_path = self.folder_path_soundfile
        self.output_file_name = f"Soundfile{self.current_time}.wav"

    def audio_recording(self):
        p = pyaudio.PyAudio()

        stream = p.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        while time.time() < self.end_time:
            try:
                data = stream.read(self.chunk)
                self.frames.append(data)

            except IOError as e:
                print(f"Audio recording error: {e}")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save captured audio to the file path
        file_path = os.path.join(self.folder_path, self.output_file_name)
        with wave.open(file_path, 'wb') as f:
            f.setnchannels(self.channels)
            f.setsampwidth(p.get_sample_size(self.format))
            f.setframerate(self.sample_rate)
            f.writeframes(b''.join(self.frames))
