# the name of the .tree file tells you the note to be played
# and the fretboard position
# for example E2-6-0 is the Decision Tree for:
#   Note E2 played on the 6th string, on the open fret
def parse_file_name(file_name: str) -> dict:
    split_file_name = file_name.split(".tree")
    split_file_name = split_file_name[0].split("-")
    note_name = split_file_name[0]
    string_number = split_file_name[1]
    fret_number = split_file_name[2]
    return(
        {
            "note"   : note_name,
            "string" : int(string_number),
            "fret"   : int(fret_number)
        }
    )

def parse_string_representation(representation: str) -> dict:
    print(representation)
    representation = representation.replace("\n", "")
    representation = representation.replace("\t", "")
    print(representation)
    split_representation = representation.split()
    note_name = split_representation[0]
    string_number = split_representation[1]
    fret_number = split_representation[2]
    return(
        {
            "note"   : note_name,
            "string" : int(string_number),
            "fret"   : int(fret_number)
        }
    )

def tail(sequence):
    return(sequence[len(sequence)-1])

class TreeNode:
    def __init__(self, note: str, string: int, fret: int):
        # music specific stuff
        self.note = note
        self.string = string
        self.fret = fret
        
        # tree implementation
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self
        child.id = len(self.children)
        self.children.append(child)
    
    def get_level(self):
        level = 0
        parent = self.parent
        while parent != None:
            level += 1
            parent = parent.parent
        return(level)

    def print_tree(self):
        level = self.get_level()
        indent = "\t" * level
        tree_as_string = f"{indent}{self.note} {self.string} {self.fret}\n"
        for child in self.children:
            tree_as_string += str(child)
        print(tree_as_string)
    
    def __str__(self):
        return(f"{self.note} {self.string} {self.fret}")

    def traverse(self) -> list:
        tree = [self]
        for child in self.children:
            tree += child.traverse()
        return(tree)
    
    def __contains__(self, item):
        tree_list = self.traverse()
        return(item in [str(node) for node in tree_list])

    def create_from_file(file_name):
        file_handle = open(file_name, "r")
        file_contents = file_handle.readlines()
        file_contents = [line for line in file_contents if len(line) > 1]
        file_handle.close()
        
        # create root node
        root_elements = parse_file_name(file_name)
        root = TreeNode(root_elements["note"], 
                        root_elements["string"],
                        root_elements["fret"])
        
        tree_dictionary = {
                            0 : [root]
                          }
        # create nodes
        for item in file_contents:
            level = item.count("\t") + 1
            
            elements = parse_string_representation(item)
            node = TreeNode(elements["note"],
                            elements["string"],
                            elements["fret"]
                            )

            # its parent must be the last added element for the previous level
            tail(tree_dictionary[level - 1]).add_child(node)
            
            # if this level has not been touched before, make a new list
            # for said level
            if not level in tree_dictionary.keys():
                tree_dictionary[level] = [node]
            
            # otherwise just add to level
            else:
                tree_dictionary[level].append(node)
        
        return(root)

if __name__ == "__main__":
    e3 = TreeNode("E3", 5, 7)
    f4 = TreeNode("F4", 2, 6)
    b3 = TreeNode("B3", 2, 0)
    e4 = TreeNode("E4", 2, 5)
    b3.add_child(e4)
    f4.add_child(b3)
    e3.add_child(f4)
    """
    print(e3)
    print([str(child) for child in e3.traverse()])
    print("F4 2 6" in e3)
    print("F4 1 1" in e3)
    """
    print("Begin tree read ------------------------")
    root = TreeNode.create_from_file("E2-6-0.tree")
    root.print_tree()
    print([str(node) for node in root.traverse()])
