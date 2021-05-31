import secrets
import random
import word_list
import specials_list
import PySimpleGUI as sg

class PassPhrase:
    '''
    Returns a multi-word passphrase

    Attributes:
    -----------
        word_count : int
            An integer representing number of words in the passphrase.  Default is 3
        case : str 
            A string that determines the word case to be used.  Options are lower,
            upper and title
        separator : str
            A string indicating the type of word separator to be used in the passphrase.
            Options are space and dash.  Default is space.
        special_character : bool
            Boolean value that determines whether a special character should be inserted 
            into the passphrase.  Default is False

    Methods:
    --------
    secret_number(number=7):
        Generates a cryptographically secure number.
    generate_pass():
        Generates the passphrase list
    '''

    def __init__(self, word_count, case, separator='space', special_character=False) -> None:
        self.word_count = word_count
        self.case = case
        self.separator = separator
        self.special_character = special_character

    def secret_num(self, number=7):
        '''
        Generates the cryptographically secure number used in the generate_pass method

        Parameters
        ----------
        number : int
            Integer for the upper range of the secrets.choice method.  (Default is 7)

        Returns
        -------
        Randomly generated integer in the range of 1 - 7
        '''
        return secrets.choice(range(1, number))

    def generate_pass(self):
        '''
        Creates the passphrase list of words.

        Returns
        -------
        passphrase words the number of which is determined by the parameter word_count
        '''
        
        phrase_words = []

        # By default, generate a secure number to be used to lookup the special character in the 
        # specials_list.py.  If the special_character argument is True, it will be appended to 
        # the passphrase list.
        special_character = specials_list.specials_dictionary[int(secrets.choice(range(1, 23)))]

        # Iterate self.word_count number of times.  Each iteration, generate 5 secure numbers that
        # is used to look up a word for the passphrase in word_list.py
        for i in range(self.word_count):

            count = 0
            number_key = ''

            while count < 5:

                secret_key = self.secret_num()
                number_key += str(secret_key)
                count += 1

            # If the user attempts to pass in a case name that is not a string method
            # for example, none, instead of lower, upper, title/capitalize, default to lower case.
            # Otherwise use the __getattribute__ method to dynamically set case
            try:
                phrase_words.append(word_list.word_dictionary[int(number_key)].__getattribute__(self.case)())

            except AttributeError:
                phrase_words.append(word_list.word_dictionary[int(number_key)])

        # Append special character if opted for by the boolean parameter special_character
        if self.special_character:
            phrase_words.append(special_character)

        # Two options for word separators.  A empty space or dash.  Defaults to dash
        if self.separator == 'space':

            # For some added 'randomness' shuffle the final list.  This has the added benefit
            # of also shuffling the position of the special character so that it is not always
            # at the end of the list
            return ' '.join(random.sample(phrase_words, len(phrase_words)))
        
        else:
            return '-'.join(random.sample(phrase_words, len(phrase_words)))


passphrase = PassPhrase(4, 'title', 'space', True)
print(passphrase.generate_pass())