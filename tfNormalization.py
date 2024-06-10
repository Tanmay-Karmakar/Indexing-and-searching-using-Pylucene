import numpy as np

def ritf(tf, mtf, k=1):
    return np.log2(1 + tf) / np.log2(k + mtf)  # For a given term and a document

def lrtf(tf, adl, dl):
    return tf * np.log2(1 + adl / dl)          # For a given term and a doument
