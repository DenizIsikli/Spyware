# Libraries
import cv2
from PIL import ImageGrab
import sounddevice as sd
import wavfile as wf
import os
import numpy as np
import time

def webCamera():
    cap = VideoCapture(0)
    frame, image = cap.read()
    if frame:
        imshow('Webcam', image)
        imwrite('WebCamera.png', image)
        waitKey(1)
        destroyWindow('Webcam')

def screenShots():
    folder_path = r"C:\Users\deniz\Skrivebord\TestMappe\Screenshots"

    image = ImageGrab.grab()

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save captured audio to the file path
    file_path = os.path.join(folder_path, "Screenshot.png")
    image.save(file_path)

def microphone():
    folder_path = r"C:\Users\deniz\Skrivebord\TestMappe\Soundfiles"

    #Constants for audio settings
    SAMPLE_RATE = 44100
    DURATION = 300 #Duration in seconds
    OUTPUT_FILE = "caputured_audio.wav"

    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = 1, callback = audio_callback)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    sd.wait()

    print("Finished capturing audio.\n")

    # Save captured audio to the file path
    file_path = os.path.join(folder_path, "Soundfile.wav")
    wf.write(file_path, SAMPLE_RATE, np.int16(audio_data * 32767))


    if __name__ == '__main__':
        webCamera()
        screenShots()
        microphone()

