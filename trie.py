#Copy and adapter 
#from: https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1

from typing import Tuple
import linecache
from IPython.display import Markdown, display
    
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
        self.description = '-1'
        # Line where the description are
        self.line = -1
        
def add(root, word: str, description: str, line: int):
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
    node.line = line

def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    prefix = prefix.lower()
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
    return True, node.line

# This method is a copy of find_prefix() with another return.
def get_prefix(root, prefix: str) -> TrieNode:
    """
    Check and return the node of the trie
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return None
    
    prefix = prefix.lower()
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

def load_trie_from_csv(root, folder: str = "df/"):
    """
    Load all the .txt file to a root node of a trie as new words
    """
    import pandas as pd
    files =    ['A.txt','B.txt','C.txt','D.txt','E.txt',
                'F.txt','G.txt','H.txt','I.txt','J.txt',
                'K.txt','L.txt','M.txt','N.txt','O.txt',
                'P.txt','Q.txt','R.txt','S.txt','T.txt',
                'U.txt','V.txt','W.txt','X.txt','Y.txt','Z.txt']
    
    for file in files:
        
        path = folder+file
        
        df = pd.read_csv(path, sep='¨',engine='python',header=None)
        df.columns = ['Word','Descr']
       

        for line, raw in enumerate(df['Word']):
            
            word =  raw.replace('*','').lower()

            add(root, word, path, line)   

def printmd(string):
    display(Markdown(string))
    
def get_description(node: TrieNode) -> str:
    """
    Return the description text of a word with from the given node in the trie
    Still need to test with bigger files
    """


    # Return nothing if description index is invalid
    if node.description == '-1':
        return "";
    else:
        text = linecache.getline(node.description, node.line+1)
        return text.split('¨')[1]

