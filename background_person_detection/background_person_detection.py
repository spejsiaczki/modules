import cv2
import numpy as np
import json
import argparse
import os


parser = argparse.ArgumentParser(description='Trim start splash screen from video')
parser.add_argument('--input', type=str, help='input video file path')
parser.add_argument('--output', type=str, help='output json file path')


def check_consecutive_diff(lst, count=4, max_diff=1.0):
    matching_subsequences = []
    for i in range(len(lst) - count + 1):
        sub_list = lst[i:i + count]
        
        if all(abs(sub_list[j] - sub_list[j+1]) <= max_diff for j in range(count - 1)):
            matching_subsequences.append(sub_list)

    return matching_subsequences


def get_middle_value(sub_list):
    length = len(sub_list)
    mid = length // 2
    if length % 2 != 0:
        return sub_list[mid]
    else:
        return (sub_list[mid - 1] + sub_list[mid]) / 2


def main(video_path:str, json_path:str):
    input_video = cv2.VideoCapture(video_path)
    frame_rate = input_video.get(cv2.CAP_PROP_FPS)
    frame_idx = 0

    timestamps = []

    back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=True)
    found_woman = []
    while input_video.isOpened():
        
        ret, frame = input_video.read()
        if not ret:
            break

        fg_mask = back_sub.apply(frame)

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) > 50000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if frame_idx/frame_rate > 10 and frame_idx%frame_rate==0:
                    found_woman.append(frame_idx/frame_rate)

        frame = cv2.resize(frame,(600,400))
        frame_idx+=1

    input_video.release()
    cv2.destroyAllWindows()

    matching_subsequences = check_consecutive_diff(found_woman)
    for subsequence in matching_subsequences:
        timestamps.append(get_middle_value(subsequence))
    data = {"background_person":timestamps}
    with open(json_path, 'w') as file:
        json.dump(data, file)

if __name__=="__main__":
    args = parser.parse_args()
    f_in = os.path.abspath(args.input)
    f_out = os.path.abspath(args.output)
    main(f_in, f_out)
