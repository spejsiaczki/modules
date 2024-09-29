from conditioned_gpt import ConditionedGPT


class Questions(ConditionedGPT):
    MODEL = "gpt-4o-mini"

    PROMPT = "Jesteś obiektywnym reporterem/krytykiem medialnym. Wysłuchaj wypowiedzi i zastanów się nad jej treścią. Następnie sformułuj 10 pytań, które mogłyby być zadane w kontekście tej wypowiedzi. Pytania zadawaj w formie bezosobowej, bez odnoszenia się bezpośrednio do mówcy."

    SAMPLES = [
        (
            "Audytem objęliśmy 96 podmiotów, a łączna kwota badanych środków publicznych to około 100 miliardów złotych. W toku działań stwierdziliśmy między innymi niegospodarne i niecelowe wydatkowanie środków publicznych oraz udzielenie dotacji podmiotom które nie spełniały kryteriów konkursowych.",
            """1. Jakie konkretnie podmioty zostały objęte audytem i na jakiej podstawie zostały wybrane do kontroli?
2. W jaki sposób zostało ustalone, że doszło do niegospodarnego i niecelowego wydatkowania środków publicznych?
3. Jakie były najczęstsze nieprawidłowości stwierdzone podczas audytu i które obszary finansowania były najbardziej narażone na tego typu działania?
4. Czy przeprowadzono postępowania wyjaśniające wobec podmiotów, które otrzymały dotacje niespełniające kryteriów konkursowych?
5. W jaki sposób audytorzy oceniali spełnianie lub niespełnianie kryteriów konkursowych przez podmioty, które otrzymały dotacje?
6. Jakie kroki podjęto lub planuje się podjąć w celu zapobieżenia podobnym przypadkom niegospodarności w przyszłości?
7. Czy kwota 100 miliardów złotych obejmuje tylko środki, które były przedmiotem nieprawidłowości, czy całość kontrolowanych funduszy?
8. Czy określono, jak duży procent całej audytowanej kwoty stanowią środki, które zostały wydane niezgodnie z przeznaczeniem?
9. Jakie sankcje przewidziano wobec podmiotów, które nie spełniły kryteriów konkursowych, a mimo to otrzymały dotacje?
10. Czy audyt wskazał na jakieś pozytywne aspekty gospodarowania środkami publicznymi, czy wszystkie zidentyfikowane działania miały charakter negatywny?""",
        )
    ]

    def __init__(self):
        super().__init__(Questions.MODEL, Questions.PROMPT, Questions.SAMPLES)

    def estimate(self, input: str) -> list[str]:
        res = self.request(input)

        if res.refusal:
            return [
                "Ta wypowiedź zawiera treści, które nie powinny być powielane w mediach."
            ]

        # Extract keypoints
        keypoints = res.content.split("\n")
        for i in range(len(keypoints)):
            j = keypoints[i].index(".")
            if j != -1:
                keypoints[i] = keypoints[i][j + 1 :].strip()

        return keypoints


if __name__ == "__main__":
    questions = Questions()
    for input in [
        "Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej! Nasz wielki rodak – papież święty Jan Paweł II mówił do nas: „Europa potrzebuje Polski, a Polska potrzebuje Europy”. Te słowa są ciągle aktualne. Dlatego musimy aktywnie uczestniczyć w kształtowaniu Wspólnoty, zgodnie z wartościami wyznawanymi przez nas od ponad tysiąca lat. Od momentu, kiedy dołączyliśmy do rodziny chrześcijańskich narodów Europy. Dzisiaj jesteśmy świadkami wielkiego sporu o przyszły kształt Unii Europejskiej. Pojawiają się niepokojące tendencje do federalizacji, mówi się o zmianach traktatów, które ograniczą suwerenność państw członkowskich. Nasza obecność w Unii Europejskiej to polska racja stanu, ale opowiadamy się za Europą wolnych narodów! Europą Ojczyzn! Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać. Dlatego tak ważne będą wybory do Parlamentu Europejskiego, które odbędą się 9 czerwca. Od tego, jakich reprezentantów wybierzemy, będzie zależał kierunek, w którym będzie podążała Unia, oraz jak polskie sprawy w Unii będą prowadzone. Zachęcam Państwa do udziału w tych wyborach.",
        "W budżecie na 2025 rok przeznaczymy ponad 221,7 mld zł na ochronę, rekordowy wzrost nakładów na ochronę zdrowia zgodnie z ustawą o blisko 31,7 mld zł, to jest to 6,1%. 0,5 mld zł na realizację programu in vitro, 8,4 mld zł na realizację świadczeń 'Aktywny rodzic', 62,8 mld zł na program 'Rodzina 800+'.",
        "Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. 0,5 mld zł na realizację programu in vitro, 8,4 mld zł na realizację świadczeń 'Aktywny rodzic', 62,8 mld zł na program 'Rodzina 800+'.",
    ]:
        print(input)
        q = questions.estimate(input)
        print("========== PYTANIA ==========")
        for i, k in enumerate(q):
            print(f"{i+1}. {k}")
        print("=============================")
