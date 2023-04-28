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

from music21 import note, chord, stream, converter
from sys import argv

def read_chords(filename: str):
    """
    reads the 
    
    keywords arguments
    filename -- the name/path of the file that contains the notes
                read from the transcriber application.
    """
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    for x in range(0, len(lines)):
        # remove newline char at the end of each line
        lines[x].replace("\n", "")
    
    # create all the chord instances
    # ------------------------------------------------------------
    # the chord constructor takes either a space delimited string
    # or a list of strings representing the notes to be played
    # for example 'E2 G2 A2' or equivalently ['E2', 'G2', 'A2']
    # each line should already be space delimited, so we can
    # just give the lines outright to the chord constructor
    chords = [chord.Chord(line) for line in lines]
    
    return(chords)

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
    # get the chords in a single list
    chords = read_chords(argv[1])
     
    # STREAM holds the notes on the sheet music
    STREAM = stream.Stream()
    
    # go through every chord and add it to the stream
    for chord in chords:
        STREAM.append(chord)
    STREAM.show()
