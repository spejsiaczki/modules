from conditioned_gpt import ConditionedGPT


class Sentiment(ConditionedGPT):
    MODEL = "gpt-4o-mini"

    PROMPT = 'Twoim zadaniem jest okreslenie sentymentu wypowiedzi. Określ ton wypowiedzi (pozytywny, negatywny, neutralny). Dodatkowo określ jakie emocje może wywołać w odbiorcy. Jeśli wypowiedź zawiera mowę nienawiści, określ emocje odbiorcy jako "nienawiść".'

    SAMPLES = [
        (
            "Działania rządu w sprawie COVID-19 uderzają w wolność obywateli.",
            "Ton wypowiedzi: negatywny\nEmocje: gniew",
        ),
        (
            "W końcu zaczęto dbać o środowisko",
            "Ton wypowiedzi: pozytywny\nEmocje: radość",
        ),
        ("nienawidzę czarnoskórych", "Ton wypowiedzi: negatywny\nEmocje: nienawiść"),
        (
            "nie mam zdania na ten temat.",
            "Ton wypowiedzi: neutralny\nEmocje: obojętność",
        ),
        (
            "Nie podoba mi się ten pomysł.",
            "Ton wypowiedzi: negatywny\nEmocje: niezadowolenie, rozczarowanie",
        ),
        (
            "Jesteśmy zadowoleni z wyników",
            "Ton wypowiedzi: pozytywny\nEmocje: zadowolenie",
        ),
        (
            "wszystko jest w porządku",
            "Ton wypowiedzi: neutralny\nEmocje: spokój, troska",
        ),
        (
            "orlen osiągnął rekordowe zyski w tym roku",
            "Ton wypowiedzi: neutralny\nEmocje: przekaz informacyjny",
        ),
    ]

    def __init__(self):
        super().__init__(Sentiment.MODEL, Sentiment.PROMPT, Sentiment.SAMPLES)

    def estimate(self, input: str) -> tuple[str, str, bool]:
        res = self.request(input)

        if res.refusal:
            return "negatywny", "niebezpieczne treści", True

        content = res.content

        tone = content.split("\n")[0].split(": ")[1].lower().strip()
        emotions = content.split("\n")[1].split(": ")[1].lower().strip()
        hate = "nienawi" in emotions

        return tone, emotions, hate


if __name__ == "__main__":
    sentiment = Sentiment()
    for input in [
        "Niepełnosprawni w naszym kraju nie przyczyniają się do rozwoju gospodarczego.",
        "Orlen osiągnął rekordowe zyski w tym roku",
        "Prezydent Duda nie wsparł protestujących przeciwko reformie sądownictwa.",
        "Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać.",
        "Nasza obecność w Unii Europejskiej jest częścią naszej wielkiej wspaniałej historii. Historii Polski, która jest historią wolności.",
        "Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej!",
    ]:
        print(input)
        print("->", sentiment.estimate(input))
