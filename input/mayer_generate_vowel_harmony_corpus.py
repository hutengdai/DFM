from HMM import HMM, START, END
from os.path import join

import argparse

'''
A script to generate vowel harmony corpora
'''
DEFAULT_CORPUS_SIZE = 50000
DEFAULT_OUTFILE = '../corpora/vowel_harmony.txt'

def generate_corpora(corpus_size, outfile):
    '''
    corpus_size: The number of tokens.
    outfile: The file to save the corpus in
    '''
    hmm = HMM()

    BACK_VOWEL = 1
    FRONT_VOWEL = 2
    BACK_CONS = 3
    FRONT_CONS = 4

    # Add states
    hmm.add_state(BACK_VOWEL, 'Back Vowel')
    hmm.add_state(FRONT_VOWEL, 'Front Vowel')
    hmm.add_state(BACK_CONS, 'Back Consonant')
    hmm.add_state(FRONT_CONS, 'Front Consonant')

    # Vowel inventory:
    # front vowels: i, e
    # back vowels: u, o
    # Consonant inventory: p t k b d g r

    # Add transitions
    # Transitions from start
    hmm.add_transition(
        START,
        FRONT_CONS,
        [('p', 1/7),
         ('t', 1/7), 
         ('k', 1/7), 
         ('b', 1/7), 
         ('d', 1/7), 
         ('g', 1/7), 
         ('r', 1/7)],
        0.25
    )

    hmm.add_transition(
        START,
        BACK_CONS,
        [('p', 1/7),
         ('t', 1/7), 
         ('k', 1/7), 
         ('b', 1/7), 
         ('d', 1/7), 
         ('g', 1/7), 
         ('r', 1/7)],
        0.25
    )

    hmm.add_transition(
        START,
        FRONT_VOWEL,
        [('i', 1/2),
         ('e', 1/2)],
         0.25
    )

    hmm.add_transition(
        START,
        BACK_VOWEL,
        [('u', 1/2),
         ('o', 1/2)],
         0.25
    )

    # Transitions from back vowel
    hmm.add_transition(
        BACK_VOWEL,
        BACK_CONS,
        [('p', 1/7),
         ('t', 1/7), 
         ('k', 1/7), 
         ('b', 1/7), 
         ('d', 1/7), 
         ('g', 1/7), 
         ('r', 1/7)],
        0.7
    )

    hmm.add_transition(
        BACK_VOWEL,
        END,
        [('', 1)],
        0.3
    )


    # Transitions from front vowel
    hmm.add_transition(
        FRONT_VOWEL,
        FRONT_CONS,
        [('p', 1/7),
         ('t', 1/7), 
         ('k', 1/7), 
         ('b', 1/7), 
         ('d', 1/7), 
         ('g', 1/7), 
         ('r', 1/7)],
        0.7
    )
    hmm.add_transition(
        FRONT_VOWEL,
        END,
        [('', 1)],
        0.3
    )

    # Transitions from back consonant
    hmm.add_transition(
        BACK_CONS,
        BACK_VOWEL,
        [('u', 1/2),
         ('o', 1/2)],
         1
    )

    # Transitions from front consonant
    hmm.add_transition(
        FRONT_CONS,
        FRONT_VOWEL,
        [('i', 1/2),
         ('e', 1/2)],
         1
    )

    stringset = hmm.generate_stringset(corpus_size)
    stringset = [' '.join(word) for word in stringset]
    uniques = list(set(stringset))

    with open(outfile, 'w') as f:
        for word in uniques:
            print(word, file=f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates vowel harmony datasets.'
    )
    parser.add_argument(
        '--corpus_size', type=int, default=DEFAULT_CORPUS_SIZE,
        help='The number of tokens to generate.'
    )
    parser.add_argument(
        '--outfile', type=str, default=DEFAULT_OUTFILE,
        help='The file to save output corpus in.'
    )
    args = parser.parse_args()

    generate_corpora(
        args.corpus_size, args.outfile
    )
