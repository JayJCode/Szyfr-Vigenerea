"""
Szyfr Vigenere'a:

Wzory:
E(k,x) = x + kj
D(k,y) = y - kj

Definicje:
E (encryption):  funkcja szyfrujaca
D (decryption):  funkcja odszyfrujaca
x (plain):  tekst jawny
y (crypto):  kryptogram
k (key): [k0, k1, k2, ..., kn-1]
"""
from utils import Utils

class Vigenere:
    def __init__(self):
        self.utils = Utils()
        self.vector_of_frequencies = {
            'a': 0.082, 'b': 0.015, 'c': 0.028, 'd': 0.043, 'e': 0.127, 'f': 0.022,
            'g': 0.02, 'h': 0.061, 'i': 0.07, 'j': 0.002, 'k': 0.008, 'l': 0.04,
            'm': 0.024, 'n': 0.067, 'o': 0.075, 'p': 0.029, 'q': 0.001, 'r': 0.06,
            's': 0.063, 't': 0.091, 'u': 0.028, 'v': 0.01, 'w': 0.023, 'x': 0.001,
            'y': 0.02, 'z': 0.001}
    
    def _prepare_key(self, length_of_plain: int) -> str:
        k = self.utils.odczytaj("key.txt").strip()
        key = ""
        for i in range(length_of_plain):
            key += k[i%len(k)]
            
        return key
    
    def prepare_text(self) -> None:
        origin_text = self.utils.odczytaj("origin.txt")
        plain_text = ""
        for i in range(len(origin_text)):
            if origin_text[i] in self.utils.slownik_male:
                plain_text += origin_text[i]
            elif origin_text[i] in self.utils.slownik_duze:
                plain_text += origin_text[i].lower()
            else:
                continue
        self.utils.zapisz("plain.txt", plain_text)
    
    def encrypt(self) -> None:
        plain = self.utils.odczytaj("plain.txt")
        key = self._prepare_key(len(plain))
        crypto = ""
        for i in range(len(plain)):
            num_of_char = self.utils.slownik_male[plain[i]] + self.utils.slownik_male[key[i]]
            crypto += chr(num_of_char % 26 + 97)
        self.utils.zapisz("crypto.txt", crypto)
        
    def decrypt(self) -> None:
        crypto = self.utils.odczytaj("crypto.txt")
        key = self._prepare_key(len(crypto))
        decrypt = ""
        for i in range(len(crypto)):
            num_of_char = self.utils.slownik_male[crypto[i]] - self.utils.slownik_male[key[i]]
            decrypt += chr(num_of_char % 26 + 97)
        self.utils.zapisz("decrypt.txt", decrypt)
        
    def _founding_key_length(self, crypto: str) -> int:
        if not crypto:
            raise ValueError("Plik 'crypto.txt' jest pusty. Nie można znaleźć długości klucza.")
        
        matches = []
        for i in range(1, len(crypto)):
            actual_matches = 0
            for j in range(len(crypto) - i):
                if crypto[j] == crypto[j + i]:
                    actual_matches += 1
            matches.append(actual_matches)
            
        if not matches:
            raise ValueError("Plik 'crypto.txt' jest za krotki. Nie można znaleźć długości klucza.")
        
        max_matches = max(matches) 
        MAGIC = max_matches//2
        indexes = [i for i, match in enumerate(matches) if match >= MAGIC]
        
        offsets = {}
        for i in range(len(indexes) - 1):
            offset = indexes[i + 1] - indexes[i]
            if offset not in offsets:
                offsets[offset] = 1
            else:
                offsets[offset] += 1
        
        key_length = max(offsets, key=offsets.get)
        return key_length

    def _find_offset(self, group: str) -> int:
        frequencies = {chr(i): 0 for i in range(97, 123)}
        for char in group:
            frequencies[char] += 1
        
        group_length = len(group)
        observed_frequencies = {char: count / group_length for char, count in frequencies.items()}

        chi_squared = {}
        for shift in range(26):
            chi_squared[shift] = 0
            for char, expected_frequency in self.vector_of_frequencies.items():
                shifted_char = chr((ord(char) - 97 + shift) % 26 + 97)
                observed_frequency = observed_frequencies.get(shifted_char, 0)
                chi_squared[shift] += ((observed_frequency - expected_frequency) ** 2) / expected_frequency
        best_shift = min(chi_squared, key=chi_squared.get)
        return best_shift

    def _group_letters(self, crypto: str, key_length: int) -> list[str]:
        groups = {i: [] for i in range(key_length)}
        for i, char in enumerate(crypto):
            groups[i % key_length].append(char)
                
        return ["".join(groups[i]) for i in range(key_length)]

    def cryptoanalysis(self) -> None:
        crypto = self.utils.odczytaj("crypto.txt")
        key_length = self._founding_key_length(crypto)
        grouped_letters = self._group_letters(crypto, key_length)
        key = ""
        for group in grouped_letters:
            num = self._find_offset(group)
            letter = chr(num + 97)
            key += letter
        self.utils.zapisz("key_found.txt", key)
        key_extended = ""
        for i in range(len(crypto)):
            key_extended += key[i%len(key)]
        decrypt = ""
        for i in range(len(crypto)):
            num_of_char = self.utils.slownik_male[crypto[i]] - self.utils.slownik_male[key_extended[i]]
            decrypt += chr(num_of_char % 26 + 97)
        self.utils.zapisz("decrypt.txt", decrypt)