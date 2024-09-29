import argparse
import json

parser = argparse.ArgumentParser(description='merger')

parser.add_argument('--input_comparison', type=str)
parser.add_argument('--input_sp', type=str)
parser.add_argument('--input_ocr', type=str)
parser.add_argument('--input_word_timestamps', type=str)
parser.add_argument('--input_pause_timestamps', type=str)
parser.add_argument('--input_background_person_detection', type=str)
parser.add_argument('--input_emotions_detection', type=str)
parser.add_argument('--input_gunning_fog', type=str)
parser.add_argument('--input_language_detection', type=str)
parser.add_argument('--input_audio_analysis', type=str)

parser.add_argument('--output_merged', type=str)


def merge_data():
    args = parser.parse_args()

    with open(args.input_comparison, "r") as f:
        comparison = f.read() \
            .replace(",", "") \
            .replace("(", "") \
            .replace(")", "") \
            .split()
        comparison = {"value": comparison[0], "description": comparison[2]}

    with open(args.input_sp, "r") as f:
        sp = f.read()
    with open(args.input_ocr, "r") as f:
        ocr = f.read()
    with open(args.input_word_timestamps, "r") as f:
        words = []
        for line in f.readlines():
            w, s, e = line.split()
            s = float(s)
            e = float(e)
            words.append({
                "word": w,
                "start": s,
                "end": e
            })
    with open(args.input_pause_timestamps, "r") as f:
        pauses = []
        for line in f.readlines():
            s, e = line.split()
            s = float(s)
            e = float(e)
            pauses.append({
                "start": s,
                "end": e
            })
    with open(args.input_background_person_detection, "r") as f:
        background_person_detection = json.load(f)["background_person"]
    with open(args.input_emotions_detection, "r") as f:
        emotions_detection = {"emotions_detection": json.load(f)}
    with open(args.input_gunning_fog, "r") as f:
        gunning_fog = {}
        for line in f.readlines():
            k, v = line.split("\t")
            gunning_fog[k] = v
    with open(args.input_language_detection, "r") as f:
        lang = []
        for line in f.readlines():
            w, pl = line.split()
            lang.append({
                "word": w,
                "polish": pl
            })
    with open(args.input_audio_analysis, "r") as f:
        audio_analysis = json.load(f)

    data = {
        "comparison": comparison,
        "sp": sp,
        "ocr": ocr,
        "word_timestamps": words,
        "pause_timestamps": pauses,
        "background_person_detection": background_person_detection,
        "emotions_detection": emotions_detection,
        "gunning_fog": gunning_fog,
        "language_detection": lang,
        "audio_analysis": audio_analysis,
    }

    print(data)
    with open(args.output_merged, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    merge_data()
