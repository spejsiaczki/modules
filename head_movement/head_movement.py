import cv2
import numpy as np
import mediapipe as mp
import json
import argparse
import os


parser = argparse.ArgumentParser(description='Trim start splash screen from video')
parser.add_argument('--input', type=str, help='input video file path')
parser.add_argument('--output', type=str, help='output json file path')



def main(video_path:str, json_path:str):
    input_video = cv2.VideoCapture(video_path)
    frame_rate = input_video.get(cv2.CAP_PROP_FPS)
    frame_idx = 0

    diff_values = []
    diff_timestamps = []
    timestamps = []

    with mp.solutions.face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    
        while input_video.isOpened():
            
            ret, frame = input_video.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    left_cheek = np.array([face_landmarks.landmark[234].x, face_landmarks.landmark[234].y])
                    right_cheek = np.array([face_landmarks.landmark[454].x, face_landmarks.landmark[454].y])
                    diff = left_cheek[0] - right_cheek[0]
                    
                    if frame_idx%frame_rate==0:
                        diff_values.append(diff)
                        diff_timestamps.append(frame_idx/frame_rate)

            frame_idx+=1
            

    input_video.release()
    cv2.destroyAllWindows()
    is_first = True
    
    for idx, elem in enumerate(diff_values):
        if is_first:
            first_elem = 0.0
            is_first = False

        if abs(elem-first_elem)>0.1:
            timestamps.append(diff_timestamps[idx]+5)
            first_elem = elem
    
    data = {'head_movement':timestamps}
    with open(json_path, 'w') as file:
        json.dump(data, file)


if __name__=="__main__":
    args = parser.parse_args()
    f_in = os.path.abspath(args.input)
    f_out = os.path.abspath(args.output)
    main(f_in, f_out)