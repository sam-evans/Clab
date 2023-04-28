import copy
from vector import Vector

STRINGS_FOR_TUNINGS = {
    "E standard"  : {6 : "E",  5 : "A",  4 : "D",  3 : "G",  2 : "B",  1 : "e"},
    "Eb standard" : {6 : "Eb", 5 : "Ab", 4 : "Db", 3 : "Gb", 2 : "Bb", 1 : "eb"},
    "D# standard" : {6 : "Eb", 5 : "Ab", 4 : "Db", 3 : "Gb", 2 : "Bb", 1 : "eb"},
    "Drop D"      : {6 : "D",  5 : "A",  4 : "D",  3 : "G",  2 : "B",  1 : "e"},
    "D standard"  : {6 : "D",  5 : "G",  4 : "C",  3 : "F",  2 : "A",  1 : "D"},
    "Db standard" : {6 : "C#", 5 : "F#", 4 : "B",  3 : "E",  2 : "G#", 1 : "C#"},
    "C# standard" : {6 : "C#", 5 : "F#", 4 : "B",  3 : "E",  2 : "G#", 1 : "C#"},
    "Drop C"      : {6 : "C",  5 : "G",  4 : "C",  3 : "F",  2 : "A",  1 : "D"},
    "C standard"  : {6 : "C",  5 : "F",  4 : "A#", 3 : "D#", 2 : "G",  1 : "C"},
    "Drop B"      : {6 : "B",  5 : "F",  4 : "A#", 3 : "D#", 2 : "G",  1 : "C"},
    "B standard"  : {7 : "B",  6 : "E",  5 : "A",  4 : "D",  3 : "G",  2 : "B",   1 : "E"},
    "A# standard" : {7 : "A#", 6 : "D#", 5 : "G#", 4 : "C#", 3 : "F#", 2 : "A#",  1 : "D#"},
    "Drop A"      : {7 : "A",  6 : "E",  5 : "A",  4 : "D",  3 : "G",  2 : "B",   1 : "E"}
}
# list of extended tunings to forcefully filter out 
# 7th and 8 string FretboardPosition options in
# get_best_next_position() method
EXTENDED_TUNINGS = ["B standard", "Drop A"]
WHOLE_STEPS = ["A", "B", "C", "D", "E", "F", "G"]

# if tuning is found to be lower than E standard, then
# just scale the frets. In TAB_MAP, D2 is played on the -2th fret (impossible)
# until you refer to the transpose map which tells you to move up to the 0th
# fret when it detects that you are in Drop D or D standard.
transpose_map = {
    "E standard" : {
    # Key   = string number
    # value = scale amount
                    7 : 0,
                    6 : 0,
                    5 : 0,
                    4 : 0,
                    3 : 0,
                    2 : 0,
                    1 : 0
                    },
    "Eb standard" : {
                    7 : 0,
                    6 : 1,
                    5 : 1,
                    4 : 1,
                    3 : 1,
                    2 : 1,
                    1 : 1
                    },
    "Drop D" :      {
    #               To play as if in E standard
    #               when in drop D, move up 2 frets.
                    7 : 0,
                    6 : 2,
                    5 : 0,
                    4 : 0,
                    3 : 0,
                    2 : 0,
                    1 : 0
                    },
    "D standard" :  {
                    7 : 0,
                    6 : 2,
                    5 : 2,
                    4 : 2,
                    3 : 2,
                    2 : 2,
                    1 : 2
                    },
    "C# standard" : {
                    7 : 0,
                    6 : 3,
                    5 : 3,
                    4 : 3,
                    3 : 3,
                    2 : 3,
                    1 : 3
                    },
    "Drop C"      : {
                    7 : 0,
                    6 : 4,
                    5 : 2,
                    4 : 2,
                    3 : 2,
                    2 : 2,
                    1 : 2
                    },
    "C standard"  : {
                    7 : 0,
                    6 : 4,
                    5 : 4,
                    4 : 4,
                    3 : 4,
                    2 : 4,
                    1 : 4
                    }
}

class Note:
    def __init__(self, note: str, octave: int):
        self.note = note
        # E standard tuning is used as reference for octave = 0; therefore:
        # E, 0 -> open E (6th string)
        # E, -1 open E on 8th string
        # A, 0 -> open A, or 5th fret of E
        # D, 0 -> open D (4th string)
        # G, 0 -> open G (3rd string)
        # B, 0 -> open B (2nd string)
        # E, 1 -> open E (1st string)
        self.octave = octave

    def one_step_down(self):
        if self.note in WHOLE_STEPS:
            index = WHOLE_STEPS.index(self.note)
            if index != 0:
                one_step_down_note = WHOLE_STEPS[index-1]
            else:
                one_step_down_note = WHOLE_STEPS[len(WHOLE_STEPS)-1]
            new_note = Note(one_step_down_note, self.octave)
    
    def __str__(self):
        return(f"({self.note}, {self.octave})")
    
    def __eq__(self, other):
        if (self.note == other.note) and (self.octave == other.octave):
            return True
        else:
            return False

class Chord:
    def __init__(self, notes: list):
        self.notes = notes

class PowerChord(Chord):
    def __init__(self, root):
        self.notes = [root]


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

# used to keep track of what note goes where in the tab
class Term:
    def __init__(self, number: int, position):
        self.number = number
        self.position = position
    
    def __str__(self):
        return(f"Note #{self.number}: {self.position}")

class Tab_Dictionary:
    def __init__(self, dictionary, length):
        self.dictionary = dictionary
        self.length = length
    
    def __getitem__(self, item):
        if item in self.dictionary.keys():
            return(self.dictionary[item])
    
    def __contains__(self, item):
        if item in self.dictionary.keys():
            return(True)
        else:
            return(False)
    
    def __str__(self):
        output = ""
        keys = self.keys()
        for key in keys:
            output += f"String #{key}:"
            for term in self[key]:
                output += f"\n\t{term}"
            output += "\n"
        return(output)
        
    def keys(self):
        return(self.dictionary.keys())
        

