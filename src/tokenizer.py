"""
This tokeniser is an heuristic based character wise tokeniser for Yoruba words
"""

class Tokenizer:
    def __init__(self, dataset=None):
        self.char_to_token = {}
        self.token_to_char = {}
        self.vowels_2_map = dict([
            ('à', 'à'), ('á', 'á'), ('á', 'á'), ('è', 'è'), ('è', 'è'), ('é', 'é'),
            ('é', 'é'), ('é', 'é'), ('é', 'é'), ('ì', 'ì'), ('í', 'í'), ('í', 'í'),
            ('ò', 'ò'), ('ò', 'ò'), ('ó', 'ó'), ('ó', 'ó'), ('ó', 'ó'), ('ó', 'ó'),
            ('ù', 'ù'), ('ú', 'ú'), ('ú', 'ú'), ('ẹ́', 'ẹ́'), ('ẹ́', 'ẹ́'), ('ọ́', 'ọ́'),
            ('ọ́', 'ọ́'), ('ṣ', 'ṣ'), ('s̩', 'ṣ'), ('ș', 'ṣ'), ('ń', 'ń'), ('ń', 'ń'),
            ('ḿ', 'ḿ')
 ])
        if dataset != None:
            self.get_tokens_mapping(dataset)


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
    
    def n_char(self, name: list) -> list:
        """ 
        Some N-gram char occurs in Yoruba, while they are made of multiple chars
        e.g "gb" or vowels such as "an, in, en, on, un", they are regarded as just 
        a single character in Yoruba, so this function identify cases where this happens
        return the n-gram characters as one
        """
        vowels = [
            'a', 'à', 'á', 'è', 'é', 'e', 'ẹ́', 'ẹ̀', 'ẹ', 'ì', 'í', 'i', 
            'ò', 'ó', 'o', 'ọ́', 'ọ̀', 'ọ', 'ù', 'ú', 'u',]
        n = 0
        len_word = len(name)
        # iterate through the name charaterwise
        while n < len_word:
            # check  if the char is "n" and the characteer before is a vowel
            if (name[n] == "n") and (n != 0) and (name[n-1] in vowels):
                # most times, when the next char after the n is a vowel and the char before 
                # is also a vowel, the "n" char is usualy independent of the one before
                if (n+1 < len_word) and (name[n+1] in vowels):
                    n += 1
                else:
                    # yes, make the last char evaluated the vowel and 'n'
                    name[n-1] = name[n-1] + name[n]
                    # delete the "n" char and reduce the length of the list by 1
                    del name[n]
                    len_word -= 1
            # also check if the char is b and if true, if the letter before is "g"
            elif (name[n] == "b") and (n != 0) and (name[n-1] == "g"):
                # yes, its a variant of letter pronounced as "gb"
                name[n-1] = name[n-1] + name[n]
                # delete the "b" char and reduce the length of the list by 1
                del name[n]
                len_word -= 1
            else:
                n += 1
        return name


    def create_vocabulary(self, words: list) -> list:
        """
        create a character vocabulary of all characters in the whole dataset
        """
        self.vocabulary = []
        for word in words:
            self.vocabulary.extend(self.preprocess(word))

        self.vocabulary = list(set(self.vocabulary))


    def get_tokens_mapping(self, words: list) -> None:
        """ 
        Create a mapping for each character to a unique token
        """
        self.create_vocabulary(words)
        for i, char in enumerate(self.vocabulary):
            # character to token mapping
            self.char_to_token[char] = i
            # token to character mapping
            self.token_to_char[i] = char
