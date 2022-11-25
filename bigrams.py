from nltk.corpus import gutenberg
import nltk
from collections import defaultdict, Counter

emma = nltk.Text(nltk.corpus.gutenberg.words('austen-emma.txt'))
bigramStats = defaultdict(int)
unigramStats = Counter(emma)

for i in range(len(emma)-1):
    bigramStats[tuple(emma[i:i+2])] += 1

    

    

    

