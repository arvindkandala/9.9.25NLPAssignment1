# 9.9.25NLPAssignment1

### This project implements a bare-bones Markov text generator using n-gram next-token prediction with stupid backoff and optional stochastic sampling.
    finish_sentence(sentence, n, corpus, randomize=False) -> list[str]

### Parameters
    sentence (list/tuple of str): Seed tokens to start from.
    n (int): N-gram order to use for prediction (tries order n, then backs off).
    corpus (list/tuple of str): Tokenized source text.
    randomize (bool, default False): If False, generation is deterministic; if True, the next token is sampled.

### Returns
    A list of tokens extending the seed until a sentence-ending token (., ?, !) is produced or the sequence reaches 10 tokens—whichever comes first.

### How it Works
1. Context & Matching
    At each step, the model looks at the last n-1 tokens of the current sentence and scans the corpus for all occurrences of that context. It counts how often each following token occurs.
2. Stupid Backoff with alpha = 0.4
    If no matches are found at order n, it backs off to order n-1, then n-2, … down to unigrams. Each time it backs off, it discounts the effective weight of candidate tokens by a factor of α^k where k is the number of backoffs so far (implemented in the sampling weights when randomize=True).
3. Deterministic vs. Randomized
    - Deterministic (randomize=False): Picks the most frequent next token. Ties are broken alphabetically for reproducibility.
    - Randomized (randomize=True): Samples a next token via random.choices with weights proportional to the observed counts and discounted by backoff (i.e., count * α^k).
4. Unigram Fallback
    - If the algorithm backs off to unigrams (order 1), it chooses based on global corpus frequencies (deterministic max-count or weighted sampling).
5. Generation Stops When:
    -A sentence terminator (., ?, !) is produced, or (after sentence has been expanded)
    -The total sequence length reaches 10 tokens.


### Examples
sentence = ['she', 'was', 'not']
n = 3
corpus = nltk.word_tokenize(nltk.corpus.gutenberg.raw('austen-sense.txt').lower())
randomize = False
print(finish_sentence(sentence, n, corpus, randomize))
    output: ['she', 'was', 'not', 'in', 'the', 'world', ',', 'and', 'the', 'two']


sentence2 = ['she', 'was', 'not', 'there']
n2=2
corpus = nltk.word_tokenize(nltk.corpus.gutenberg.raw('austen-sense.txt').lower())
randomize2 = True
random.seed(24)
print(finish_sentence(sentence2, n2, corpus, randomize2))
    output:['she', 'was', 'not', 'there', 'no', 'interest', 'of', 'tricking', 'edward', 'made']


### Areas for Improvement
    - In the event where the input sentence parameter ends in one of (., ?, !), this markov text generator would extend the sentence. In some cases, this might result in the outputted sentence to have back to back punctation
        - Stops only on (. ? !) after appending; commas and semicolons can appear in odd places and never stop a sentence
    - Deterministic mode breaks ties lexicographically, which is arbitrary and corpus-dependent
    - Uses “stupid backoff” without additive/Kneser-Ney smoothing; unseen events get zero mass until lower-order backoffs hit