# This is all the ways you can play any given note on a guitar's fretboard, under the presumption that you have a 6 string guitar with 24 frets.
# To handle other tunings, just transpose (see transpose function) from Standard E tuning.
# For example, D Standard is 1 whole step lower than E standard, so to transpose E → D, move DOWN each fretboard position by 2, except for where the fret is 0.
#                                                                   to transpose D → E, moe UP each fretboard position by 2, except for where the fret is 24.
# NOTE: the keys are now the string representations of the Note instances
# WHY?: Python was trying to match these instances and failing, though their attributes were matching, because they were not literally the same in memory.
TAB_MAP = {
        # Mappings for tunings lower than E standard.
        # To get these on a tab:
        #   1. detect tuning
        #   2. if tuning is not in E standard, apply rule to transpose frets
        #       - Example: if in D standard, transpose down 2 always
        str(Note("A", 1)) :  [FretboardPosition(7, -2)],
        str(Note("A#", 1)) : [FretboardPosition(7, -1)],
        str(Note("B", 1)) :  [FretboardPosition(7, 0)],
        str(Note("C", 2)) :  [FretboardPosition(6, -4), FretboardPosition(7, 1)], 
        str(Note("C#", 2)) : [FretboardPosition(6, -3), FretboardPosition(7, 2)], 
        str(Note("Db", 2)) : [FretboardPosition(6, -3), FretboardPosition(7, 2)], 
        str(Note("D", 2)) :  [FretboardPosition(6, -2), FretboardPosition(7, 3)], 
        str(Note("D#", 2)) : [FretboardPosition(6, -1), FretboardPosition(7, 4)],
        str(Note("Eb", 2)) : [FretboardPosition(6, -1), FretboardPosition(7, 4)],
        # E standard notes
        str(Note("E", 2)) :  [FretboardPosition(6, 0), FretboardPosition(7, 5)], 
        str(Note("F", 2)) :  [FretboardPosition(6, 1)],
        str(Note("F#", 2)) : [FretboardPosition(6, 2)],
        str(Note("Gb", 2)) : [FretboardPosition(6, 2)],
        str(Note("G", 2)) :  [FretboardPosition(6, 3)],
        str(Note("G#", 2)) : [FretboardPosition(6, 4)],
        str(Note("Ab", 2)) : [FretboardPosition(6, 4)],
        str(Note("A", 2)) :  [FretboardPosition(6, 5), FretboardPosition(5, 0)],
        str(Note("A#", 2)) : [FretboardPosition(6, 6), FretboardPosition(5, 1)],
        str(Note("Bb", 2)) : [FretboardPosition(6, 6), FretboardPosition(5, 1)],
        str(Note("B", 2)) :  [FretboardPosition(6, 7), FretboardPosition(5, 2)],
        str(Note("C", 3)) :  [FretboardPosition(6, 8), FretboardPosition(5, 3)],
        str(Note("C#", 3)) : [FretboardPosition(6, 9), FretboardPosition(5, 4)],
        str(Note("Db", 3)) : [FretboardPosition(6, 9), FretboardPosition(5, 4)],
        str(Note("D", 3)) :  [FretboardPosition(6, 10), FretboardPosition(5, 5), FretboardPosition(4, 0)],
        str(Note("D#", 3)) : [FretboardPosition(6, 11), FretboardPosition(5, 6), FretboardPosition(4, 1)],
        str(Note("Eb", 3)) : [FretboardPosition(6, 11), FretboardPosition(5, 6), FretboardPosition(4, 1)],
        
        
        # One octave up Low E String                A String                  D String                  G String                  B String                 High E String
        str(Note("E", 3)) :  [FretboardPosition(5, 7),  FretboardPosition(6, 12),  FretboardPosition(4, 2)],
        str(Note("F", 3)) :  [FretboardPosition(6, 13), FretboardPosition(5, 8),  FretboardPosition(4, 3)],
        str(Note("F#", 3)) : [FretboardPosition(6, 14), FretboardPosition(5, 9),  FretboardPosition(4, 4)],
        str(Note("Gb", 3)) : [FretboardPosition(6, 14), FretboardPosition(5, 9),  FretboardPosition(4, 4)],
        str(Note("G", 3)) :  [FretboardPosition(6, 15), FretboardPosition(5, 10), FretboardPosition(4, 5),  FretboardPosition(3, 0)], 
        str(Note("G#", 3)) : [FretboardPosition(6, 16), FretboardPosition(5, 11), FretboardPosition(4, 6),  FretboardPosition(3, 1)],
        str(Note("Ab", 3)) : [FretboardPosition(6, 16), FretboardPosition(5, 11), FretboardPosition(4, 6),  FretboardPosition(3, 1)],
        str(Note("A", 3)) :  [FretboardPosition(6, 17), FretboardPosition(5, 12), FretboardPosition(4, 7),  FretboardPosition(3, 2)],
        str(Note("A#", 3)) : [FretboardPosition(6, 18), FretboardPosition(5, 13), FretboardPosition(4, 8),  FretboardPosition(3, 3)],
        str(Note("Bb", 3)) : [FretboardPosition(6, 18), FretboardPosition(5, 13), FretboardPosition(4, 8),  FretboardPosition(3, 3)],
        str(Note("B", 3)) :  [FretboardPosition(6, 19), FretboardPosition(5, 14), FretboardPosition(4, 9),  FretboardPosition(3, 4), FretboardPosition(2, 0)],
        str(Note("C", 4)) :  [FretboardPosition(6, 20), FretboardPosition(5, 15), FretboardPosition(4, 10), FretboardPosition(3, 5), FretboardPosition(2, 1)],
        str(Note("C#", 4)) : [FretboardPosition(6, 21), FretboardPosition(5, 16), FretboardPosition(4, 11), FretboardPosition(3, 6), FretboardPosition(2, 2)],
        str(Note("Db", 4)) : [FretboardPosition(6, 21), FretboardPosition(5, 16), FretboardPosition(4, 11), FretboardPosition(3, 6), FretboardPosition(2, 2)],
        str(Note("D", 4)) :  [FretboardPosition(6, 22), FretboardPosition(5, 17), FretboardPosition(4, 12), FretboardPosition(3, 7), FretboardPosition(2, 3)],
        str(Note("D#", 4)) : [FretboardPosition(6, 23), FretboardPosition(5, 18), FretboardPosition(4, 13), FretboardPosition(3, 8), FretboardPosition(2, 4)],
        str(Note("Eb", 4)) : [FretboardPosition(6, 23), FretboardPosition(5, 18), FretboardPosition(4, 13), FretboardPosition(3, 8), FretboardPosition(2, 4)],
        
        # Two octaves up
        str(Note("E", 4)) :  [FretboardPosition(6, 24), FretboardPosition(5, 19), FretboardPosition(4, 14), FretboardPosition(3, 9), FretboardPosition(2, 5), FretboardPosition(1, 0)],
        str(Note("F", 4)) :  [                          FretboardPosition(5, 20), FretboardPosition(4, 15), FretboardPosition(3, 10), FretboardPosition(2, 6), FretboardPosition(1, 1)],
        str(Note("F#", 4)) : [                          FretboardPosition(5, 21), FretboardPosition(4, 16), FretboardPosition(3, 11), FretboardPosition(2, 7), FretboardPosition(1, 2)],
        str(Note("Gb", 4)) : [                          FretboardPosition(5, 21), FretboardPosition(4, 16), FretboardPosition(3, 11), FretboardPosition(2, 7), FretboardPosition(1, 2)],
        str(Note("G", 4)) :  [                          FretboardPosition(5, 22), FretboardPosition(4, 17), FretboardPosition(3, 12), FretboardPosition(2, 8), FretboardPosition(1, 3)],
        str(Note("G#", 4)) : [                          FretboardPosition(5, 23), FretboardPosition(4, 18), FretboardPosition(3, 13), FretboardPosition(2, 9), FretboardPosition(1, 4)],
        str(Note("Ab", 4)) : [                          FretboardPosition(5, 23), FretboardPosition(4, 18), FretboardPosition(3, 13), FretboardPosition(2, 9), FretboardPosition(1, 4)],
        str(Note("A", 4)) :  [                          FretboardPosition(5, 24), FretboardPosition(4, 19), FretboardPosition(3, 14), FretboardPosition(2, 10), FretboardPosition(1, 5)],
        str(Note("A#", 4)) : [                                                    FretboardPosition(4, 20), FretboardPosition(3, 15), FretboardPosition(2, 11), FretboardPosition(1, 6)],
        str(Note("Bb", 4)) : [                                                    FretboardPosition(4, 20), FretboardPosition(3, 15), FretboardPosition(2, 11), FretboardPosition(1, 6)],
        str(Note("B", 4)) :  [                                                    FretboardPosition(4, 21), FretboardPosition(3, 16), FretboardPosition(2, 12), FretboardPosition(1, 7)],
        str(Note("C", 5)) :  [                                                    FretboardPosition(4, 22), FretboardPosition(3, 17), FretboardPosition(2, 13), FretboardPosition(1, 8)],
        str(Note("C#", 5)) : [                                                    FretboardPosition(4, 23), FretboardPosition(3, 18), FretboardPosition(2, 14), FretboardPosition(1, 9)],
        str(Note("Db", 5)) : [                                                    FretboardPosition(4, 23), FretboardPosition(3, 18), FretboardPosition(2, 14), FretboardPosition(1, 9)],
        str(Note("D", 5)) :  [                                                    FretboardPosition(4, 24), FretboardPosition(3, 19), FretboardPosition(2, 15), FretboardPosition(1, 10)],
        str(Note("D#", 5)) : [                                                                              FretboardPosition(3, 20), FretboardPosition(2, 16), FretboardPosition(1, 11)],
        str(Note("Eb", 5)) : [                                                                              FretboardPosition(3, 20), FretboardPosition(2, 16), FretboardPosition(1, 11)],
        
        # Three octaves up
        str(Note("E", 5)) :  [                                                                              FretboardPosition(3, 21), FretboardPosition(2, 17), FretboardPosition(1, 12)],
        str(Note("F", 5)) :  [                                                                              FretboardPosition(3, 22), FretboardPosition(2, 18), FretboardPosition(1, 13)],
        str(Note("F#", 5)) : [                                                                              FretboardPosition(3, 23), FretboardPosition(2, 19), FretboardPosition(1, 14)],
        str(Note("Gb", 5)) : [                                                                              FretboardPosition(3, 23), FretboardPosition(2, 19), FretboardPosition(1, 14)],
        str(Note("G", 5)) :  [                                                                              FretboardPosition(3, 24), FretboardPosition(2, 20), FretboardPosition(1, 15)],
        str(Note("G#", 5)) : [                                                                                                        FretboardPosition(2, 21), FretboardPosition(1, 16)],
        str(Note("Ab", 5)) : [                                                                                                        FretboardPosition(2, 21), FretboardPosition(1, 16)],
        str(Note("A", 5)) :  [                                                                                                        FretboardPosition(2, 22), FretboardPosition(1, 17)],
        str(Note("A#", 5)) : [                                                                                                        FretboardPosition(2, 23), FretboardPosition(1, 18)],
        str(Note("Bb", 5)) : [                                                                                                        FretboardPosition(2, 23), FretboardPosition(1, 18)],
        str(Note("B", 5)) :  [                                                                                                        FretboardPosition(2, 24), FretboardPosition(1, 19)],
        str(Note("C", 6)) :  [                                                                                                                                  FretboardPosition(1, 20)],
        str(Note("C#", 6)) : [                                                                                                                                  FretboardPosition(1, 21)],
        str(Note("Db", 6)) : [                                                                                                                                  FretboardPosition(1, 21)],
        str(Note("D", 6)) :  [                                                                                                                                  FretboardPosition(1, 22)],
        str(Note("D#", 6)) : [                                                                                                                                  FretboardPosition(1, 23)],
        str(Note("Eb", 6)) : [                                                                                                                                  FretboardPosition(1, 23)],
        
        # Four Octaves up
        str(Note("E", 6)) :  [                                                                                                                                  FretboardPosition(1, 24)]
    }

