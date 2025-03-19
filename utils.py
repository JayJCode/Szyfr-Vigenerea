"""
Potrzebne parametry i funkcje pomocnicze
"""

class Utils:

    def __init__(self):
        self.slownik_male = {chr(i): i - 97 for i in range(97, 123)}
        self.slownik_duze = {chr(i): i - 65 for i in range(65, 91)}

    def odczytaj(self, file: str) -> str:
        with open(file, "r") as p:
            return p.read()

    def zapisz(self, file: str, text: str) -> None:
        with open(file, "w") as p:
            p.write(text)

    def dopisz(self, file: str, text: str) -> None:
        with open(file, "a") as p:
            p.write(text)