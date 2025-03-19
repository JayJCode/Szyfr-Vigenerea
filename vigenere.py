"""
Program szyfrujaco-deszyfrujacy.
Napisany na potrzeby zaliczenia 2 laboratoriow.
Termin: 23 marca 2025.
Autor: Jan Janowicz
"""
from vigenere_class import Vigenere
import argparse


def argparse_init() -> argparse.Namespace:
    """
    Przyklad uzycia: python vigenere.py -e
    """
    parser = argparse.ArgumentParser()

    # Uzytkownik powinien wybrac jedna z 4 opcji mozliwych akcji
    parser.add_argument("-e", "--encryption", action="store_true", help="Szyfrowanie")
    parser.add_argument("-d", "--decryption", action="store_true", help="Odszyfrowanie")
    parser.add_argument("-p", "--prepare", action="store_true", help="Przygotowanie tekstu")
    parser.add_argument("-k", "--krypto", action="store_true", help="Kryptoanaliza wylacznie w oparciu o kryptogram")

    return parser.parse_args()

def wybor_algorytmu(args: argparse.Namespace) -> None:
    """
    Funkcja wybiera algorytm szyfrowania w zaleznosci od wyboru uzytkownika.
    """
    vigenere = Vigenere()
    if (args.encryption and args.decryption or args.encryption and args.prepare or args.encryption and args.krypto
        or args.decryption and args.prepare or args.decryption and args.krypto or args.prepare and args.krypto
        or args.encryption and args.decryption and args.prepare or args.encryption and args.decryption and args.krypto
        or args.encryption and args.prepare and args.krypto or args.decryption and args.prepare and args.krypto
        or args.encryption and args.decryption and args.prepare and args.krypto):
        raise ValueError("Wybierz tylko jedna akcje")
    elif args.encryption:   vigenere.encrypt()
    elif args.decryption:   vigenere.decrypt()
    elif args.prepare:      vigenere.prepare_text()
    elif args.krypto:       vigenere.cryptoanalysis()
    else:                   raise ValueError("Brak wartosci: musisz wybrac jedna z opcji akcji (-e, -d, -p, -k)")

def main():
    args = argparse_init()
    wybor_algorytmu(args)

main()