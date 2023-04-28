from sys import argv
from itertools import chain

class Chord:
    def __init__(self, notes = []):
        self.notes = notes
        self.type = "unknown"

    def add_note(self, note: str):
        self.notes.append(note)

    def __str__(self):
        return(str(self.notes))

class FretboardPosition:
    def __init__(self, string: int, fret: int):
        self.string = string
        self.fret = fret
    
    def __str__(self):
        return(f"(String {self.string}, fret {self.fret})")
    
    def __eq__(self, other):
        if other == None:
            return False
        
        if (self.string == other.string) and (self.fret == other.fret):
            return True
        else:
            return False

class Term:
    def __init__(self, sequence_number, chord):
        self.sequence_number = sequence_number
        # chord is an instance of the Chord class
        self.chord = chord

    def __str__(self):
        return(f"{self.sequence_number},{self.string},{self.fret}")
    
    def __eq__(self, other):
        if not type(other) == type(self):
            return False

INVERTED_TAB_MAP = {		
        "(String 7, fret -2)" : "A1",
		"(String 7, fret -1)" : "A#1",
		"(String 7, fret 0)" : "B1",
		"(String 6, fret -4)" : "C2",
		"(String 7, fret 1)" : "C2",
		"(String 6, fret -3)" : "Db2",
		"(String 7, fret 2)" : "Db2",
		"(String 6, fret -2)" : "D2",
		"(String 7, fret 3)" : "D2",
		"(String 6, fret -1)" : "Eb2",
		"(String 7, fret 4)" : "Eb2",
		"(String 6, fret 0)" : "E2",
		"(String 7, fret 5)" : "E2",
		"(String 6, fret 1)" : "F2",
		"(String 6, fret 2)" : "Gb2",
		"(String 6, fret 3)" : "G2",
		"(String 6, fret 4)" : "Ab2",
		"(String 6, fret 5)" : "A2",
		"(String 5, fret 0)" : "A2",
		"(String 6, fret 6)" : "Bb2",
		"(String 5, fret 1)" : "Bb2",
		"(String 6, fret 7)" : "B2",
		"(String 5, fret 2)" : "B2",
		"(String 6, fret 8)" : "C3",
		"(String 5, fret 3)" : "C3",
		"(String 6, fret 9)" : "Db3",
		"(String 5, fret 4)" : "Db3",
		"(String 6, fret 10)" : "D3",
		"(String 5, fret 5)" : "D3",
		"(String 4, fret 0)" : "D3",
		"(String 6, fret 11)" : "Eb3",
		"(String 5, fret 6)" : "Eb3",
		"(String 4, fret 1)" : "Eb3",
		"(String 5, fret 7)" : "E3",
		"(String 6, fret 12)" : "E3",
		"(String 4, fret 2)" : "E3",
		"(String 6, fret 13)" : "F3",
		"(String 5, fret 8)" : "F3",
		"(String 4, fret 3)" : "F3",
		"(String 6, fret 14)" : "Gb3",
		"(String 5, fret 9)" : "Gb3",
		"(String 4, fret 4)" : "Gb3",
		"(String 6, fret 15)" : "G3",
		"(String 5, fret 10)" : "G3",
		"(String 4, fret 5)" : "G3",
		"(String 3, fret 0)" : "G3",
		"(String 6, fret 16)" : "Ab3",
		"(String 5, fret 11)" : "Ab3",
		"(String 4, fret 6)" : "Ab3",
		"(String 3, fret 1)" : "Ab3",
		"(String 6, fret 17)" : "A3",
		"(String 5, fret 12)" : "A3",
		"(String 4, fret 7)" : "A3",
		"(String 3, fret 2)" : "A3",
		"(String 6, fret 18)" : "Bb3",
		"(String 5, fret 13)" : "Bb3",
		"(String 4, fret 8)" : "Bb3",
		"(String 3, fret 3)" : "Bb3",
		"(String 6, fret 19)" : "B3",
		"(String 5, fret 14)" : "B3",
		"(String 4, fret 9)" : "B3)",
		"(String 3, fret 4)" : "B3",
		"(String 2, fret 0)" : "B3",
		"(String 6, fret 20)" : "C4",
		"(String 5, fret 15)" : "C4",
		"(String 4, fret 10)" : "C4",
		"(String 3, fret 5)" : "C4",
		"(String 2, fret 1)" : "C4",
		"(String 6, fret 21)" : "Db4",
		"(String 5, fret 16)" : "Db4",
		"(String 4, fret 11)" : "Db4",
		"(String 3, fret 6)" : "Db4",
		"(String 2, fret 2)" : "Db4",
		"(String 6, fret 22)" : "D4",
		"(String 5, fret 17)" : "D4",
		"(String 4, fret 12)" : "D4",
		"(String 3, fret 7)" : "D4",
		"(String 2, fret 3)" : "D4",
		"(String 6, fret 23)" : "Eb4",
		"(String 5, fret 18)" : "Eb4",
		"(String 4, fret 13)" : "Eb4",
		"(String 3, fret 8)" : "Eb4",
		"(String 2, fret 4)" : "Eb4",
		"(String 6, fret 24)" : "E4",
		"(String 5, fret 19)" : "E4",
		"(String 4, fret 14)" : "E4",
		"(String 3, fret 9)" : "E4",
		"(String 2, fret 5)" : "E4",
		"(String 1, fret 0)" : "E4",
		"(String 5, fret 20)" : "F4",
		"(String 4, fret 15)" : "F4",
		"(String 3, fret 10)" : "F4",
		"(String 2, fret 6)" : "F4",
		"(String 1, fret 1)" : "F4",
		"(String 5, fret 21)" : "Gb4",
		"(String 4, fret 16)" : "Gb4",
		"(String 3, fret 11)" : "Gb4",
		"(String 2, fret 7)" : "Gb4",
		"(String 1, fret 2)" : "Gb4",
		"(String 5, fret 22)" : "G4",
		"(String 4, fret 17)" : "G4",
		"(String 3, fret 12)" : "G4",
		"(String 2, fret 8)" : "G4",
		"(String 1, fret 3)" : "G4",
		"(String 5, fret 23)" : "Ab4",
		"(String 4, fret 18)" : "Ab4",
		"(String 3, fret 13)" : "Ab4",
		"(String 2, fret 9)" : "Ab4",
		"(String 1, fret 4)" : "Ab4",
		"(String 5, fret 24)" : "A4",
		"(String 4, fret 19)" : "A4",
		"(String 3, fret 14)" : "A4",
		"(String 2, fret 10)" : "A4",
		"(String 1, fret 5)" : "A4",
		"(String 4, fret 20)" : "Bb4",
		"(String 3, fret 15)" : "Bb4",
		"(String 2, fret 11)" : "Bb4",
		"(String 1, fret 6)" : "Bb4",
		"(String 4, fret 21)" : "B4",
		"(String 3, fret 16)" : "B4",
		"(String 2, fret 12)" : "B4",
		"(String 1, fret 7)" : "B4",
		"(String 4, fret 22)" : "C5",
		"(String 3, fret 17)" : "C5",
		"(String 2, fret 13)" : "C5",
		"(String 1, fret 8)" : "C5",
		"(String 4, fret 23)" : "Db5",
		"(String 3, fret 18)" : "Db5",
		"(String 2, fret 14)" : "Db5",
		"(String 1, fret 9)" : "Db5",
		"(String 4, fret 24)" : "D5",
		"(String 3, fret 19)" : "D5",
		"(String 2, fret 15)" : "D5",
		"(String 1, fret 10)" : "D5",
		"(String 3, fret 20)" : "Eb5",
		"(String 2, fret 16)" : "Eb5",
		"(String 1, fret 11)" : "Eb5",
		"(String 3, fret 21)" : "E5",
		"(String 2, fret 17)" : "E5",
		"(String 1, fret 12)" : "E5",
		"(String 3, fret 22)" : "F5",
		"(String 2, fret 18)" : "F5",
		"(String 1, fret 13)" : "F5",
		"(String 3, fret 23)" : "Gb5",
		"(String 2, fret 19)" : "Gb5",
		"(String 1, fret 14)" : "Gb5",
		"(String 3, fret 24)" : "G5",
		"(String 2, fret 20)" : "G5",
		"(String 1, fret 15)" : "G5",
		"(String 2, fret 21)" : "Ab5",
		"(String 1, fret 16)" : "Ab5",
		"(String 2, fret 22)" : "A5",
		"(String 1, fret 17)" : "A5",
		"(String 2, fret 23)" : "Bb5",
		"(String 1, fret 18)" : "Bb5",
		"(String 2, fret 24)" : "B5",
		"(String 1, fret 19)" : "B5",
		"(String 1, fret 20)" : "C6",
		"(String 1, fret 21)" : "Db6",
		"(String 1, fret 22)" : "D6",
		"(String 1, fret 23)" : "Eb6",
		"(String 1, fret 24)" : "E6"
}

