import pandas as pd
from collections import Counter
from itertools import product


def kmers_create(kmerlen: int) -> list:
    
    """
    Create list of all possible k-mers from amino-acid alphabet
    """
    
    alph = "ACDEFGHIKLMNPQRSTVWY"
    
    tup_list = list(product(alph, repeat = kmerlen))
    kmers = [''.join(tups) for tups in tup_list]
    
    return kmers



def kmer_count(seq: str, kamerlen) -> dict:

    """
    Counts the frequency of k-mers in sequence to the dictionary 
    """
    
    kmer_dict = Counter()
    
    for idx in range(len(seq)):
        kmer = seq[idx:idx+kamerlen]
        if len(kmer) == kamerlen:
            kmer_dict[kmer] += 1

    for k,v in kmer_dict.items():
        kmer_dict[k] = v / (len(seq) - kamerlen+1)
    
    return kmer_dict
    


def get_features(sequences, kamerlen):
    
    """
    Return DataFrame with k-mers frequency for all dataset.
    Input: pandas series with sequences, int - length of kmer
    """
    
    return pd.DataFrame([kmer_count(seq,kamerlen) for seq in sequences], columns=kmers_create(kamerlen)).fillna(0)

