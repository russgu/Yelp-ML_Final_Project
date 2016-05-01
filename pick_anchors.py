
# stemming
import json, re, nltk, ast, codecs
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.sentiment.util import mark_negation


def stem(infile, outfile,  anchors, stem=True, negate=True):
    stemmer = SnowballStemmer("english", ignore_stopwords=True)

    with open(infile,'r') as f, open(outfile,'w') as out_f:
        i = 0
        for line in f:
            line = json.loads(json.loads(line))
            for anchor in anchors:
                words = anchor.split(" / ")
                for w in words:
                    temp = w.replace(" ", "_")
                    line['text'] = line['text'].replace(w, temp)
            #text_before_stem = word_tokenize(line)
            
##            if stem:
##                text_after_stem = []
##                for word in text_before_stem:
##                    word = stemmer.stem(word)
##                    text_after_stem.append(word)
##            
##            if negate:
##                text_after_stem = mark_negation(text_after_stem, double_neg_flip=True)
##                
                
            #text_after_stem = ' '.join(text_after_stem)                              
            
            #line['text'] = text_after_stem
            json.dump(line, out_f)
            out_f.write('\n')
            

def find_anchors(infile, anchors):
    outf = open("counts.txt", 'w')
    for anchor in anchors:
        totalcount = 0
        totalstars = {1:0, 2:0, 3:0, 4:0, 5:0}       
        words = anchor.split(" / ")
        for word in words:
            stars = {1:0, 2:0, 3:0, 4:0, 5:0}
            count = 0
            with open(infile, 'r') as f:
                word = word.replace(" ", "_")
                pos = 0
                neg = 0
                for line in f: 
                    line = json.loads(line)
                    star = line['stars']
                    text = line['text']
                    if stars[(line['stars'])] == 1:
                        pos += 1
                    elif stars[(line['stars'])] == 0:
                        neg += 1
                    
                    
                    
                    if " "+word+" " in text:
                        count += 1
                        stars[(line['stars'])] += 1
                        totalcount += 1
                        totalstars[(line['stars'])] += 1

                print pos
                print neg
                assert False
                print word
                print "count " + str(count)
                print "stars " + str(stars)
                outf.write(word + " count: " + str(count) + " stars: " + str(stars) + "\n")
                
           
        print words
        print "count " + str(totalcount)
        print "stars " + str(totalstars)
        print "\n"
        outf.write(str(words) + " count: " + str(totalcount) + " stars: " + str(totalstars) + "\n")
    outf.close()
training_file = 'train_reviews.json'
output_file = 'stemmed_review_text.txt'

anchors = ["rip off / over charged / overpriced / over priced",
           "worth every penny / affordable prices / fair prices / fairly priced", "complimentary",
           "best margaritas",
           "happy hour",
           "spicy / flavorful / hot", "fresh / tender / juicy",
            "bland / tasteless",
            "stale / soggy / canned",
           "luke warm / cold food",
           "best tacos / best taco",
           "best guacamole / fresh guac / homemade guacamole",
           "gourmet",
           "fresh / homemade",
           "small portions",
           "decor / ambience",
            "laid back / casual",
            "date",
            "bright",
            "hidden gem / little gem",
            "terrible service / horrible service / worst service / rude / poor service",
            "sent back / wrong food / never received",
            "extremely attentive / outstanding service / extremely helpful",
            "took forever / finally came",
            "line",
            "authentic / traditional",
            "patio seating",
            "breakfast / brunch",
            "food poisoning / got sick",
            "only saving grace / only redeeming / only positive"]

stem(training_file, output_file, anchors)

find_anchors(output_file, anchors)