def get_file_contents(file_name):
    """
    opens a file and returns a list of strings where each string
    is a line in the file

    keyword arguments
    -----------------
    file_name -- string corresponding to the file to be read
    """
    file_instance = open(file_name, "r")
    file_contents = file_instance.readlines()
    file_instance.close()
    return(file_contents)

def separate_open_notes_from_fret_positions(file_contents):
    """
    returns a list of lists where each list is the result of splitting
    a string by the | character. For a tab, this means that index 0 is
    the open note corresponding to that string and index 1 is the string
    representation of the frets to be played on that string

    keyword arguments
    -----------------
    file_contents -- a list of strings
    """
    modified_list = []
    
    # adds contents of file_contents to modified_list as lists, 
    # where the 1st element of any given list is always the note
    # an openly-played guitar string corresponds to, and the 2nd element
    # of any list is always the string of frets to be played on that
    # guitar string.
    for x in range(len(file_contents)):
        # ignore completely blank lines
        if file_contents[x] == "\n":
            continue
        
        # tabs always say the note name, then have a | character
        # followed by the frets to be played. 
        # therefore, if you split by the | character, index 0
        # is the note corresponding to that string when played open (no frets)
        # and index 1 is the string representation of the frets to be played
        split_contents = file_contents[x].split("|")
        modified_list.append(split_contents)
    return(modified_list)

