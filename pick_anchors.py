
# stemming
import json, re, nltk, ast, codecs
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.sentiment.util import mark_negation


def stem(infile, outfile, stem=True, negate=True):
    stemmer = SnowballStemmer("english", ignore_stopwords=True)

    with open(infile,'r') as f, open(outfile,'w') as out_f:
        
        for line in f:
            line = json.loads(json.loads(line))
            text_before_stem = word_tokenize(line['text'])
            
            if stem:
                text_after_stem = []
                for word in text_before_stem:
                    word = stemmer.stem(word)
                    text_after_stem.append(word)
            
            if negate:
                text_after_stem = mark_negation(text_after_stem, double_neg_flip=True)
                
                
            text_after_stem = ' '.join(text_after_stem)                              
            
            line['text'] = text_after_stem
            json.dump(line, out_f)
            out_f.write('\n')
            

def find_anchors(infile, anchors):
    for anchor in anchors:
#         p = re.compile('.*not( [\w]+)* '+anchor+'( [\w]+)*(\.|\?|\!)')
#         posp = re.compile('.* '+anchor+'( [\w]+)*(\.|\?|\!)') 

        with open(infile, 'r') as f:
            stars = {1:0, 2:0, 3:0, 4:0, 5:0}
            count = 0
            poscount = 0
            posstars = {1:0, 2:0, 3:0, 4:0, 5:0}
            

            for line in f: 
                line = json.loads(line)
                star = line['stars']
                text = line['text']
                
                if " "+anchor+" " in text:#posp.match(text) and not p.match(text):
                    poscount += 1
                    posstars[(line['stars'])] += 1

                    
                if anchor+"_NEG" in text:#p.match(text):
                    count += 1
                    stars[(line['stars'])] += 1

            
            print anchor
            print "poscount " + str(poscount)
            print "posstars " + str(posstars)
            print anchor+'_NEG'
            print "negcount " + str(count) 
            print "negstars " + str(stars)
            print "\n"




training_file = 'train_reviews.json'
output_file = 'stemmed_review_text.txt'


stem(training_file, output_file)

anchors = ['overpow','delect','mussel','full','fave','decor','nice','best','flavor','disgust',
'set','gross','favorit','worst','taco','accommod','special','wait','includ','bargain','secret',
'hot','amount','easili','disappoint', 'portion', 'well', 'mmm', 'hook', 'microwav','anticip',
'tight','charm','salti','upset','thorough','high','drink','coat','bustl']

find_anchors(output_file, anchors)
