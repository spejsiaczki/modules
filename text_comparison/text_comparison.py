from Levenshtein import ratio
from typing import Tuple
import re
import os
import argparse


class TextComparison:
    def __init__(self) -> None:
        pass

    def compare_leven(self, text_a: str, text_b: str) -> float:
        """
        Compare two texts and return a similarity score ratio.
        """
        return ratio(
            self._norm_text(text_a),
            self._norm_text(text_b))

    def _norm_text(self, text: str) -> str:
        text = re.sub(r'[^A-Za-z0-9]+', '', text).lower()
        return text

    def compare_length(self, text_a: str, text_b: str) -> float:
        """
        Compare two texts and return a similarity score based on length.
        """
        len_a = len(self._norm_text(text_a))
        len_b = len(self._norm_text(text_b))

        return min(len_a, len_b) / max(len_a, len_b)

    def compare(self,
                text_a: str,
                text_b: str) -> Tuple[float, str]:
        leven = self.compare_leven(text_a, text_b)
        length = self.compare_length(text_a, text_b)
        return leven * length

    def compare_with_description(self, text_a: str, text_b: str) -> Tuple[float, str]:
        """
        Compare two texts and return a similarity score based on length.
        """
        cmp = self.compare(text_a, text_b)
        if cmp > 0.9:
            return cmp, "Mocna zgodność"
        if cmp > 0.7:
            return cmp, "Zgodność"
        elif cmp > 0.5:
            return cmp, "Cześciowa zgodność"
        else:
            return cmp, "Not similar"


parser = argparse.ArgumentParser(
    description='text_comparison')
parser.add_argument('--input_ocr', type=str)
parser.add_argument('--input_sr', type=str)
parser.add_argument('--output', type=str)

if __name__ == "__main__":
    args = parser.parse_args()

    input_ocr = os.path.abspath(args.input_ocr)
    input_sr = os.path.abspath(args.input_sr)
    output = os.path.abspath(args.output)

    with open(input_ocr, "r") as f:
        input_ocr_data = f.read()
    with open(input_sr, "r") as f:
        input_sr_data = f.read()

    text_comparison = TextComparison()
    cmp = text_comparison.compare(input_ocr_data, input_sr_data)
    des = text_comparison.compare_with_description(
        input_ocr_data, input_sr_data)

    with open(output, "w") as f:
        f.write(f"{cmp}\t{des}")
