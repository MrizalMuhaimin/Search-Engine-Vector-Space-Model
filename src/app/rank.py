import pandas as pd
from collections import Counter
from scipy.sparse import csr_matrix

def dot(A,B):
# Fungsi untuk menghitung dot product dari 2 vektor A & B
    sum=0
    if len(A)==len(B) and len(B)!=0:
        for i in range(len(B)):
            sum=sum+(A[i]*B[i])
    return sum

def norm(A):
# Fungsi untuk menghitung nilai dari |A|
    N=0
    for i in range(len(A)):
        N=N+A[i]**2
    N = N ** 0.5
    return N

def fit(corpus):
# fungsi yang melakukan fitting atau memberikan index pada kata-kata unik yang ada pada dokumen yang ada pada corpus.
# dan mengembalikan sebuah dictionary yang berisi index dan kata-kata unik tersebut
    words = set()
    for sentence in corpus:
        for word in sentence.split(' '):
            if len(word) > 1:
                words.add(word.lower())
    vocab = {}
    for i, w in enumerate(sorted(list(words))):
        vocab[w] = i
    return vocab


def transform(vocab,corpus):
# fungsi yang mengembalikan sebuah matrix yang berisi jumlah kemunculan kata dalam 
# vocab pada setiap dokumen di corpus
    row, col, val = [], [], []
    for i, sentence in enumerate(corpus):
        count_word = dict(Counter(sentence.split(' ')))
        for word, count in count_word.items():
            if len(word) > 1:
                col_index = vocab.get(word.lower())
                if col_index >= 0:
                    row.append(i)
                    col.append(col_index)
                    val.append(count)
    Matrix = (csr_matrix((val, (row, col)), shape=(len(corpus), len(vocab)))).toarray()
    return Matrix

def colRename(columns_length):
# Fungsi yang mengembalikan sebuah array of strings yang berisi nama dokumen ke-i
    columns_name = [j for j in range(columns_length)]
    columns_name[0] = 'Query'
    for i in range(1, columns_length):
        columns_name[i] = 'D'+str(i)
    return columns_name

def cosine_sim(dataframe,columns_length):
# Fungsi yang mengembalikan sebuah array of float yang berisikan hasil perhitungan
# Cosine Similarity antara Query dan Dokumen lainnya
    cosine_sim_array = [j for j in range(columns_length-1)]
    for i in range(0, columns_length-1):
        cosine_sim_array[i] = dot(dataframe.values[0], dataframe.values[i+1]) / (norm(dataframe.values[i+1]) * norm(dataframe.values[0]))
        cosine_sim_array[i] = round(cosine_sim_array[i] * 100, 2)
    return cosine_sim_array