# lookup table to be referenced by get_best_next_position() method
# to increase performance by not having to check as many if-statements
# if the best next position calculation has already been made
LOOKUP_TABLE = dict()

TUNINGS = {
        # NOTE: 7 and 8 string guitar tunings can be created by simply appending extended range to existing 6 string tuning; for example, B standard (7 string) = ["B"] + TUNINGS["E standard"] 

        # 6 String standard tunings
        "E standard": ["E", "A", "D", "G", "B", "E"],
        "Eb standard" : ["Eb", "Ab", "Db", "Gb", "Bb", "Eb"], 
        "Drop D": ["D", "A", "D", "G", "B", "E"],
        
        "D standard" : ["D", "G", "C", "F", "A", "D"],
        "C# standard": ["C#", "F#", "B", "E", "G#", "C#"],
        "Drop C#": ["C#", "G#", "C#", "F#", "A#", "D#"],
        "Drop C": ["C", "G", "C", "F", "A", "D"],
        
        "C standard" : ["C", "F", "A#", "D#", "G", "C"],
        "Drop B": ["B", "F#", "B", "E", "G#", "C#"],
        "B standard" : ["B", "E", "A", "D", "G", "B", "E"],
        
        "Drop A": ["A", "E", "A", "D", "G", "B"],
        "A standard" : ["A", "D", "G", "C", "E", "A"],
        }

NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
CIRCLE_OF_FIFTHS = [
                   "C", 
                   "G", 
                   "D", 
                   "A", 
                   "E", 
                   "B", 
                   "Gb", 
                   "Db", 
                   "Ab", 
                   "Eb", 
                   "Bb", 
                   "F"]

def get_vertical_distance(position1, position2):
    """
    Returns the vertical distance (how many strings away) this note is from another note on the fretboard. 
    Useful for determining whether or not it is worth it to jump X amount of strings to decrease
    horizontal movement space, or to jump Y amount of strings with greater horizontal movement space,
    where X > Y.
    
    keyword arguments
    position1 -- an instance of the FretboardPosition class
    position2 -- an instance of the FretboardPosition class
    """
    if position1.string > position2.string:
        return(position1.string - position2.string)
    elif position1.string < position2.string:
        return(position2.string - position1.string)
    else:
        return(0)

def lateral_fretboard_distance(position1, position2):
    """
    Returns the lateral distance (how many frets away) this note is from another note on the fretboard. 
    Used to determine whether or not the note should be on the same string, or a different string. 
    E.g. it is extremely difficult to go from the 3rd fret to the 9th fret on the E string, so it would be better to play the 3rd fret on the E string, then the 4th fret on the A string.
    
    keyword arguments
    position1 -- an instance of the FretboardPosition class
    position2 -- an instance of the FretboardPosition class
    """
    if position1.fret > position2.fret:
        return(position1.fret - position2.fret)
    elif position1.fret < position2.fret:
        return(position2.fret - position1.fret)
    else:
        return(0)

def get_same_string_options(note: str, string: int):
    """
    Returns a list of FretboardPosition instances, where each instance has the same string attribute as the string argument.
    
    keyword arguments
    note -- string representation of a note instance
    string -- integer corresponding to one of the 6 strings
    """
    keys = TAB_MAP.keys()
    if note in keys:
        options = TAB_MAP[note]
    else:
        return([])
    same_string_options = []
    for option in options:
        if option.string == string:
            same_string_options.append(option)
    return(same_string_options)

def get_open_option(note: str):
    """
    Given a note, returns a FretboardPosition instance if it can be played on one of the strings openly (0th fret)
    and returns None otherwise
    
    keyword arguments
    note -- string representation of a Note instance.
    """
    keys = TAB_MAP.keys()
    
    # case: invalid note passed
    if not note in keys:
        return(None)
    
    # if an option is found that is played on the 0th fret, return that option
    options = TAB_MAP[note]
    for option in options:
        if option.fret == 0:
            return(option)
    
    # otherwise, return None
    return(None)

def insert_into_lookup_table(previous, options, choice):
    LOOKUP_TABLE[str(previous)] = {str(options) : choice}

