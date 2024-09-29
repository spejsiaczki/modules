import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import argparse
import json
import pyloudnorm as pyln
from loud_detect import detect_loudness_start



def analyze_file(path: str):
    # Initialize output variables
    repeating_sound: list[tuple[float, float]] = []
    long_silence: list[tuple[float, float]] = []

    # Load the .wav file
    sample_rate, data = wav.read(path)

    # If the audio is stereo, convert to mono
    if len(data.shape) > 1:
        data = data[:, 0]

    # Apply Short-Time Fourier Transform (STFT)
    frequencies, times, Zxx = signal.stft(
        data, fs=sample_rate, nperseg=1024, noverlap=512, window='hann')
    
    # Calculate the magnitude (absolute value) and convert to decibels (dB)
    magnitude = np.abs(Zxx)
    # Add a small constant to avoid log(0)
    magnitude_db = 20 * np.log10(magnitude + 1e-8)

    # Limit frequencies to a maximum of 8 kHz
    max_freq = 8000  # 8 kHz

    # Find the index where frequency is greater than 8 kHz
    freq_limit_idx = np.where(frequencies <= max_freq)[0]

    # Truncate the frequencies and spectrogram to only include frequencies <= 8 kHz
    frequencies = frequencies[freq_limit_idx]
    magnitude_db = magnitude_db[freq_limit_idx, :]

    REPEAT_MIN_TIME = 0.28
    DISTANCE_THRESH = 100
    FRAMES_THRESH = REPEAT_MIN_TIME * sample_rate / 512
    current_frames = 0
    repeated = False
    last_in_thresh = False
    repeat_start_time = 0.0
    repeat_last_time = 0.0

    for i in range(1, len(times)):
        if np.linalg.norm(magnitude_db[:, i] - magnitude_db[:, i-1]) < DISTANCE_THRESH:
            current_frames = min(current_frames+1, (FRAMES_THRESH*3)//2)
            last_in_thresh = True
        else:
            if not last_in_thresh:
                current_frames = max(current_frames-1, 0)
            last_in_thresh = False
        if current_frames > FRAMES_THRESH:
            repeated = True
            repeat_last_time = times[i]

        if current_frames < FRAMES_THRESH//2:
            if repeated:
                repeating_sound.append((repeat_start_time, repeat_last_time))
                repeated = False
                current_frames = 0
            repeat_start_time = 0.0
        elif repeat_start_time == 0.0:
            repeat_start_time = times[i]

    # detect long silence
    SILENCE_MIN_TIME = 0.33
    SILENCE_THRESH = 20
    SILENCE_FRAMES_THRESH = SILENCE_MIN_TIME * sample_rate / 512
    FINAL_DEADZONE = 2.0
    magnitude_db[:, np.max(magnitude_db, axis=0) < SILENCE_THRESH] = -60
    silence_frames = 0
    silence_repeat = False
    silence_start_time = 0.0
    silence_last_time = 0.0

    for i in range(1, len(times)):
        if magnitude_db[:, i].max() < -50:
            silence_frames = min(
                silence_frames+1, (SILENCE_FRAMES_THRESH*3)//2)
        else:
            silence_frames = max(silence_frames-1, 0)

        if silence_frames > SILENCE_FRAMES_THRESH:
            if times[-1] - times[i] < FINAL_DEADZONE:
                break
            silence_repeat = True
            silence_last_time = times[i]
        if silence_frames < SILENCE_FRAMES_THRESH//2:
            if silence_repeat:
                long_silence.append((silence_start_time, silence_last_time))
                silence_repeat = False
                silence_frames = 0
            silence_start_time = 0.0
        elif silence_start_time == 0.0:
            silence_start_time = times[i]

    loud_moments = detect_loudness_start(data, sample_rate)
    return repeating_sound, long_silence, loud_moments


def main(args):
    repeating_sound, long_silence, loud_moments = analyze_file(args.input)
    with open(args.output, 'w') as f:
        json.dump({
            'repeating_sound': repeating_sound,
            'long_silence': long_silence,
            'loud_moments': loud_moments
        }, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input audio file path')
    parser.add_argument('--output', type=str, help='Path to output file')
    parsed_args = parser.parse_args()
    main(parsed_args)
