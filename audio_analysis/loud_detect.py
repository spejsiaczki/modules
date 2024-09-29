import numpy as np
import pyloudnorm as pyln
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

def tests():
    for i in range(1, 21):
        # Load the .wav file
        rate, data = wav.read(f'audios/audio{i}.wav')

        # If stereo, convert to mono
        if len(data.shape) > 1:
            data = data[:, 0]

        data = data.astype(np.float32) / np.max(np.abs(data.astype(np.float32)))

        # Create a loudness meter object based on the sample rate
        meter = pyln.Meter(rate)
        
        total_loudness=meter.integrated_loudness(data)
        
        data = pyln.normalize.loudness(data, total_loudness, -24.0)

        SEGMENT_IN_SECONDS = 0.4
        # Define segment length (e.g., 1 second)
        segment_length = int(rate * SEGMENT_IN_SECONDS)  # 1 second of audio


        print(f"Total loudness: {total_loudness} LUFS")

        # Calculate loudness for each segment
        loudness_values = []
        for i in range(0, len(data), segment_length):
            segment = data[i:i+segment_length]
            # print(len(segment), segment_length)
            if len(segment) < segment_length:
                break
            loudness = meter.integrated_loudness(segment)
            print(f"Time: {i/rate} seconds, Loudness: {loudness} LUFS")
            loudness_values.append(loudness)
            
        # Detect sudden loudness changes by calculating the difference between consecutive segments
        loudness_diff = np.diff(loudness_values)

        DIFF_THRESHOLD = 9.0
        change_time = []

        for i in range(len(loudness_diff)):
            print(f"Time: {i*SEGMENT_IN_SECONDS} seconds, Loudness diff: {loudness_diff[i]} LUFS")
            if loudness_diff[i] > DIFF_THRESHOLD and loudness_values[i+1] > total_loudness + DIFF_THRESHOLD:
                
                change_time.append(i * SEGMENT_IN_SECONDS)
                
        print(change_time)
        input()
    
    
def detect_loudness_start(data, rate):
    
    data = data.astype(np.float32) / np.max(np.abs(data.astype(np.float32)))
    
    # Create a loudness meter object based on the sample rate
    meter = pyln.Meter(rate)
    
    total_loudness=meter.integrated_loudness(data)
    
    data = pyln.normalize.loudness(data, total_loudness, -24.0)

    SEGMENT_IN_SECONDS = 0.4
    # Define segment length (e.g., 1 second)
    segment_length = int(rate * SEGMENT_IN_SECONDS)  # 1 second of audio

    # Calculate loudness for each segment
    loudness_values = []
    for i in range(0, len(data), segment_length):
        segment = data[i:i+segment_length]
        if len(segment) < segment_length:
            break
        loudness = meter.integrated_loudness(segment)
        loudness_values.append(loudness)
        
    loudness_diff = np.diff(loudness_values)

    DIFF_THRESHOLD = 9.0
    loud_moments = []

    for i in range(len(loudness_diff)):
        if loudness_diff[i] > DIFF_THRESHOLD and loudness_values[i+1] > total_loudness + DIFF_THRESHOLD:
            
            loud_moments.append(i * SEGMENT_IN_SECONDS)
            
    return loud_moments
