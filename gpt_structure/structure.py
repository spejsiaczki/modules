from conditioned_gpt import ConditionedGPT


class Structure(ConditionedGPT):
    MODEL = "gpt-4o-mini"

    PROMPT = "Twoim zadaniem jest wysłuchanie wypowiedzi i ocenienie jest struktury. Określ czy wypowiedź zawiera wstęp, rozwinięcie i zakończenie. Określ też czy nie został zmieniony temat wypowiedzi."

    SAMPLES = [
        (
            "W tym roku zamierzamy zwiększyć ilość żołnierzy w wojsku polskim o ponad 400 tysięcy. Będziemy w tym roku mieli w takim razie najwięcej pracowników sektoru publicznego, między innymi lekarzy. Lekarze w tym roku dostaną podwyżki wynoszące aż do tysiąca złotych miesięcznie. Jest to duży rok dla lekarzy.",
            "Wstęp: TAK\nRozwinięcie: TAK\nZakończenie: TAK\nZmiana tematu: TAK",
        ),
        (
            "W dzisiejszych czasach zdrowy styl życia zyskuje na znaczeniu, a coraz więcej osób zwraca uwagę na swoją dietę oraz aktywność fizyczną. Regularne ćwiczenia i zbilansowana dieta nie tylko poprawiają samopoczucie, ale również wpływają na nasze zdrowie psychiczne.",
            "Wstęp: TAK\nRozwinięcie: TAK\nZakończenie: NIE\nZmiana tematu: NIE",
        ),
        (
            "Dzięki innowacjom, takim jak sztuczna inteligencja, zyskujemy narzędzia, które znacząco ułatwiają nam codzienne zadania. Z drugiej strony, nie możemy zapominać o znaczeniu natury i ochrony środowiska, które stają się coraz bardziej palącymi kwestiami. W obliczu zmian klimatycznych musimy znaleźć równowagę między postępem technologicznym a zrównoważonym rozwojem naszej planety.",
            "Wstęp: NIE\nRozwinięcie: TAK\nZakończenie: TAK\nZmiana tematu: TAK",
        ),
        (
            "W obliczu zmian klimatycznych musimy znaleźć równowagę między postępem technologicznym a zrównoważonym rozwojem naszej planety.",
            "Wstęp: NIE\nRozwinięcie: NIE\nZakończenie: TAK\nZmiana tematu: NIE",
        ),
        (
            "W dzisiejszych czasach coraz więcej ludzi zwraca uwagę na zdrowy styl życia, co przekłada się na wzrost popularności sportów.",
            "Wstęp: TAK\nRozwinięcie: NIE\nZakończenie: NIE\nZmiana tematu: NIE",
        ),
        (
            "Dzietność w Polsce od lat pozostaje na niskim poziomie, co budzi wiele obaw dotyczących przyszłości społeczeństwa. Wzrost kosztów życia, trudności w godzeniu pracy z opieką nad dziećmi oraz niepewność zawodowa to tylko niektóre czynniki wpływające na decyzje rodzinne. Z drugiej strony, w ostatnich latach zauważalny jest rozwój programów wsparcia dla rodziców, które mogą poprawić sytuację demograficzną.",
            "Wstęp: TAK\nRozwinięcie: TAK\nZakończenie: NIE\nZmiana tematu: TAK",
        ),
        (
            "W ostatnich miesiącach obserwujemy znaczny wzrost cen paliw w Polsce, co ma istotny wpływ na codzienne życie obywateli. Przyczyny tego zjawiska są złożone, obejmujące zarówno globalne tendencje cenowe, jak i lokalne czynniki, takie jak podatki czy kursy walut. Wzrost cen paliw prowadzi do podwyżek kosztów transportu, co z kolei wpływa na ceny żywności i innych towarów. W obliczu tych wyzwań, konieczne jest poszukiwanie rozwiązań, które mogą złagodzić skutki dla polskich konsumentów.",
            "Wstęp: TAK\nRozwinięcie: TAK\nZakończenie: TAK\nZmiana tematu: NIE",
        ),
    ]

    def __init__(self):
        super().__init__(Structure.MODEL, Structure.PROMPT, Structure.SAMPLES)

    def estimate(self, input: str) -> list[str]:
        res = self.request(input)

        if res.refusal:
            return [False, False, False, False]

        keypoints = res.content.split("\n")
        results = []
        for keyp in keypoints:
            keyp = keyp + " "
            keyp = keyp.lower()
            keypres = keyp.rfind(" tak ")
            if keypres != -1:
                results.append(True)
            else:
                results.append(False)

        return results


if __name__ == "__main__":
    structure = Structure()
    for input in [
        "Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. Dlatego każdego dnia musimy zabiegać o polskie sprawy w Unii Europejskiej! Nasz wielki rodak – papież święty Jan Paweł II mówił do nas: „Europa potrzebuje Polski, a Polska potrzebuje Europy”. Te słowa są ciągle aktualne. Dlatego musimy aktywnie uczestniczyć w kształtowaniu Wspólnoty, zgodnie z wartościami wyznawanymi przez nas od ponad tysiąca lat. Od momentu, kiedy dołączyliśmy do rodziny chrześcijańskich narodów Europy. Dzisiaj jesteśmy świadkami wielkiego sporu o przyszły kształt Unii Europejskiej. Pojawiają się niepokojące tendencje do federalizacji, mówi się o zmianach traktatów, które ograniczą suwerenność państw członkowskich. Nasza obecność w Unii Europejskiej to polska racja stanu, ale opowiadamy się za Europą wolnych narodów! Europą Ojczyzn! Wiemy, że politycy i urzędnicy unijni bywają czasem trudnym partnerem – przekonywaliśmy się o tym w ostatnich latach wielokrotnie. Interesy unijnej biurokracji oraz niektórych państw członkowskich nieraz bywają sprzeczne z polskimi. W Unii każdego dnia trwa walka, twarda walka o interesy poszczególnych krajów i trzeba o nie skutecznie zabiegać. Dlatego tak ważne będą wybory do Parlamentu Europejskiego, które odbędą się 9 czerwca. Od tego, jakich reprezentantów wybierzemy, będzie zależał kierunek, w którym będzie podążała Unia, oraz jak polskie sprawy w Unii będą prowadzone. Zachęcam Państwa do udziału w tych wyborach.",
        "W budżecie na 2025 rok przeznaczymy ponad 221,7 mld zł na ochronę, rekordowy wzrost nakładów na ochronę zdrowia zgodnie z ustawą o blisko 31,7 mld zł, to jest to 6,1%. 0,5 mld zł na realizację programu in vitro, 8,4 mld zł na realizację świadczeń 'Aktywny rodzic', 62,8 mld zł na program 'Rodzina 800+'.",
        "Szanowni Państwo, Drodzy Rodacy! Przed Polską i przed Unią Europejską wiele wyzwań dotyczących bezpieczeństwa i gospodarki. Od tego, jak na nie odpowiemy, zależy nasza przyszłość. Będąc w Unii, możemy wpływać na jej kształt, nadawać kluczowe kierunki. Nasz głos ma znaczenie. 0,5 mld zł na realizację programu in vitro, 8,4 mld zł na realizację świadczeń 'Aktywny rodzic', 62,8 mld zł na program 'Rodzina 800+'.",
    ]:
        print(input)
        print("->", structure.estimate(input))
