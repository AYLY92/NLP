import nltk
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

#S -> N V

NONTERMINALS = """

S -> NP VP | VP | S Conj S | S P S
NP -> N | Det N | Det NP | P NP | Adj NP | Adv NP | Conj NP | N NP | N Adv
VP -> V | V NP | Adv VP | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    #raise NotImplementedError
    
    #Show the original sentence
    print("Original setence:", sentence )
    # Regex pattern to match words with at least one alphabetic character
    pattern = re.compile(".*[a-z].*")

    # Word tokenize lower-cased sentence and remove all pure non-alphabetic words
    words = nltk.word_tokenize(sentence.lower())
    #Show all tokens 
    print("All tokens:", words)
    words = [word for word in words if pattern.match(word)]
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    #raise NotImplementedError
    
    #NP is a list of all noun phrase chunks in the sentence tree
    NP = []
    parented_tree = nltk.tree.ParentedTree.convert(tree)
    
    for subtree in parented_tree.subtrees(lambda t: t.label() == 'N'):
        NP.append(subtree.parent())

    return NP


if __name__ == "__main__":
    main()
