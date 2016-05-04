import json, re, nltk
from collections import Counter
from nltk.tokenize import word_tokenize

'''
if partial is true, stop after num lines (for debugging)

This function builds a dictionary of all unique words that occurs at least 50 times in the training set;
The dictionary is saved in "dictionary.txt"
'''
def build_dictionary(infile, partial=False, num=500):
    f = open(infile, 'r')
    words = []
    i = 0
    for line in f:
        line = json.loads(line)['text']
        text = word_tokenize(line)
        words = words + list(set(text))

        if i%100 == 0:
            print i
        
        i += 1
        if i == num and partial:
            break

    f.close()

    word_counts = Counter(words)
    words = [k for k, v in word_counts.items() if v >= 50]

    f = open('dictionary.txt', 'w')
    for word in words:
        f.write(word.encode('utf-8') + "\n")
    
    f.close()

'''
Reviews are partitioned into 2 groups, 1 and 0(y-label)
    1 - if star rating>=4
    0 - if otherwise
Each review text is converted to a feature vector of the size of words in the dictionary
For each word in dictionary:
    1 - if word appears in the review
    0 - if otherwise
Format: [label, feature_vector]
    all elements are separated by " "
'''
def write_features(infile, binary=True, cutoff=4):
    outfile = infile.replace("_reviews.json", "_features.txt")
    
    f = open('dictionary.txt', 'r')
    words = []
    i = 0
    for line in f:
        words.append(line.strip())
    f.close()
   
    f = open(infile, 'r')
    reviews = []
    for line in f:
        reviews.append(line)
    f.close()

    f = open(outfile, 'w')
    i = 0
    for review in reviews:
        review = json.loads(review)

        if binary:
            if review['stars'] >= cutoff:
                f.write("1")
            else:
                f.write("0")
            f.write(" ")
        else:
            f.write(str(review['stars']) + " ")

        review = review['text'].encode('utf-8')
        review = review.split()
        for word in words:
            if word in review:
                f.write("1")
            else:
                f.write("0")
            f.write(" ")
        f.write("\n")

        if i%100 == 0:
            print i
        i += 1
        
    f.close()
    print "Done features"

##build_dictionary('(yelp)bigrams_selected_reviews.json')
write_features('(yelp)bigrams_selected_reviews.json')


