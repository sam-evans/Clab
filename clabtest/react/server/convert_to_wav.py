# David Jara
# 02-15-2023
# Description: CLI utility to convert audio files to wav files.
# Reason: transcriber tool only works on wav files. To expand compatability,
#         do not change transcriber (hard) ー just make utility to convert
#         input into accepted file type.
# Notes: You must have ffmpeg installed on your system to work. 
#        - you can get ffmpeg here: https://www.gyan.dev/ffmpeg/builds/
#        - use a package manager:
#           - sudo apt install ffmpeg
#           - winget install gyan.ffmpeg
#           - choco install ffmpeg (requires admin)
from sys import argv
import subprocess


argc = len(argv)

def yield_extension(file: str):
    split_file = file.split(".")
    extension = split_file[len(split_file)-1]
    return(extension)

def yield_file_name(file: str):
    split_file = file.split(".")
    file_name = split_file[0]
    return(file_name)

ACCEPTABLE_EXTENSIONS = ["mp3", "ogg", "flac", "wma", "m4a", "aac", "aiff"
                         "alac"]

if argc > 1:
    for arg in argv[1:]:
        extension = yield_extension(arg)
        # do not convert if not an audio file
        if extension in ACCEPTABLE_EXTENSIONS:
            new_name = f"{yield_file_name(arg)}.wav"
            # use ffmpeg to convert the audio file to wav
            # so that it can be used by the transcriber
            converted = subprocess.call(["ffmpeg", "-i", arg, new_name])
            
            
    
    
