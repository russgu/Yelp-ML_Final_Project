import json, re, nltk
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.sentiment.util import mark_negation

# def select_pos(text, pos, stem):
#     tags = nltk.pos_tag(text)
#     words = []
#     for tag in tags:
#         if tag[1] in pos:
#             word = tag[0]
#             if re.match("[a-z]+", word):
#                 words.append(word)
#     return list(set(words))

'''
if stem is true, stem the words in the reviews
if negate is true, apply scope of negate to mark negated words
if pos is non-null, select only the parts of speech in pos
if partial is true, stop after num lines (for debugging)
At this point, must pick eitehr pos or negate

This function builds a dictionary of all unique words that occurs at least 50 times in the training set;
If negate=True, "disappoint" and "disappoint_NEG" are considered as two unique words. 
The dictionary is saved in "dictionary.txt"
'''
def build_dictionary(infile, stem=False, negate=False, pos=[], partial=False, num=500):
    if stem:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
    
    f = open(infile, 'r')
    reviews = []
    words = []
    i = 0
    for line in f:
        reviews.append([])
        line = json.loads(line)
        text = word_tokenize(line['text'])
        #if len(pos) > 0:
        #    text = select_pos(text, pos, stem)
        #elif negate:
        #    text = mark_negation(text, double_neg_flip=True)
        if stem:
            for j in range(0, len(text)):
                text[j] = stemmer.stem(text[j])
                #w.append(word)
            #reviews[i] = list(set(w))
        if negate:
            text = mark_negation(text, double_neg_flip=True)
        words = words + list(set(text))

        if i%100 == 0:
            print i
        
        i += 1
        if i == num and partial:
            break

    f.close()

    word_counts = Counter(words)
    words = [k for k, v in word_counts.items() if v >= 50]

    print "num features: " + str(len(words))
    print "num reviews: " + str(len(reviews))

    f = open('dictionary.txt', 'w')
    for word in words:
        f.write(word.encode('utf-8') + "\n")
        
        #try:
            #f.write(word.encode('utf-8') + "\n")
        #except:
            #print word
            #print q
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


#pos = ["NN", "NNS", "NNP", "NNPS"]

#build_dictionary('(yelp)selected_reviews.json')

#write_features('train_reviews.json')
#write_features('validate_reviews.json')
#write_features('test_reviews.json')

build_dictionary('(yelp)selected_reviews.json')
write_features('(yelp)selected_reviews.json')


