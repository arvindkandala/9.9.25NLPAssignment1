import random
import nltk
import numpy

def finish_sentence(sentence, n, corpus, randomize=False):
    numBackoffs = 0
    # helper that tries order=n, then backs off to n-1, ..., down to unigram
    def _pick_next(sentence, order):
        
        nonlocal numBackoffs
        if order <= 0:
            return None

        if order == 1:
            # unigram case: return most frequent word in corpus
            counts = {}
            for token in corpus:
                counts[token] = counts.get(token, 0)+1
            if randomize:
                tokens  = list(counts.keys())
                weights = [c * (0.4 ** numBackoffs) for c in counts.values()]
                return random.choices(tokens, weights=weights, k=1)[0]
            else:
                #alphabetical order
                bestCountToken= None 
                bestCount=-1
                for tok, c in counts.items():
                    if c > bestCount or (c == bestCount and (bestCountToken is None or tok < bestCountToken)):
                        bestCountToken= tok
                        bestCount =c
                return bestCountToken   

        # context length = order - 1
        context_len = order - 1
        if (context_len > 0):
            last_nminus1_elements = tuple(sentence[-context_len:])
        else:
            last_nminus1_elements = tuple()



        wordPredictions = {}
        # iterate so that corpus[i + context_len] is in-bounds
        for i in range(len(corpus) - context_len):
            # compare contiguous slices for the context
            if tuple(corpus[i:i+context_len]) == last_nminus1_elements:
                next_token = corpus[i + context_len] #selecting an element of corpus, which is a string
                if next_token in wordPredictions: #check if the word after the n tokens is already in the wordPredictions
                    wordPredictions[next_token]+=1 #if in wordPredictions, increment count by 1 
                else:
                    wordPredictions[next_token]=1 #if not in wordPredictions, add it and set count to 1

        if not wordPredictions: #if the wordPredictions dictionary is empty
            # back off to history with one less token
            # this lower-order distribution when the higher-order one is empty.
            numBackoffs +=1
            return _pick_next(sentence, order - 1)

        # Choose next token (deterministic or random)
        if randomize:
            tokens = list(wordPredictions.keys())
            weights = [cnt * (0.4 ** numBackoffs) for cnt in wordPredictions.values()]
            return random.choices(tokens, weights=weights, k=1)[0]
        else:
            # max count; alphabetical tie-break
            maxCountToken = None
            maxCount = -1  # so count==0 still beats initial value
            for token in wordPredictions: 
                cnt = wordPredictions[token]
                if cnt > maxCount:
                    maxCount = cnt
                    maxCountToken = token
                elif cnt == maxCount:
                    # tie means pick alphabetically first
                    if maxCountToken is None or token < maxCountToken:
                        maxCountToken = token
            return maxCountToken

    mySentence = list(sentence)
    while (len(mySentence)<10):
        numBackoffs = 0
        nextWord =  _pick_next(mySentence, n)
        mySentence.append(nextWord)
        if nextWord is None:
            break
        if (nextWord == '!' or nextWord == '?' or nextWord == '.'):
            break
    
    return mySentence