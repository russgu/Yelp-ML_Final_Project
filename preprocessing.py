import json, re
from collections import Counter

def features_from_reviews():
    f = open('(yelp)selected_reviews.json', 'r')
    reviews = []
    stars = []
    words = []
##    i = 0
    for line in f:
        line = json.loads(line)
        text = line['text'].lower().replace("'", "")
        text = re.sub("[^a-z]", " ", text)
        text = set(text.split())
        for w in text:
            words.append(w)
        text = " ".join(text)
        reviews.append(text)
        stars.append(line['stars'])

##        i += 1
##        if i == 10:
##            break
    f.close()
  
    word_counts = Counter(words)
    words = [k for k, v in word_counts.items() if v >= 50]
    f = open('dictionary_0.txt', 'w')
    for word in words:
        f.write(word + "\n")
    f.close()

    f = open('features_0.txt', 'w')
    i = 0
    for review in reviews:
        text = review.split()
        if stars[i] >= 4:
            f.write("1")
        else:
            f.write("0")
        f.write(" ")
        for word in words:
            if word in text:
                f.write("1")
            else:
                f.write("0")
            f.write(" ")
        f.write("\n")
        i += 1
        
    f.close()           

features_from_reviews()
