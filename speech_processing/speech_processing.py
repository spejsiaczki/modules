import speech_recognition
from typing import List, Tuple
import argparse
import os


class SpeechProcessing:
    PROMPT = ""

    def __init__(self, input_path: str):
        self.input_path = input_path
        self.recognizer = None
        self.audio = None
        self.results = None
        self.recognizer = speech_recognition.Recognizer()

    def run(self) -> "SpeechProcessing":
        self._read_audio()
        self._transcribe()
        return self

    def _read_audio(self) -> str:
        with speech_recognition.AudioFile(self.input_path) as src:
            self.audio = self.recognizer.record(src)

    def _transcribe(self) -> str:
        try:
            self.results = self.recognizer.recognize_whisper(
                model="small",
                audio_data=self.audio,
                language="polish",
                word_timestamps=True,
                show_dict=True,
                prompt=SpeechProcessing.PROMPT,
            )
        except speech_recognition.UnknownValueError:
            print("could not understand audio")
        except speech_recognition.RequestError as e:
            print("error; {0}".format(e))

    def get_word_timestamps(self) -> List[Tuple[str, float, float]]:
        timestamps = []
        for segment in self.results["segments"]:
            for word in segment["words"]:
                text = word["word"]
                timestamps.append((text, word["start"], word["end"]))
        return timestamps

    def get_text(self) -> str:
        return "".join(self.get_words())

    def get_words(self) -> List[str]:
        words = []
        for segment in self.results["segments"]:
            for word in segment["words"]:
                words.append(word["word"])
        return words

    def get_pause_timestamps(self) -> List[Tuple[float, float]]:
        pauses = []
        word_timestamps = self.get_word_timestamps()
        for first, second in zip(word_timestamps, word_timestamps[1:]):
            t_start = first[2]
            t_end = second[1]
            if t_end - t_start > 0.01:
                pauses.append((t_start, t_end))
        return pauses


parser = argparse.ArgumentParser(description='speech_processing')
parser.add_argument('--input_audio', type=str, help='input video file path')
parser.add_argument('--output_text', type=str)
parser.add_argument('--output_word_timestamps', type=str)
parser.add_argument('--output_pause_timestamps', type=str)

if __name__ == "__main__":
    args = parser.parse_args()

    f_input = os.path.abspath(args.input_audio)
    f_output_text = os.path.abspath(args.output_text)
    f_output_word_timestamps = os.path.abspath(args.output_word_timestamps)
    f_output_pause_timestamps = os.path.abspath(args.output_pause_timestamps)

    speech_processing = SpeechProcessing(f_input).run()

    text = speech_processing.get_text()
    words = speech_processing.get_words()
    word_timestamps = speech_processing.get_word_timestamps()
    pause_timestamps = speech_processing.get_pause_timestamps()

    with open(f_output_text, "w") as f:
        f.write(str(text))
    with open(f_output_word_timestamps, "w") as f:
        for (word, start, end) in word_timestamps:
            f.write(f"{word}\t{float(start)}\t{float(end)}\n")
    with open(f_output_pause_timestamps, "w") as f:
        for (start, end) in pause_timestamps:
            f.write(f"{float(start)}\t{float(end)}\n")
