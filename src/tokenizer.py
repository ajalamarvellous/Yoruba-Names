"""
This tokeniser is an heuristic based character wise tokeniser for Yoruba words
"""

class Tokenizer:
    def __init__(self):
        self.class_to_label = {}
        self.label_to_class = {}
        self.vowels_2_map = dict([
            ('à', 'à'), ('á', 'á'), ('á', 'á'), ('è', 'è'), ('è', 'è'), ('é', 'é'),
            ('é', 'é'), ('é', 'é'), ('é', 'é'), ('ì', 'ì'), ('í', 'í'), ('í', 'í'),
            ('ò', 'ò'), ('ò', 'ò'), ('ó', 'ó'), ('ó', 'ó'), ('ó', 'ó'), ('ó', 'ó'),
            ('ù', 'ù'), ('ú', 'ú'), ('ú', 'ú'), ('ẹ́', 'ẹ́'), ('ẹ́', 'ẹ́'), ('ọ́', 'ọ́'),
            ('ọ́', 'ọ́'), ('ṣ', 'ṣ'), ('s̩', 'ṣ'), ('ș', 'ṣ'), ('ń', 'ń'), ('ń', 'ń'),
            ('ḿ', 'ḿ')
 ])


    def preprocess(self , name: str) -> list:
        name = name.strip()
        name = name.lower()
        name = list(name)
        name = self.parse_sign(name)
        name = self.map_vowels(name)
        name = self.n_char(name)
        return name
    

    def parse_sign(self, name: list) -> list:
        """
        Map the tonal marks on top of the letters separated out 
        by splitting into one character back
        """
        tonal_marks = ['̀', '́', '́', '̣', '̩' ]
        n = 0
        len_word = len(name)
        # iterate through the name charaterwise
        while n < len_word:
            # check  if the next char is a tonal mark
            if name[n] in tonal_marks:
                # yes, make the previous char the sign plus that previous character
                name[n-1] = name[n-1] + name[n]
                # delete the sign and reduce the length of thee list by 1
                del name[n]
                len_word -= 1
            else:
                n += 1
        return name
    
    
    def map_vowels(self, word: list, map_table=self.vowels_2_map) -> list:
        for i, char in enumerate(word):
            if char in map_table.keys():
                word[i] = map_table[char]
        return word