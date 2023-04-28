from sys import argv
from snippets import Tree
from tab_generator import FretboardPosition

if len(argv) < 2:
    print("Please provide a .tree file to read")
    exit()

# the name of the .tree file tells you the note to be played
# and the fretboard position
# for example E2-6-0 is the Decision Tree for:
#   Note E2 played on the 6th string, on the open fret
def parse_file_name(file_name: str) -> dict:
    split_file_name = file_name.split("-")
    note_name = split_file_name[0]
    string_number = split_file_name[1]
    fret_number = split_file_name[2]
    return(
        {
            "note"   : note_name,
            "string" : int(string_number)
            "fret"   : int(fret_number)
        }
    )

def get_file_contents(file_name: str):
    file_handle = open(file_name, "r")
    file_contents = file_handle.readlines()
    file_handle.close()
    # remove the \n characters
    file_contents = [line.replace("\n", "") for line in file_contents]
    return(file_contents)

def find_last_node_at_level(nodes, level: int): 
    pass

# it will ignore the root as the nodes found will just be made
# children of the root. Nested children become children of
# children (not visible as elements of the list returned)
def read_nodes(file_name: str):
    root_node_dictionary = parse_file_name(file_name)
    root_node = Tree(
            Tree.Node(root_node_dictionary["note"],
                      root_node_dictionary["string"],
                      root_node_dictionary["fret"]
                      )
            )
    file_contents = get_file_contents(file_name)

    for line in file_contents:
        # level is needed to determine whether
        # or not a node should be added to the nodes list
        # or made a child of the previous node.
        level = line.count("\t")
        level_difference = (previous_level - level) + 1
        
        # get information to construct the node
        split_line = line.split()
        note_name = split_line[0]
        string_number = int(split_line[1])
        fret_number = int(split_line[2])
        
        # case: level 0 node (direct child of root)
        if level_difference != 0:
            pass
        # if level is 0, it goes directly as a child of the root
        if level == 0:
            root_node.insert_child(
                            Tree.Node(note_name,
                                    FretboardPosition(string_number, fret_number),
                                    root_node)
                                    )
            
        # if not a level 0 node, then it must be the child of the last node added
        else:
            raise NotImplementedError("Logic needs to be worked out for adding nested children")
        
        # probably want to do a level difference thing like
        # how you did with the HTML list generator.
            
