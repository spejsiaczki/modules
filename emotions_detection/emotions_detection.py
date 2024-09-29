import cv2
from fer import FER
import numpy as np
import json
import argparse
import os


parser = argparse.ArgumentParser(
    description='Trim start splash screen from video')
parser.add_argument('--input', type=str, help='input video file path')
parser.add_argument('--output', type=str, help='output json file path')


def main(file_path: str, json_path: str):
    input_video = cv2.VideoCapture(file_path)
    frame_rate = input_video.get(cv2.CAP_PROP_FPS)
    frame_idx = 0

    emotion_detector = FER()
    emotions_dict = {'angry': [], 'disgust': [], 'fear': [],
                     'happy': [], 'sad': [], 'surprise': [], 'neutral': []}
    emotions_labels = list(emotions_dict.keys())

    previous_value = 0
    found_zboczes = 0
    max_emotions_dict = {}

    while input_video.isOpened():
        emotions_in_segment = []
        emotion_history = []
        success, single_frame = input_video.read()
        if not success:
            break
        result = emotion_detector.detect_emotions(single_frame)
        if not result:
            continue
        emotions = result[0]['emotions']
        for emotion, percent in emotions.items():
            if frame_idx > 0:
                previous_value = emotions_dict[str(emotion)][frame_idx-1]
            diff = percent - previous_value
            if diff > 0.4 and emotion != 'neutral':
                found_zboczes += 1
                timestamp = frame_idx/frame_rate
            emotions_dict[str(emotion)].append(percent)
            emotions_in_segment = emotions_dict

        if frame_idx % frame_rate == 0:
            for key, value in emotions_in_segment.items():
                mean_emotion_values = np.mean(value)
                emotion_history.append(mean_emotion_values)
            max_emotion = emotions_labels[np.argmax(emotion_history)]
            max_emotions_dict[frame_idx/frame_rate] = max_emotion

        frame_idx += 1

    input_video.release()
    cv2.destroyAllWindows()
    if found_zboczes <= 3:
        mimika_timestamp = None
    else:
        mimika_timestamp = timestamp

    data = {'mimika_timestamp': mimika_timestamp,
            'emotions': max_emotions_dict}
    with open(json_path, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    args = parser.parse_args()

    f_in = os.path.abspath(args.input)
    f_out = os.path.abspath(args.output)

    main(f_in, f_out)

    # print(found_zboczes)
    # if found_zboczes>3:
    #     print("Znaleziono błąd: mimika")
    # print("Emocje:")
    # for keys, values in max_emotions_dict.items():
    #     if int(keys)==0:
    #         print(f"Sekunda {keys}, emocja {values}")
    #         prev_emotion = values
    #     else:
    #         if values!=prev_emotion:
    #             print(f"Sekunda {keys}, emocja {values}")
    #             prev_emotion = values
    # # unique_emotions = set(max_emotions_dict.values())
    # # print(unique_emotions)

    # # print(get_filename("videos/HY_2024_film_08.mp4"))
    # # TODO
