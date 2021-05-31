import secrets
import random
import word_list
import specials_list
import PySimpleGUI as sg

# https://www.zdnet.com/article/fbi-recommends-passphrases-over-password-complexity/
# https://correcthorsebatterystaple.net/

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


# Add the GUI with PySimpleGUI

sg.theme('DarkGrey9')

num_words = [
    [sg.Text('Number Of Words:', size=(25, 0), font=('Courier New', 10, 'bold')), sg.InputOptionMenu(('2', '3', '4', '5', '6', '7', '8'), default_value=3, key='words')]
]

word_case = [
    [sg.Text('Word Case:', size=(25, 0), font=('Courier New', 10, 'bold')), sg.InputOptionMenu(('lower', 'upper', 'title'), default_value='lower', key='word_case')]
]

word_separator = [
    [sg.Text('Word Separator:', size=(25, 0), font=('Courier New', 10, 'bold')), sg.InputOptionMenu(('space', 'dash'), default_value='space', key='separator')]
]

special_character = [
    [sg.Checkbox(' Use Special Character', size=(25, 1) ,font=('Courier New', 10, 'bold'), key='special')]
]

output = [
    [sg.Multiline(size=(70, 2), font=('Courier New', 9), key='output', write_only=True, no_scrollbar=True, text_color='white', disabled=True)]
]


layout = [
    [sg.Text('')],
    [num_words],
    [word_case],
    [word_separator],
    [sg.Text('')],
    [special_character],
    [sg.Text('')],
    [sg.Frame('Passphrase', output)],
    [sg.Text('')],
    [sg.Button('Generate', key='GENERATE'), sg.Text('', size=(50, 1)), sg.Exit()]
]

window = sg.Window('Passphrase Generator', layout, grab_anywhere=False)

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'GENERATE':
        get_passphrase = PassPhrase(int(values['words']), values['word_case'], values['separator'], values['special'])

        window['output'].update(get_passphrase.generate_pass())

window.close()

# new_passphrase = PassPhrase(4, 'title', 'space', True)
# print(new_passphrase.generate_pass())