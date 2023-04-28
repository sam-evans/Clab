from tab_generator import TAB_MAP, Note, parse_transcriber_note, determine_tuning
from sys import argv
import copy

NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

def get_notes_between(note1, note2, direction = "up"):
    if(note1 == note2):
        return([])
    else:
        notes = []
        note1_index = NOTES.index(note1)
        note2_index = NOTES.index(note2)
        if note1_index < note2_index:
            if direction == "up":
                for note in NOTES[note1_index+1 : note2_index]:
                    notes.append(note)
            else:
                for x in range(note2_index - 1, note1_index, -1):
                    notes.append(NOTES[x])
        return(notes)

def generate_E_standard():
    tunings_map = dict()
    tunings_map["E standard"] = []
    for x in range(0, 5):
        tunings_map["E standard"].append(Note("E", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("F", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("F#", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("G", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("G#", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("A", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("A#", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("B", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("C", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("C#", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("D", x))
    
    for x in range(0, 4):
        tunings_map["E standard"].append(Note("D#", x))
    
    return(tunings_map)
        
     
                
def generate_tunings_map():
    tunings_map = generate_E_standard()
    
    # add Eb Standard
    e_flat_standard_notes = copy.copy(tunings_map["E standard"])
    e_flat_standard_notes.remove(Note("E", 4))
    e_flat_standard_notes.append(Note("D#", -1))
    e_flat_standard_notes.append(Note("Eb", -1))
    tunings_map["Eb standard"] = e_flat_standard_notes
    
    # add Drop D
    drop_d_notes = copy.copy(tunings_map["E standard"])
    drop_d_notes.append(Note("D", -1))
    drop_d_notes.append(Note("D#", -1))
    drop_d_notes.append(Note("Eb", -1)) 
    tunings_map["Drop D"] = drop_d_notes
   
    # add D standard
    d_standard_notes = tunings_map["Eb standard"]
    d_standard_notes.remove(Note("D#", 3))
    d_standard_notes.append(Note("D", -1))
    tunings_map["D standard"] = d_standard_notes
    
    # add C# standard
    c_sharp_standard_notes = tunings_map["D standard"]
    c_sharp_standard_notes.remove(Note("D", 3))
    c_sharp_standard_notes.append(Note("C#", -1))
    tunings_map["C# standard"] = c_sharp_standard_notes
    
    # add Drop C
    drop_c_notes = tunings_map["D standard"]
    drop_c_notes.append(Note("C", -1))
    drop_c_notes.append(Note("C#", -1))
    tunings_map["Drop C"] = drop_c_notes
    
    # add C standard
    c_standard_notes = tunings_map["C# standard"]
    c_standard_notes.remove(Note("C#", 3))
    c_standard_notes.append(Note("C", -1))
    tunings_map["C standard"] = c_standard_notes
    
    # add Drop B
    drop_b_notes = tunings_map["C standard"]
    drop_b_notes.append(Note("B", -1))
    tunings_map["Drop B"] = drop_b_notes
    
    # add B standard -- start of where guitar is now 7 string
    b_standard_notes = [Note("B", -1), Note("C", -1), Note("C#", -1), Note("D", -1), Note("D#", -1)]
    # B standard is just E standard, but with a 7th string tuned to B
    # this means that B standard simply adds B, C, C#, D, and D# as playable notes
    # you can view it as extending E standard (which is why 7 string guitars are called
    # "extended range" guitars
    b_standard_notes = b_standard_notes + copy.copy(tunings_map["E standard"])
    tunings_map["B standard"] = b_standard_notes 
    
    # add drop A
    drop_a_notes = tunings_map["B standard"]
    drop_a_notes.append(Note("A", -1))
    drop_a_notes.append(Note("A#", -1))
    tunings_map["Drop A"] = drop_a_notes
    
    return(tunings_map)

def read_notes(filename: str):
    """
    reads the notes from 
    
    keywords arguments
    filename -- the name/path of the file that contains the notes
                read from the transcriber application.
    """
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for x in range(0, len(lines)):
        lines[x] = lines[x][:len(lines[x])-1]
    notes = []
    for line in lines:
        split_line = line.split()
        for note in split_line:
            notes.append(note)
    return(notes)

tunings = generate_tunings_map()
for tuning in tunings:
    print(f"{tuning}: ")
    for note in tunings[tuning]:
        print(f"\t{str(note)}")
        
transcriber_notes = read_notes(argv[1])
notes = []
for transcriber_note in transcriber_notes:
    note = parse_transcriber_note(transcriber_note)
    notes.append(note)
for note in notes:
    print(str(note))
print("Notes in E standard:")
for note in tunings["E standard"]:
    print(str(note))
 
print(Note("D#", -1) in tunings["E standard"])    
tuning = determine_tuning(notes, tunings)
print(f"The tuning of the song is: {tuning}")