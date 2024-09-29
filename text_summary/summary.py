import argparse
import os
from openai import OpenAI


class ConditionedGPT:
    def __init__(self, model: str, prompt: str, samples: list[tuple[str, str]]):
        self.client = OpenAI()
        self.model = model

        self.messages = [{"role": "system", "content": prompt}]
        for sample in samples:
            self.messages.append({"role": "user", "content": sample[0]})
            self.messages.append({"role": "assistant", "content": sample[1]})

    def request(self, input: str) -> list[str]:
        msgs = self.messages.copy()
        msgs.append({"role": "user", "content": input})
        completion = self.client.chat.completions.create(
            model=self.model, messages=msgs
        )
        res = completion.choices[0].message
        return res


class Summary(ConditionedGPT):
    MODEL = "gpt-4o-mini"

    PROMPT = "Twoim zadaniem jest wysłuchanie wypowiedzi i określenie co z niej rozumiesz. Wypowiedź jest długa, ale zawiera konkretne informacje. Wyszczególnij najważniejsze informacje w wysłuchanej wypowiedzi. Pomiń zbędne szczegóły."

    SAMPLES = [
        (
            "Ukraiński dowódca wojskowy twierdzi, że jego wojska kontrolują teraz setki mil kwadratowych rosyjskiego terytorium w regionie Chersonia, co skutkuje wydaniem przez Rosję nakazu ewakuacji, ponieważ Ukraina posuwa się dalej w głąb kraju. Jaki jest cel Ukrainy i czy będzie w stanie utrzymać to terytorium?",
            "1. Zdaniem Ukraińskiego dowódcy, jego wojska kontrolują ogromny obszar Chersonia.\n2. Rosja zarządziła ewakuację z okupowanego terytorium.\n3. Ukraina posuwa się w głąb Rosji.\n4. Pytanie jaki jest cel Ukrainy i czy sobie poradzi?",
        ),
        (
            "i muszę powiedzieć, że ze zdziwieniem patrzyłem na wyniki dzisiejszego głosowania, gdy część z parlamentarzystów, i to bynajmniej nie po prawej stronie sceny politycznej, wstrzymała się od głosu. Bo czy te rozwiązania, o których mówię, nie powinny być wprowadzone? Czy państwo nie uważacie, że za te obrzydliwe przestępstwa kara powinna być bardzo, bardzo surowa i nieuchronna?",
            "1. Mówca wyraził zdziwienie wynikami dzisiejszego głosowania.\n2. Niektórzy parlamentarzyści lewicy wstrzymali się od głosu.\n3. Mówca sugeruje by omawiane poważne przestępstwa powinny być surowo karane.",
        ),
        (
            "Jednym z głównych punktów krytyki wobec Pieronka są jego ostre wypowiedzi dotyczące metody in vitro. „Czymże jest literackie wyobrażenie Frankensteina, czyli istoty powołanej do życia wbrew naturze, jak nie pierwowzorem in vitro? To makabryczna perspektywa, ale ona istnieje” - mówił biskup w rozmowie z serwisem Onet.pl, porównując metodę leczenia niepłodności do tworzenia potwora z ludzkich ciał. Jego opinie wywołały oburzenie zwłaszcza wśród rodzin, które skorzystały z tej metody, oraz obrońców praw człowieka.",
            "1. Biskup krytykował Pieronka za ostre wypowiedzi na temat in vitro.\n2. Opinie biskupa wywołały oburzenie wśród rodzin korzystających z in vitro.",
        ),
    ]

    def __init__(self):
        super().__init__(Summary.MODEL, Summary.PROMPT, Summary.SAMPLES)

    def estimate(self, input: str) -> list[str]:
        res = self.request(input)

        # If refused, set hate speech
        if res.refusal:
            return ["Wypowiedź zahacza o niebezpieczne tematy."]

        # Extract keypoints
        keypoints = res.content.split("\n")
        for i in range(len(keypoints)):
            j = keypoints[i].index(".")
            if j != -1:
                keypoints[i] = keypoints[i][j + 1 :].strip()

        return keypoints


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="text_summary")
    parser.add_argument("--original_text", type=str)
    parser.add_argument("--summary_text", type=str)
    args = parser.parse_args()

    original_text_path = os.path.abspath(args.original_text)
    summary_text_path = os.path.abspath(args.summary_text)

    with open(original_text_path, "r") as f:
        original_text_data = f.read()

    summary = Summary()
    keypoints = summary.estimate(original_text_data)

    summary_text_data = "\n".join(keypoints)

    with open(summary_text_path, "w") as f:
        f.write(summary_text_data)