def get_best_next_position(previous, options, track, tuning, song = [], song_index = 0):
    """
    Greedy method for determining where to place your fingers on the fretboard given the fretboard positions corresponding to a note to be played.

    Keyword arguments
    previous   -- FretboardPosition instance corresponding to the last spot played on the fretboard.
    options    -- a list of FretboardPosition instances. Each instance corresponds to different ways to play a target note.
    track      -- the entire set of previously determined positions to play (outputs of this method)
    tuning     -- a string representing the tuning the guitar is in.
    song       -- the entire set of notes to be played
    song_index -- the index within the song argument to which the current note to be placed on the 
                  fretboard corresponds to (note corresponding to options argument)
    """
    # use lookup table to avoid unnecessary calculation
    if str(previous) in LOOKUP_TABLE.keys():
        if str(options) in LOOKUP_TABLE[str(previous)]:
            #print(f"used lookup table for\n\tprevious = {str(previous)}\n\toptions = {str([str(option) for option in options])}")
            return(LOOKUP_TABLE[str(previous)][str(options)])
    
    lateral_distances = []
    vertical_distances = []
    
    # remove all 7th and 8th string positionings when
    # playing in a 6-string tuning
    if not tuning in EXTENDED_TUNINGS:
        options = [option for option in options if not option.string in [7, 8]]
    
    # get the lateral and vertical distance of every position on the fretboard that plays the note that comes after the "previous" argument
    for option in options:
        lateral_distance = lateral_fretboard_distance(previous, option)
        vertical_distance = get_vertical_distance(previous, option)
        lateral_distances.append(lateral_distance)
        vertical_distances.append(vertical_distance)
    
    corresponding_note = get_corresponding_note(options[0]) # use [0] because it does not matter as they are all the same note
    open_option = get_open_option(str(corresponding_note))
    same_string_options = get_same_string_options(str(corresponding_note), previous.string)
        
    # if there is only one option, return that option
    if len(options) == 1:
        # add to lookup table
        insert_into_lookup_table(previous, options, options[0])
        return(options[0])
    
    # if the note can be played open (0th fret), on the same string 
    # as the previous note, play openly.
    if open_option != None:
        if previous.string == open_option.string:
            # add to lookup table
            insert_into_lookup_table(previous, options, open_option)   
            return(open_option)
    
    for option in same_string_options:
        # if you can play the note on the same string as the
        # previous note and the previous note was played openly
        # then play it on the same string, regardless of distance
        if previous.fret == 0:
            # add to lookup table
            insert_into_lookup_table(previous, options, option)
            return(option)
        
        # if previous note was not played on open string
        # then still prefer the same string, so long as it is
        # not too far away (5+ frets away)
        if lateral_fretboard_distance(previous, option) < 5:
            # add to lookup table
            insert_into_lookup_table(previous, options, option)
            return(option)
    
    # if the previously played note was played on an open string,
    # then you can be more liberal with the positioning of the next note
    # as your hand comes off the fretboard entirely.
    # The rule here is to minimize vertical distance (string skipping)
    # unless, you can skip 1 extra string to play the same note, and minimize horizontal distance
    if previous.fret == 0:
        previous_previous_note = track[len(track)-2]
        sorted_vertical_distances = vertical_distances.sort()
        minimum_vertical_distance = min(vertical_distances)
        minimum_string_skipping_position_index = vertical_distances.index(minimum_vertical_distance)
        minimum_string_skipping_position = options[minimum_string_skipping_position_index]
        # try to minimize horizontal distance by considering
        #   1. the note played before the open note
        #   2. if you do less horizontal movement relative to that
        #      note that came before the open note, by skipping 1 extra string
        if lateral_fretboard_distance(minimum_string_skipping_position, previous_previous_note) > 2:
            try:
                second_minimum_string_skipping_position_index = vertical_distances.index(sorted_vertical_distances[1])
                second_minimum_string_skipping_position = options[second_minimum_string_skipping_position_index]
                # add to lookup table
                insert_into_lookup_table(previous, options, second_minimum_string_skipping_position)
                return(second_minimum_string_skipping_position)
            except:    
                pass
        # otherwise, return the position that minimizes string skipping
        # add to lookup table
        insert_into_lookup_table(previous, options, minimum_string_skipping_position)
        return(minimum_string_skipping_position)
    
    # if none of the other heuristics apply, then
    # return the smallest distance
    smallest_distance = min(lateral_distances)
    smallest_distance_index = lateral_distances.index(smallest_distance)
    nearest = options[smallest_distance_index]
    # add to lookup table
    insert_into_lookup_table(previous, options, nearest)
    return(nearest)

