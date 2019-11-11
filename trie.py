#Copy and adapter 
#from: https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1

from typing import Tuple


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """
    
    def __init__(self, char: str):
        self.char = char
        self.children = []
        # Is it the last character of the Tree, other words, not found.
        self.is_final = False
        # How many children has associate with this Node
        self.num_children = 1
        # Is it the last character of a word.
        self.is_word = False        
        # If is a word, so must have a description and a index to be used in description file
        self.description = -1

def add(root, word: str, description: int):
    """
    Adding a word in the trie structure
    """
    node = root
    for char in word:
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.num_children += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)

            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.is_final = True
    node.is_word = True
    node.description = description

def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0

    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.num_children

# This method is a copy of find_prefix() with another return.
def get_prefix(root, prefix: str) -> TrieNode:
    """
    Check and return
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return None
    
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return None
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return node

def load_trie_from_csv(root, filename: str = "trie_data.csv"):
    """
    Load rows of a .csv file to a root node of a trie as new words
    Still need to test with bigger files
    """
    # Creates a meta-object to access the file without loading to RAM
    with open(filename) as csvfile:
        # Creates a reader to run over the rows and columns of a csv file
        readcsv = csv.reader(csvfile, delimiter = ',')
        for row in readcsv:
            word = row[0]
            # Convert string to int
            description = int(row[1])
            add(root, word, description)

def get_description(node: TrieNode, descriptionsfile: str = "trie_descriptions.csv") -> str:
    """
    Return the description text of a word with from the given node in the trie
    Still need to test with bigger files
    """
    # Return nothing if description index is invalid
    if node.description < 0:
        return "";

    # Creates a meta-object to access the file without loading to RAM
    with open(descriptionsfile) as csvfile:
        # Convert io text wrapper object to list so we can access an index. Need to test if not loads to RAM
        csvlist = list(csvfile)
        # Gets only the description we want
        description = csvlist[node.description]
        # Remove "\n" of the end of the description
        if description.endswith("\n"):
            description = description[:-2]
        return description

if __name__ == "__main__":
    root = TrieNode('*')
    
    add(root, "hackathon", 0)
    add(root, 'hack', 1)
    # Same thing reading from csv
    # load_trie_from_csv(root)

    print(find_prefix(root, 'hac'))
    print(find_prefix(root, 'hack'))
    print(find_prefix(root, 'hackathon'))
    print(find_prefix(root, 'ha'))
    print(find_prefix(root, 'hammer'))
    
    # Example of reading from csv
    node = get_prefix(root, 'hackathon')
    if node.is_final:
        print(get_description(node))
    else:
        print("Palavra não encontrada")
