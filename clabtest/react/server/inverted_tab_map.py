import pyclip

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

def invert_dictionary(original_dictionary):
    inverted_dictionary = dict()
    for key in original_dictionary.keys():
        fretboard_positions = original_dictionary[key]
        for position in fretboard_positions:
            fretboard_position_as_string = ""

            inverted_dictionary[str(position)] = key
    return(inverted_dictionary)

inverted_tab_map = invert_dictionary(TAB_MAP)

string_representation = "INVERTED_TAB_MAP = {"
for key in inverted_tab_map.keys():
    string_representation += f"\t\t\"{key}\" : \"{inverted_tab_map[key]}\",\n"
string_representation += "}"
pyclip.copy(string_representation)
