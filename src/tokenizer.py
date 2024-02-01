"""
This tokeniser is an heuristic based character wise tokeniser for Yoruba words
"""

class Tokenizer:
    def __init__(self):
        self.class_to_label = {}
        self.label_to_class = {}

    def preprocess(self , name: str) -> list:
        name = name.strip()
        name = name.lower()
        name = list(name)
        name = self.parse_sign(name)
        name = self.map_vowels(name)
        name = self.n_char(name)
        return name
    
