# David Jara
# Feb 28 2023
# Description: small application that takes a sequence of notes
# ──────────── from a file and puts them on sheet music.
#
# Purpose: to generate, in addition to guitar tabs, sheet music
# ──────── for the ease of use of our audience and also to expand
#          our audience beyond just guitar players.
# Notes:
# 1. download music21 with pip install music21
# 2. run python -m music21.configure
# 3. step 2 will prompt you to download musescore

from music21 import note, stream, converter, environment
from sys import argv

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

def generate_output_filename(input_name: str):
    split_name = input_name.split(".")
    split_base_name = split_name[:len(split_name)-1]
    base_name = ""
    for part in split_base_name:
        base_name += part
    
    # if this character is at the start of the
    # input file name, it will not be able to
    # create the output file. "Error: access denied"
    if base_name[0] == "\\":
        base_name = base_name[1:]
    return(base_name)

argc = len(argv)
# if a file to be read is supplied

if argc > 1:
    # get the notes in a single list
    input_notes = read_notes(argv[1])
    
    # STREAM holds the notes on the sheet music
    STREAM = stream.Stream()
    
    # go through every note and add it to the stream
    for input_note in input_notes:
        STREAM.append(note.Note(input_note))
    STREAM.show("musicxml.png")

    
