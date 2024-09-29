import easyocr
import cv2
from cv2.typing import MatLike
import nltk
import argparse
import os


class OCR:
    PROCESSING_WIDTH = 400
    FRAME_STEP = 0.1  # seconds between OCR frames
    ABS_DIFF_THRESHOLD = 3
    LEVENSHTEIN_THRESHOLD = 0.2

    def __init__(self):
        self.reader = easyocr.Reader(["pl"])

    def ocr_img(self, img: MatLike) -> str:
        width, height = img.shape[1], img.shape[0]
        l = round(width * 0.24)
        t = round(height * 0.82)
        r = round(width * 0.76)
        b = round(height * 0.99)
        img_cropped = img[t:b, l:r]
        img_cropped = cv2.resize(
            img_cropped,
            (
                OCR.PROCESSING_WIDTH,
                round(
                    OCR.PROCESSING_WIDTH *
                    img_cropped.shape[0] / img_cropped.shape[1]
                ),
            ),
        )

        result = self.reader.readtext(img_cropped)

        content = ""
        for bbox, text, prob in result:
            if prob > 0.2:
                content += text + " "

        return content.strip()

    def ocr(self, file_path: str) -> dict[float, str]:
        cap = cv2.VideoCapture(file_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        frame_step = round(frame_rate * OCR.FRAME_STEP)
        frame_number = 0

        last_frame = None
        last_content = ""
        subtitles: dict[float, str] = {}
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_number % frame_step == 0:
                # Check if frame has changed significantly
                if last_frame is not None:
                    diff = cv2.absdiff(frame, last_frame)
                    if diff.mean() < OCR.ABS_DIFF_THRESHOLD:
                        frame_number += 1
                        continue

                last_frame = frame.copy()

                content = self.ocr_img(frame)

                if len(content) > 0:
                    if (
                        nltk.edit_distance(content, last_content)
                        / max(len(content), len(last_content))
                        > OCR.LEVENSHTEIN_THRESHOLD
                    ):
                        time = frame_number / frame_rate
                        last_content = content
                        subtitles[time] = content

            frame_number += 1

        cap.release()

        return subtitles


parser = argparse.ArgumentParser(
    description='OCR')
parser.add_argument('--input', type=str, help='input video file path')
parser.add_argument('--output_ocr', type=str, help='output text file path')

if __name__ == "__main__":
    args = parser.parse_args()

    f_in = os.path.abspath(args.input)
    f_out = os.path.abspath(args.output_ocr)

    ocr = OCR()
    subtitles = ocr.ocr(f_in)
    ocr_text = " ".join(subtitles.values())

    with open(f_out, "w") as f:
        f.write(ocr_text)
