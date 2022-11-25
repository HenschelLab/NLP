## Basic procedure to
## Scoring matrix delta is implemented as a function (given as argument to dp)
import pdb
from numpy import zeros, arange, argmin

def dp(v,w, delta, gap=1):
    n = len(v)
    m = len(w)
    D = zeros((n+1, m+1), dtype=int)
    b = zeros((n+1, m+1), dtype=int)
    b[0,1:] = 1

    D[0] = arange(m+1) * gap
    D[:,0] = arange(n+1) * gap
    for i in range(1,n+1):
        for j in range(1,m+1):
            options = [D[i-1,j] + gap,
                       D[i,j-1] + gap,
                       D[i-1,j-1] + delta(v[i-1], w[j-1])
                       ]
            bestOption = argmin(options) # only considers one best option, breaks ties randomly, kind of
            D[i,j] = options[bestOption]
            b[i,j] = bestOption # better to note down all
    return D,b

def printAlignment(v,w,b):
    print (b, b.shape, b.shape==(0,0))
    ## 0 stands for coming from N
    ## 1 stands for coming from W
    ## 2 stands for coming from NW, ie. either mismatch or match,
    ## Your code here
    return

def delta(a, b, matchscore=0, mismatch=2):
    if a==b: return matchscore
    else: return mismatch

if __name__ == "__main__":
    #D,b = dp('BRIEF', 'DRIVE', delta, gap=1)
    D,b = dp('BANANA', 'BAHAMAS', delta, gap=1)
    #D,b = dp('KINDLE', 'KINKLA', delta, gap=1)
    print(D)

            