def get_unprocessed_tab_dictionary(modified_list):
    """
    returns a dictionary that maps a note (corresponding to the open strings on
    a guitar) to a a string of frets to be played on that string.
    """
    unprocessed_tab_dictionary = dict()

    # 1. get the open-string notes and frets to be played on said string
    # from the modified_list
    # 2. then map them in the dictionary
    string_number = 1
    for x in range(len(modified_list)):
        # index 0 is always the open-string note in modified_list
        # (see separate_open_notes_from_fret_positions() method)
        open_note = modified_list[x][0]
        
        # need to couple the open note with the string number, because it is possible to have a tuning like
        # DADGBE -- in this case, D will be added twice to the keys of the dictionary (no bueno)
        if string_number > 6:                                    # |
            modulus = string_number % 6                          # | this prevents strings from going 0 to 7. Keeps them
            string_number = 6 if modulus == 0 else modulus       # | in range [0, 6]

        open_note = f"{open_note}, {string_number}"
        string_number += 1

        # index 1 is always the string representation of frets to be played
        frets = modified_list[x][1]
        
        # if an open-string note has not yet been mapped the to
        # the dictionary, map it
        if not open_note in unprocessed_tab_dictionary.keys():
            unprocessed_tab_dictionary[open_note] = frets
        # otherwise, add to the frets being tracked by the dictionary
        else: 
            unprocessed_tab_dictionary[open_note] += frets
    return(unprocessed_tab_dictionary)

def get_tuning(tab_dictionary):
    string_open_notes = tab_dictionary.keys()
    tuning = dict()
    for element in string_open_notes:
        # the second [1] is to remove the white space that leads before the
        # number after doing the split (I have no idea why there is a space before the number)
        string_number = int(element.split(",")[1][1])
        string_note = element.split(",")[0]
        tuning[string_number] = string_note
    return(tuning)

def iterate_over_tab_dictionary_vertically(tab_dictionary):
    column = 0
    tuning = get_tuning(tab_dictionary)
    print(tuning)
    example_string = f"{tuning[1]}, 1"
    stopping_point = len(tab_dictionary[example_string])
    print(f"Stopping point is {stopping_point}")
    chords = []
    while column < stopping_point:
        # create a list of notes to put into a chord instance
        # NOTE: you cannot just create a Chord instance and then
        # use the add_note() method, and then append the chord
        # instance to the chords list, because for whatever reason
        # the chord instance will be the same one used previously,
        # resulting in a monstrous chord with 70+ notes somehow
        # being played simultaneously.
        positions = []
        
        # go through every string
        for string in tab_dictionary.keys():
            print(f"string is: {string}")
            value = tab_dictionary[string][column]
            if value in ["p", "/", "h", "-", "\n", "x"]:
                print(f"detected \"{value}\" -- ignoring string {string} for column {column}")
                continue
            string_number = int(string.split(",")[1])
            positions.append(FretboardPosition(string_number, int(value)))
            print(f"Created fretboardPosition {str(FretboardPosition(string_number, int(value)))}")
            print(f"added value {value} to chord {positions}")
        
        if len(positions) > 0:
            notes = [INVERTED_TAB_MAP[str(position)] for position in positions]
            chords.append(Chord(notes))
        
        column += 1
        print(f"column is now {column}")
    return(chords)

def write_chords_to_file(file_name, chords) -> None:
    file_handle = open(file_name, "w")
    # the format of the file will be such that each line
    # in the file is a chord. Therefore a file containing only 3
    # chords may look as such (also note that a chord can be just a single
    # note in this context):
    # E2 B2 E3
    # E2 
    # G2
    for chord in chords:
        print(chord)
        line = " ".join(chord.notes)
        file_handle.write(f"{line}\n")
    file_handle.close()

if len(argv) < 2:
    exit()

file_contents = get_file_contents(argv[1])

preprocessed_file_contents = separate_open_notes_from_fret_positions(file_contents)

unprocessed_tab_dictionary = get_unprocessed_tab_dictionary(preprocessed_file_contents)

for key in unprocessed_tab_dictionary.keys():
    print(f"{key}: {unprocessed_tab_dictionary[key]}")

chords = iterate_over_tab_dictionary_vertically(unprocessed_tab_dictionary)

for chord in chords:
    print(f"{chord}\n\n")

write_chords_to_file(f"notes_for_{argv[1]}", chords)
