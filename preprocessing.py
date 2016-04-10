import json, re, nltk
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

stemmer = SnowballStemmer("english", ignore_stopwords=True)

def select_pos(text, pos, stem):
    tags = nltk.pos_tag(text)
    words = []
    for tag in tags:
        if tag[1] in pos:
            word = tag[0]
            if stem:
                word = stemmer.stem(tag[0])
            if re.match("[a-z]+", word):
                words.append(word)
    return list(set(words))

def features_from_reviews(tag, stem, pos, partial, num):
    
    f = open('(yelp)selected_reviews.json', 'r')
    reviews = []
    stars = []
    words = []
    i = 0
    for line in f:
        reviews.append([])
        line = json.loads(line)
        stars.append(line['stars'])
        text = word_tokenize(line['text'])
        if tag:
            reviews[i] = select_pos(text, pos, stem)
        elif stem:
            w = []
            for word in text:
                word = stemmer.stem(word)
                w.append(word)
            reviews[i] = list(set(w))
        words = words + reviews[i]

        if i%100 == 0:
            print i
        
        i += 1
        if i == num and partial:
            break

    f.close()

    print("Done part 1")

    word_counts = Counter(words)
    words = [k for k, v in word_counts.items() if v >= 50]

    print "num features: " + str(len(words))
    print "num reviews: " + str(len(reviews))

    f = open('dictionary_0.txt', 'w')
    for word in words:
        try:
            f.write(word.encode('utf-8') + "\n")
        except:
            print word
            print q
    f.close()

    print ("Dict done")

    f = open('features_0.txt', 'w')
    i = 0
    for review in reviews:
        if i%100 == 0:
            print i
        if stars[i] >= 4:
            f.write("1")
        else:
            f.write("0")
        f.write(" ")
        for word in words:
            if word in review:
                f.write("1")
            else:
                f.write("0")
            f.write(" ")
        f.write("\n")
        i += 1
        
    f.close()
    print "Done features"


pos = ["NN", "NNS", "NNP", "NNPS"]
features_from_reviews(False, True, pos, False, 500)
