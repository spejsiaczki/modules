from langdetect import detect_langs, LangDetectException
import argparse
import os


class LanguageDetection:
    FILANAME_LANG_SET = os.path.dirname(__file__) + "/lang_set.txt"

    def __init__(self):
        self.lang_set = self._load_lang_set()

    def _norm_word(self, word: str) -> str:
        return word.replace(",", "").replace(".", "").lower().strip()

    def _load_lang_set(self):
        with open(self.FILANAME_LANG_SET, "r") as f:
            return set(self._norm_word(w) for w in f.read().splitlines())

    def detect_polish(self, text: str) -> bool:
        """
        Returns a list of detected languages with confidence scores
        """

        word = self._norm_word(text)
        if word in self.lang_set:
            return True

        if any(ch in text for ch in "ęóąśłżźćń"):
            return True

        try:
            probs = [(lang.lang, lang.prob) for lang in detect_langs(text)]
            if probs[0] == "pl":
                return True
            else:
                return False
        except LangDetectException:
            return False

    @property
    def languages(self):
        return self.possible_languages


parser = argparse.ArgumentParser(
    description='language detection')
parser.add_argument('--input_text', type=str)
parser.add_argument('--output_language', type=str)


if __name__ == "__main__":
    args = parser.parse_args()

    input_text = args.input_text
    output_language = args.output_language

    with open(input_text, "r") as f:
        input_text_data = f.read()

    lang_detect = LanguageDetection()
    with open(output_language, "w") as f:
        for word in input_text_data.split():
            f.write(f"{word} {lang_detect.detect_polish(word)}\n")