# implementation using vectors for distances
def get_best_next_position_vector(previous, options, track, tuning):
    # use lookup table to avoid unnecessary calculation
    if str(previous) in LOOKUP_TABLE.keys():
        if str(options) in LOOKUP_TABLE[str(previous)]:
            #print(f"used lookup table for\n\tprevious = {str(previous)}\n\toptions = {str([str(option) for option in options])}")
            return(LOOKUP_TABLE[str(previous)][str(options)])
    
    lateral_distances = []
    vertical_distances = []
    vectors = []

    # remove all 7th and 8th string positionings when
    # playing in a 6-string tuning
    if not tuning in EXTENDED_TUNINGS:
        options = [option 
                   for option in options 
                   if not option.string in [7, 8]]
    
    # get the lateral and vertical distance of every position on the fretboard that plays the note that comes after the "previous" argument
    for option in options:
        lateral_distance = lateral_fretboard_distance(previous, option)
        vertical_distance = get_vertical_distance(previous, option)
        vectors.append(Vector(lateral_distance, vertical_distance))
        #lateral_distances.append(lateral_distance)
        #vertical_distances.append(vertical_distance)
    
    corresponding_note = get_corresponding_note(options[0]) # use [0] because it does not matter as they are all the same note
    open_option = get_open_option(str(corresponding_note))
    same_string_options = get_same_string_options(str(corresponding_note), previous.string)
        
    # if there is only one option, return that option
    if len(options) == 1:
        # add to lookup table
        insert_into_lookup_table(previous, options, options[0])
        return(options[0])
    
    # if the note can be played open (0th fret), on the same string 
    # as the previous note, play openly.
    if open_option != None:
        if previous.string == open_option.string:
            # add to lookup table
            insert_into_lookup_table(previous, options, open_option)   
            return(open_option)
    
    for option in same_string_options:
        # if you can play the note on the same string as the
        # previous note and the previous note was played openly
        # then play it on the same string, regardless of distance
        if previous.fret == 0:
            # add to lookup table
            insert_into_lookup_table(previous, options, option)
            return(option)
        
        # if previous note was not played on open string
        # then still prefer the same string, so long as it is
        # not too far away (5+ frets away)
        if lateral_fretboard_distance(previous, option) < 5:
            # add to lookup table
            insert_into_lookup_table(previous, options, option)
            return(option)
    
    # if the previously played note was played on an open string,
    # then you can be more liberal with the positioning of the next note
    # as your hand comes off the fretboard entirely.
    # The rule here is to minimize vertical distance (string skipping)
    # unless, you can skip 1 extra string to play the same note, and minimize horizontal distance
    if previous.fret == 0:
        previous_previous_note = track[len(track)-2]
        sorted_vertical_distances = vertical_distances.sort()
        minimum_vertical_distance = min(vertical_distances)
        minimum_string_skipping_position_index = vertical_distances.index(minimum_vertical_distance)
        minimum_string_skipping_position = options[minimum_string_skipping_position_index]
        # try to minimize horizontal distance by considering
        #   1. the note played before the open note
        #   2. if you do less horizontal movement relative to that
        #      note that came before the open note, by skipping 1 extra string
        if lateral_fretboard_distance(minimum_string_skipping_position, previous_previous_note) > 2:
            try:
                second_minimum_string_skipping_position_index = vertical_distances.index(sorted_vertical_distances[1])
                second_minimum_string_skipping_position = options[second_minimum_string_skipping_position_index]
                # add to lookup table
                insert_into_lookup_table(previous, options, second_minimum_string_skipping_position)
                return(second_minimum_string_skipping_position)
            except:    
                pass
        # otherwise, return the position that minimizes string skipping
        # add to lookup table
        insert_into_lookup_table(previous, options, minimum_string_skipping_position)
        return(minimum_string_skipping_position)
    
    # if none of the other heuristics apply, then
    # return the smallest distance
    smallest_distance = min(lateral_distances)
    smallest_distance_index = lateral_distances.index(smallest_distance)
    nearest = options[smallest_distance_index]
    # add to lookup table
    insert_into_lookup_table(previous, options, nearest)
    return(nearest)
           
# prototype new version that takes into account the NEXT note as well
# before assigning the current note.

def get_best_next_position_neo(previous, subsequent, options): 
    """
    Returns an instance of the FretboardPosition class corresponding to the best way to play a note, given the context of what was played before and what will be played next.
    
    keyword arguments:
    previous -- an instance of the FretboardPosition class, corresponding to the previously played note
    subsequent -- string representation of the next note to be played 
    options -- list of FretboardPosition instances corresponding to ways to play the current note
    """
    previous_lateral_distances = []
    subsequent_lateral_distances = [] # "next" was not used for the keyword, as it is a reserved word
    
    # get the lateral distance of every position on the fretboard that plays the note that comes after the "previous" argument
    for option in options:
        previous_lateral_distance = lateral_fretboard_distance(previous, option)
        previous_lateral_distances.append(previous_lateral_distance)
    #print(lateral_distances)
    
    if not subsequent in [None, ""]:
        # get the lateral distance of every position on the fretboard that plays the note that comes after the "subsequent" argument
        subsequent_options = TAB_MAP[subsequent]
        for option in subsequent_options:
            subsequent_lateral_distance = lateral_fretboard_distance(subsequent, option)
            subsequent_lateral_distances.append(lateral_distance)
    
    if (options[0].string == previous.string) and (lateral_fretboard_distance(options[0], previous) < 5):
        if subsequent != None:
            if lateral_fretboard_distance(options[0], subsequent) < 5:
                return(options[0])
    else:
        # smallest distance
        smallest_distance = min(lateral_distances)
        smallest_distance_index = lateral_distances.index(smallest_distance)
        nearest = options[smallest_distance_index]
        return(nearest)

    # filter the positions based on whether or not they are too far away (distance = 6+)
    """
    candidates = []
    for x in range(0, len(lateral_distances)):
        distance = lateral_distances[x]
        if distance <= 5:
            candidates.append(options[x])
    
    return(candidates)
    """

def notes_are_in_tuning(notes, tuning):
    """
    Determines whether or not a sequence of notes (string representation) are in 
    a tuning. Returns True or False.
    
    keyword arguments:
    notes: a list of the string representations of the note class
    tuning: a string such as "Drop D", corresponding to a tuning.
    """
    for note in notes:
        if not note in tuning:
            return(False)
    return(True)

# To determine the tuning that the song should be played in:
#   1. look at all known tunings
#   2. look at every note in the sequence
#   3. compare against tuning
#       1. if every note is in the tuning, return this tuning
#       2. otherwise, continue through the tunings
def determine_tuning(notes, tunings):
    """
    Determines the tuning the guitar should be in, based on the lowest played note.
    
    keyword arguments:
    notes -- a sequence of the string representations of note instances.
    tunings -- a dictionary corresponding to all the tunings to check (TUNINGS dictionary in
             on line 292)
    """
    decision = None
    for tuning in tunings:
        if notes_are_in_tuning(notes, tunings[tuning]):
            return(tuning)    
    return(None)
        
