from sys import argv
from itertools import chain
if len(argv) < 2:
    print("Please provide a file to read")
    exit()

def filter_tab_comments(element):
    """
    method to be used with filter() that removes anything that does
    not have to do with the tab information (removes all characters 
    that are not alphanumeric

    keyword arguments 
    element
    """

def get_formatted_file_contents(file_name):
    tab_map = dict()
    file_instance = open(file_name, "r")
    file_contents = file_instance.readlines()
    for x in range(len(file_contents)):
        # split the list by the | character so that you can get the
        # open note the string corresponds to, on the left
        print(file_contents[x])
        split_list = file_contents[x].split("|")
        
        # get corresponding note
        string_open_note = split_list[x][0]
        
        # get all the positions
        string_fret_positions = split_list[x][1]
        
        # remove the -'s
        string_fret_positions = string_fret_positions.split("-")
        
        # remove the leftover empty strings from previous operation
        string_fret_positions = [fret for fret in string_fret_positions if fret != '']
        
        # now the only thing left would be tab comments all the way to the right
        # or some frets might be numbers bundled with alphabetic or / characters
        # for example 7p0 or 3/6 for pull offs and slides respectively
        # we have to remove such characters
        for x in range(len(string_fret_positions)):
            for char in ["p", "h", "/"]:
                if char in string_fret_positions[x]:
                    string_fret_positions[x] = string_fret_positions[x].split(char)
        
        # now, if any of these had to be split, then we will have lists
        # in the list, and we need to flatten these
        flattened_string_fret_positions = list(chain.from_iterable(string_fret_positions))

        # map the open string to all of its notes
        tab_map[string_open_note] = flattened_string_fret_positions
    return(tab_map)

file_name = argv[1]
tab_map = get_formatted_file_contents(file_name)
