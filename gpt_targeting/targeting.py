from conditioned_gpt import ConditionedGPT


class Targeting(ConditionedGPT):
    MODEL = "gpt-4o-mini"

    PROMPT = "Twoim zadaniem jest wysłuchanie wypowiedzi i określenie potencjalnej docelowej grupy słuchaczy. Scharakteryzuj grupę ze względu na wiek i/lub wykształcenie/zainteresowania."

    SAMPLES = [
        (
            "Ukraiński dowódca wojskowy twierdzi, że jego wojska kontrolują teraz setki mil kwadratowych rosyjskiego terytorium w regionie Chersonia, co skutkuje wydaniem przez Rosję nakazu ewakuacji, ponieważ Ukraina posuwa się dalej w głąb kraju. Jaki jest cel Ukrainy i czy będzie w stanie utrzymać to terytorium?",
            "Grupa docelowa: MŁODZIEŻ SZKOLNA I DOROŚLI ZAINTERESOWANI POLITYKĄ I DZIAŁANIAMI NA FRONCIE",
        ),
        (
            "i muszę powiedzieć, że ze zdziwieniem patrzyłem na wyniki dzisiejszego głosowania, gdy część z parlamentarzystów, i to bynajmniej nie po prawej stronie sceny politycznej, wstrzymała się od głosu. Bo czy te rozwiązania, o których mówię, nie powinny być wprowadzone? Czy państwo nie uważacie, że za te obrzydliwe przestępstwa kara powinna być bardzo, bardzo surowa i nieuchronna?",
            "Grupa docelowa: OSOBY DOROSŁE ZAINTERESOWANE POLITYKĄ KRYMINALNĄ I WYMIAREM SPRAWIEDLIWOŚCI",
        ),
        (
            "Jednym z głównych punktów krytyki wobec Pieronka są jego ostre wypowiedzi dotyczące metody in vitro. „Czymże jest literackie wyobrażenie Frankensteina, czyli istoty powołanej do życia wbrew naturze, jak nie pierwowzorem in vitro? To makabryczna perspektywa, ale ona istnieje” - mówił biskup w rozmowie z serwisem Onet.pl, porównując metodę leczenia niepłodności do tworzenia potwora z ludzkich ciał. Jego opinie wywołały oburzenie zwłaszcza wśród rodzin, które skorzystały z tej metody, oraz obrońców praw człowieka.",
            "Grupa docelowa: PARAFIANIE ZAINTERESOWANI ZAMIESZANIEM WOKÓŁ PIERONKA",
        ),
        (
            "Witajcie, moi drodzy! Dziś chciałbym poruszyć temat, który dotyczy każdego z nas. Mianowicie, chciałbym porozmawiać o tym, jak ważne jest dbanie o swoje zdrowie psychiczne. W dzisiejszych czasach, kiedy tempo życia jest tak szybkie, a stres towarzyszy nam na każdym kroku, niezwykle ważne jest, aby zadbać o swoje zdrowie psychiczne. Wiele osób nie zdaje sobie sprawy z tego, jak bardzo stres wpływa na nasze zdrowie. Dlatego też, chciałbym zachęcić Was do tego, abyście zwrócili uwagę na swoje samopoczucie i zadbali o swoje zdrowie psychiczne.",
            "Grupa docelowa: MŁODZIEŻ I DOROŚLI ZAINTERESOWANI ZDROWIEM PSYCHICZNYM",
        ),
    ]

    def __init__(self):
        super().__init__(Targeting.MODEL, Targeting.PROMPT, Targeting.SAMPLES)

    def estimate(self, input: str) -> str:
        res = self.request(input)

        # If refused, assume hate speech
        if res.refusal:
            return ["tekst wydaje się być nieodpowiedni dla żadnej grupy docelowej"]

        # Extract target group
        answer = res.content.lower()
        i = answer.find("grupa docelowa:")
        if i != -1:
            answer = answer[i + len("grupa docelowa:") :]
        answer = answer.strip(". ").replace(". ", "; ")

        return answer


if __name__ == "__main__":
    targeting = Targeting()
    for input in [
        """Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej! Nasz wielki rodak – papież święty Jan Paweł II mówił do nas: „Europa potrzebuje Polski, a Polska potrzebuje Europy”. Te słowa są ciągle aktualne. Dlatego musimy aktywnie uczestniczyć w kształtowaniu Wspólnoty, zgodnie z wartościami wyznawanymi przez nas od ponad tysiąca lat. Od momentu, kiedy dołączyliśmy do rodziny chrześcijańskich narodów Europy. Dzisiaj jesteśmy świadkami wielkiego sporu o przyszły kształt Unii Europejskiej. Pojawiają się niepokojące tendencje do federalizacji, mówi się o zmianach traktatów, które ograniczą suwerenność państw członkowskich. Nasza obecność w Unii Europejskiej to polska racja stanu, ale opowiadamy się za Europą wolnych narodów! Europą Ojczyzn! Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać. Dlatego tak ważne będą wybory do Parlamentu Europejskiego, które odbędą się 9 czerwca. Od tego, jakich reprezentantów wybierzemy, będzie zależał kierunek, w którym będzie podążała Unia, oraz jak polskie sprawy w Unii będą prowadzone. Zachęcam Państwa do udziału w tych wyborach.""",
        """W poprzednim zadaniu składniki każdej sumy były sobie równe. Nie trudno dodać równe liczby. Teraz nauczymy się dodawać różne ułamki o różnych mianownikach. Ważne! Aby dodać ułamki o różnych mianownikach, trzeba najpierw sprowadzić je do wspólnego mianownika, skracając lub rozszerzając. Następnie należy dodać je tak, jak się dodaje ułamki o jednakowych mianownikach.""",
    ]:
        target_group = targeting.estimate(input)
        print(input)
        print("->", target_group)