def determine_all_tunings(notes, tunings, accumulated = []):
    """
    Determines all the tunings in which a song can be played
    
    keyword arguments
    notes -- a sequence of the string representations of note instances.
    tunings -- a dictionary corresponding to all the tunings to check (TUNINGS dictionary in
               on line 292)
    accumulated -- all the tunings that have already been established the notes can be played in
    """
    # we do not have to check tunings that are already
    # determined to be suitable for the song
    # so just remove them from the list of tunings to check
    for tuning_to_ignore in accumulated:
        del tunings[tuning_to_ignore]
        
    for tuning in tunings: 
        # we do not have to check tunings that are already
        # determined to be suitable for the song
        # so just remove them from the list of tunings to check
        if (notes_are_in_tuning(notes, tunings[tuning])) and (not tuning in accumulated):
            accumulated.append(tuning)
    return(accumulated)
        
def transpose_fretboard_position(note, level: int):
    """
    Given a note, return the position on the fretboard on which it is played for a guitar that is tuned <level> HALF STEPS lower or higher.
    
    Keyword arguments:
    note -- an instance of the Note class
    level -- the amount of half steps to transpose up or down
    """
    positions = TAB_MAP[note]
    transposed_positions = []
    for position in positions:
        # transpose the note up/down
        transposed_note = position.fret + level
    
        # check for validity on guitar with 24 frets
        if transposed_note in range(0, 25):
            transposed_positions.append(FretboardPosition(position.string, transposed_note))
    
    return(transposed_positions)

def get_perfect_fifth(note: str):
    """
    Returns the perfect 5th of a given note. Useful for procedurally generating the list of notes to play for various chords.
    
    keyword arguments:
    note -- string representation of a note. Octave doesn't matter here, so an instance of the Note class is not necessary.
    """
    alternate_notation_map = {"A#" : "Gb",
                                "C#" : "Db",
                                "D#" : "Eb",
                                "F#" : "Gb",
                                "G#" : "Ab"
                              }
    if note in alternate_notation_map.keys():
        note = alternate_notation_map[note]
    
    index = CIRCLE_OF_FIFTHS.index(note)
    if index < len(CIRCLE_OF_FIFTHS) - 1:
        perfect_fifth = CIRCLE_OF_FIFTHS[index + 1]
    else:
        perfect_fifth = CIRCLE_OF_FIFTHS[0]
    return(perfect_fifth)
 
def get_perfect_fourth(note: str):
    """
    Returns the perfect 4th of a given note. Useful for procedurally generating the list of notes to play for various chords. Same as the get_perfect_fifth method, but it goes backwards.
    
    keyword arguments:
    note -- string representation of a note. Octave doesn't matter here, so an instance of the Note class is not necessary.
    """
    # index of the note in the 
    index = CIRCLE_OF_FIFTHS.index(note)
    if index > 0:
        perfect_fourth = CIRCLE_OF_FIFTHS[index - 1]
    else:
        perfect_fourth = CIRCLE_OF_FIFTHS[len(CIRCLE_OF_FIFTHS)-1]
    return(perfect_fourth)
       
def get_corresponding_note(position):
    """
    Gets the note instance that corresponds to a position on the fretboard. 
    
    keyword arguments
    position -- an instance of the FretboardPosition class.
    """
    keys = TAB_MAP.keys()
    for note in keys:
        positions = TAB_MAP[note]
        if position in positions:
            split_note = note.split(",")
            note_name = split_note[0][1:]
            note_octave = split_note[1]
            note_octave = note_octave[0:len(note_octave)-1]
            corresponding_note = Note(note_name, int(note_octave))
            return(corresponding_note)
           
def get_fretboard_position_octave_up(position):
    """
    Given a position on the fretboard (e.g. 4th fret on the A string), return a list of positions on the fretboard that would play the corresponding note, one octave up. Useful for determining the notes to play for a chord, given just its root.
    
    keyword arguments:
    position -- an instance of the Fretboard position class
    """
    corresponding_note = get_corresponding_note(position)
    octave_up_note = Note(corresponding_note.note, corresponding_note.octave+1)
    octave_up_positions = TAB_MAP[str(octave_up_note)]
    return(octave_up_positions)

def get_fretboard_position_octave_down(position):
    """
    Given a position on the fretboard (e.g. 4th fret on the A string), return a list of positions on the fretboard that would play the corresponding note, one octave down. Useful for determining the notes to play for a chord, given just its root.
    
    keyword arguments:
    position -- an instance of the Fretboard position class
    """
    corresponding_note = get_corresponding_note(position)
    octave_down_note = Note(corresponding_note.note, corresponding_note.octave-1)
    octave_down_positions = TAB_MAP[octave_down_note]
    return(octave_up_positions)

# you can use this with semitones = 6 to get a tritone chord, procedurally.
def get_note_x_semitones_up(note: str, semitones: int):
    """
    returns the string representation of a note that is some amount of semitones higher than the note provided.
    
    keyword arguments
    note -- string representation of any note, e.g. A#
    semitones -- how many semitones you want to go up
    """
    alternate_notation_map = {"Bb" : "A#",
                                "Db" : "C#",
                                "Eb" : "D#",
                                "Gb" : "F#",
                                "Ab" : "G#"
                              }
    if note in alternate_notation_map.keys():
        note = alternate_notation_map[note]
    index = NOTES.index(note)
    new_index = index + semitones
    if new_index >= len(NOTES):
        new_index -= len(NOTES)
    new_note = NOTES[new_index]
    return(new_note)

def get_power_chord(root):
    root_note = get_corresponding_note(root)
    root_note_perfect_fifth = get_perfect_fifth(root_note.note)
    root_note_perfect_fifth_instance = Note(root_note_perfect_fifth, root_note.octave)
    root_note_octave_up = Note(root_note.note, root_note.octave+1)
    positions = [root,
                 TAB_MAP[str(root_note_perfect_fifth_instance)],
                 TAB_MAP[str(root_note_octave_up)]
    ]
    return(positions)

