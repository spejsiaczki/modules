from conditioned_gpt import ConditionedGPT


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
    summary = Summary()
    for input in [
        """Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej! Nasz wielki rodak – papież święty Jan Paweł II mówił do nas: „Europa potrzebuje Polski, a Polska potrzebuje Europy”. Te słowa są ciągle aktualne. Dlatego musimy aktywnie uczestniczyć w kształtowaniu Wspólnoty, zgodnie z wartościami wyznawanymi przez nas od ponad tysiąca lat. Od momentu, kiedy dołączyliśmy do rodziny chrześcijańskich narodów Europy. Dzisiaj jesteśmy świadkami wielkiego sporu o przyszły kształt Unii Europejskiej. Pojawiają się niepokojące tendencje do federalizacji, mówi się o zmianach traktatów, które ograniczą suwerenność państw członkowskich. Nasza obecność w Unii Europejskiej to polska racja stanu, ale opowiadamy się za Europą wolnych narodów! Europą Ojczyzn! Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać. Dlatego tak ważne będą wybory do Parlamentu Europejskiego, które odbędą się 9 czerwca. Od tego, jakich reprezentantów wybierzemy, będzie zależał kierunek, w którym będzie podążała Unia, oraz jak polskie sprawy w Unii będą prowadzone. Zachęcam Państwa do udziału w tych wyborach."""
    ]:
        keypoints = summary.estimate(input)
        print(input)
        print("========== PODSUMOWANIE ==========")
        print(f"{len(input)} znaków -> {sum(len(k) for k in keypoints)} znaków")
        print("========== PODSUMOWANIE ==========")
        for i, k in enumerate(keypoints):
            print(f"{i + 1}. {k}")
