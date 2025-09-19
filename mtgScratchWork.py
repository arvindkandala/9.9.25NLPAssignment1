
import nltk
import numpy
import random

def finish_sentence(sentence, n, corpus, randomize=False):
    
    #if we reach n==0, then the the last word in the sentence doesn’t appear at all in the corpus
    if n==0:
        return None
    
    if n==1:
        #return the most frequent word in the model
        pass
    
    #get the last n-1 tokens of the sentence
    last_nminus1_elements = sentence[-(n-1):]
    occurrences = 0 #the number of times those last n tokens are found in corpus in that order
    wordPredictions = {}
    for i in range(len(corpus)-n):
        #count the number of times those last n tokens are found in corpus in that order
        if corpus[i:i+(n-1)] == last_nminus1_elements: #compares two tuples
            #increment 'occurrences'
            occurrences +=1
            if(i+n<len(corpus)): #check to make sure that the tokens are not the very last elements of the corpus
                next_token = corpus[i + (n - 1)] #selecting an element of corpus, which is a string
                if(next_token) in wordPredictions: #check if the word after the n tokens is already in the wordPredictions
                    wordPredictions[next_token]+=1 #if in wordPredictions, increment count by 1 
                else:
                    wordPredictions[next_token]=1 #if not in wordPredictions, add it and set count to 1
            #if the tokens are at the very end of the corpus, there is no (i+n)th element in the corpus
    

    #for if the n-1 tokens we are looking for are not found in corpus
    if(occurrences==0):
        return finish_sentence(sentence,n-1, corpus, bool(randomize=True)) #backoff and multiply

    #find the most token that most frequently occurs after the (n-1) tokens we're looking for,
    #which is just find the dictionary key with the highest value
    if len(wordPredictions)>0: 
        maxCountToken = None
        maxCount = 0
        for token in wordPredictions:
            if(wordPredictions[token]>maxCount):
                maxCount = wordPredictions[token]
                maxCountToken = token
            elif(wordPredictions[token]==maxCount): #if two tokens have the same count, choose first alphabetically
                if(token < maxCountToken): #if current token comes lexographically before maxCountToken (comparing two strings)
                    maxCountToken = token
                    maxCount = wordPredictions[token]     



    nextWord = None
    if randomize:
        nextWord = random.choices(wordPredictions.keys, weights=wordPredictions.values)
    else:
        nextWord = random.choices()


    
    pass
