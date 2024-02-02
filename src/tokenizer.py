"""
This tokeniser is an heuristic based character wise tokeniser for Yoruba words
"""
from typing import Union

class Tokenizer:
    def __init__(self, dataset=None, vocabulary=None):
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
        self.tokens_initialised = False
        if dataset != None or vocabulary != None:
            self.get_tokens_mapping(dataset, vocabulary)
            self.tokens_initialised = True


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


    def create_vocabulary(self, words: list) -> None:
        """
        create a character vocabulary of all characters in the whole dataset
        """
        self.vocabulary = []
        for word in words:
            self.vocabulary.extend(self.preprocess(word))

        self.vocabulary = list(set(self.vocabulary))


    def get_tokens_mapping(self, words: Union[list, None], vocabulary: Union[list, None]) -> None:
        """ 
        Create a mapping for each character to a unique token
        """
        if words != None:
            self.create_vocabulary(words)
        elif vocabulary != None:
            self.vocabulary = vocabulary
        for i, char in enumerate(self.vocabulary):
            # character to token mapping
            self.char_to_token[char] = i
            # token to character mapping
            self.token_to_char[i] = char


    def get_char_to_token(self, chars: list) -> list:
        """ 
        Returns the tokens for the different characters
        """
        return [self.char_to_token[char] for char in chars]
    

    def get_token_to_char(self, tokens: list) -> list:
        """ 
        Returns the tokens for the different characters
        """
        return [self.token_to_char[token] for token in tokens]
    
    
    def __call__(self, data: list, pad: bool=False, max_length: Union[str, int, None]="max_length") -> list:
        """ 
        Tokenise and return tokens to the words given
        """
        all_tokens = []
        # check if tokens needs to be padded
        if pad:
            # if yes, ascertain that max_lenth is not None
            assert max_length != None, "Maximum length needs to be specified if pad set as True"
            # if max_length set for longest token, initatilise for zero else set as value specified
            if max_length == "max_length":
                self.max_length_ = 0
            elif type(max_length, int):
                self.max_length_ = max_length
            # if the value is neither an int or max_length, raise an exception
            else:
                raise Exception("Invalid value for max_length")
        
        # if tokens are not intialised, initialise
        if not self.tokens_initialised:
            self.get_tokens_mapping(data)

        for word in data:
            # preprocesss the tokens
            word = self.preprocess(word)
            # convert to tokens
            tokens = self.get_char_to_token(word)
            # get longest sequence lenght yet if pad and use max_length
            if pad and max_length == "max_length" and len(tokens) < self.max_length_:
                self.max_length_ = len(tokens)
            all_tokens.append(tokens)

        if pad:
            for i in range(len(all_tokens)):
                all_tokens[i] = self.pad_sequence(all_tokens[i])
        return all_tokens