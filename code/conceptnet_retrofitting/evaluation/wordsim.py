import os

from scipy.stats import spearmanr
import numpy as np

directory = os.path.dirname(os.path.abspath(__file__))

def evaluate(similarity_func, standard):
    actual, ideal = [], []
    for w1, w2, assoc in standard:
        ideal.append(assoc)
        actual.append(similarity_func(w1, w2))

    return spearmanr(np.array(ideal), np.array(actual))[0]

def test_all(similarity_func):
    print("wordsim-353")
    print(evaluate(similarity_func, parse_wordsim()))
    print("men-3000")
    print(evaluate(similarity_func, parse_men3000()))
    print("rg-65")
    print(evaluate(similarity_func, parse_rg65()))
    print("rw")
    print(evaluate(similarity_func, parse_rw()))
    print("mc-30")
    print(evaluate(similarity_func, parse_mc30()))

def parse_file(filename, sep=None, preprocess_word=None):
    with open(os.path.join(directory, 'data', filename)) as file:
        for line in file:
            if sep is None:
                w1, w2, val, *_ = line.strip().split()
            else:
                w1, w2, val, *_ = line.strip().split(sep)

            if preprocess_word is not None:
                w1 = preprocess_word(w1)
                w2 = preprocess_word(w2)

            yield w1, w2, float(val)


def parse_wordsim(filename='ws353.csv'):
    return parse_file(filename, sep=',')

def parse_men3000(filename='men3000-dev.csv'):
    return parse_file(filename, preprocess_word=lambda w: w.split('-')[0])

def parse_rw(filename='rw.csv'):
    return parse_file(filename)

def parse_rg65(filename='rg-65.csv'):
    return parse_file(filename)

def parse_mc30(filename='mc30.csv'):
    return parse_file(filename)

def main(labels_in, vecs_in, verbose=True):
    from conceptnet_retrofitting import loaders
    from conceptnet_retrofitting.word_vectors import WordVectors

    if verbose >= 2:
        print("Loading labels")

    labels = loaders.load_labels(labels_in)

    standardize = labels[0].startswith('/c/')

    if verbose >= 2:
        print("Loading vectors")
    vecs = loaders.load_vecs(vecs_in)

    if verbose >= 2:
        print("Building LabelSet")
    wv = WordVectors(labels, vecs, standardize=standardize)

    test_all(wv.similarity)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])