def get_tritone_chord(root):
    root_note = get_corresponding_note(root)
    six_semitones_up_note = get_note_x_semitones_up(root_note.note, 6)
    six_semitones_up_note_instance = Note(six_semitones_up_note, root_note.octave)
    root_note_octave_up = Note(root_note.note, root_note.octave+1)
    print(root_note)
    print(six_semitones_up_note_instance)
    print(root_note_octave_up)
    positions = [root,
                 str(TAB_MAP[str(six_semitones_up_note_instance)][1]),
                 str(TAB_MAP[str(root_note_octave_up)][2])
    ]
    return(positions) 

# updated version -- internal note representation (Note class) is
#                    now the same as the representation from the
#                    transcriber 
def parse_transcriber_note(note: str):
    """
    Reads the string representation of notes from the transcriber app and converts it to the equivalent Note instance
    
    keyword arguments
    note -- string representation of the note as they are provided by the transcriber application
    """
    if "#" in note:
        note_name = note[0:2]
    else:
        note_name = note[0]
    
    # last character is always a number corresponding to the octave
    octave = int(note[len(note)-1]) 
    
    # open E on a EADGBe guitar is E2 in transcriber.
    # so create Note("E", 2)
    
    equivalent_note_instance = Note(note_name, octave)
    return(equivalent_note_instance)
   
def apply_scale_factor(tab_dictionary, tuning):
    """
    Corrects the positionings in a Tab_Dictionary instance so that they are
    reflective of how the song would be played in a certain tuning 
    (otherwise, the tab would show negative frets (impossible))
    """
    for string in tab_dictionary.keys():
        scale_factor = transpose_map[tuning][string]
        for fret in tab_dictionary[string]:
            fret.position += scale_factor
    return(tab_dictionary)
   
def generate_tab_dictionary(notes, tuning):
    """
    Generates an instance of the  Tab_Dictionary class, given a list of notes. The Tab_Dictionary instance associates all the notes with a sequence number by putting them in a Term instance, and then associates those notes with a string. This provides all the information needed to create a tab.
    
    keyword arguments
    notes -- a list of instances of the Note class
    """
    positions = []
    # get_best_next_position() method requires a previous note to be referenced
    # so it can determine the what the next best note to play is, but if we are
    # on the first note, then there is nothing to reference, so manually insert
    # the first note, always.
    try:
        #print(str(notes[0]))
        #debug = TAB_MAP[str(notes[0])]   # remove commented-out part later on march 26th
        #for element in debug:
            #print(str(element))
        first = TAB_MAP[str(notes[0])][0] # final [0] prefers the 6th string over others
        positions.append(first)
        previous = first
    except:
        print("No first note can be added")
    
    # for every other note, determine what position is the easiest way
    # to play the note, given the context of what was just played previously.
    # then add this to the positions list
    for x in range(1, len(notes)):
        note = notes[x]
        options = TAB_MAP[str(note)]
        
        easiest = get_best_next_position(previous, options, positions, tuning, notes, x)
        positions.append(easiest)
        previous = easiest
    
    # represent tab as a dictionary
    tab_dictionary = {
                      7 : [],
                      6 : [],
                      5 : [],
                      4 : [],
                      3 : [],
                      2 : [],
                      1 : []
                     }
    
    # if tuned to B standard, treat as a 7 string guitar
    if tuning == "B standard":
        tab_dictionary[7] = []
        
    # determines length of dictionary ahead of time, so no iterating through all keys later
    counter = 1
    
    # take each note and create a Term instance, which associates a sequence number
    # with that note. Then associate the Term with the string. Now we know what is being
    # played, when, and on what string. Boom. A tablature.
    for position in positions:
        tab_dictionary[position.string].append(Term(counter, position.fret))
        counter += 1
    
    result = Tab_Dictionary(tab_dictionary, counter)
    if tuning != "E standard":
        result = apply_scale_factor(result, tuning)
    return(result)
        
def generate_tab(tab_dictionary, tuning):
    """
    Generates and prints a tab to stdout, given a Tab_Dictionary instance.
    
    keyword arguments:
    tab_dictionary -- an instance of the Tab_Dictionary class.
    """
    
    # represent tab to be printed as a dictionary
    tab = {
           1 : [],
           2 : [],
           3 : [],
           4 : [],
           5 : [],
           6 : [],
           7 : []
          }
    
    # if tuned to B standard, treat as a 7 string guitar
    if tuning == "B standard":
        tab[7] = []
    
    counter = 1
    keys = tab_dictionary.keys()
    
    # go through every key (string)
    while counter != tab_dictionary.length:
        for key in keys:
            terms = tab_dictionary[key]
            # go through every note that is played on that string
            for term in terms:
                # if the note has the sequence number of the 
                # current note, then add it to the tab
                if term.number == counter:
                    tab[key].append(f"{term.position}-")
                    # add -'s to every other string
                    for otherkey in keys:
                        if key != otherkey:
                            tab[otherkey].append("--"*len(str(term.position))) # * len(str(position)) part makes
                            #                                                     it so stuff aligns when you put
                            #                                                     a double digit fret
                    # move onto next note in sequence
                    counter += 1
                # removing this fixed the problem with causing the tablature
                # to become misaligned as it grows longer
                #else:
                    #tab[key].append("-")
    #print(f"Counter = {counter}")
    
    # actually print the tab
    tab_string = "" 
    for key in tab:
        # aesthetic: use the tuning information and the strings_for_tunings dictionary
        #            from the tunings library to replace 6, 5, 4, ..., 1
        #            with the actual notes the open strings correspond to
        if not key in STRINGS_FOR_TUNINGS[tuning].keys():
            continue
        key_label = STRINGS_FOR_TUNINGS[tuning][key]
        tab_string += f"{key_label}|-"
        frets = tab[key]
        for fret in frets:
            tab_string += fret
        tab_string += "\n"
    return(tab_string)
