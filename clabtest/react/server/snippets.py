from tab_generator import FretboardPosition

class Tree:
    def __init__(self, root):
        self.root = root

    class Node:
        def __init__(self, note_value, fretboard_value, parent, children = []):
            self.value = value
            self.fretboard_value = fretboard_value
            self.parent = parent

        def has_children(self) -> bool:
            return(True if len(self.children) != 0 
                   else False)

        def __str__(self):
            return(self.value)

        def is_root(self) -> bool: 
            if self.parent == None:
                return(True)
            
            return(False)
        
        def has_child(self, child) -> bool:
            children_list_as_string = [str(child) for child in self.children]
            child_as_string = str(child)
            return(child_as_string in children_list_as_string)

        def insert_child(self, child) -> None:
            if self.has_child(child):
                return
            self.children.append(child)
        
        def __getitem__(self, item):
            split_item = item.split()
            value = split_item[0]
            fretboard_value = split_item[1]
            for child in self.children:
                if child.value == value and child.fretboard_value == fretboard_value:
                    return(child)



E2_Tree = Tree(Node("E2", FretboardPosition(6, 0), None, []))
E3_Tree = Tree(Node("E3", FretboardPosition(5, 7), None, []))

snippets = {
        
            }
