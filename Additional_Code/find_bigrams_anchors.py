from nltk import bigrams
from nltk import word_tokenize
from collections import Counter
import json

stoplist = ['a', 'and', 'an', 'on', 'that', 'is', 'of', 'for', 'to',
        'that', 'in', 'by', 'with', 'the', 'from', 'or', 'their',
        'i', 'we', 'was', 'our', 'it', 'at', 'my', 'where', 'not',
        'they', 'but', 'this', 'when', 'us', 'there', 'as', 'but',
        'are', 'if', 'so', 'it\'s', 'be', 'so', 'very', 'just',
        'have', 'which', 'really', 'were', 'had', 'out', 'you',
        'would', 'me', 'up', 'after', 'no', 'after', 'no', 'she',
        'he', 'what', 'all', 'your', 'i\'ve', 'one', 'don\t', 'i\'m',
        'would', 'some']


def finding_bigrams(infile, outfile, no_stop_file):
    
    qualified_bigrams = []
    with open(infile, 'r') as f:
        for line in f: 
            line = json.loads(json.loads(line))

            text = line['text'].lower()
            
            word_list = word_tokenize(text)
            
            bigram_list = list(bigrams(word_list))
            
            for pair in bigram_list:
                if pair[0].isalpha() and pair[1].isalpha():
                    qualified_bigrams.append(pair)

    # count frequency for each bigram
    c = Counter()
    for pair in qualified_bigrams:
        c[pair] += 1

    # save a human-readable version of bigrams
    final_list = []
    with open(outfile,'w') as f:
        # sort all pairs by frequncy from highest to lowest
        most_common = c.most_common(len(c))
        
        for pair in most_common:
            # remove pairs where either words is a stop word
            if pair[0][0] not in stoplist or pair[0][1] not in stoplist and pair[1]>10:
                json.dump(pair, f)
                f.write('\n')
                final_list.append(pair)
                
        
    # save a machine-friendly version of bigrams
    with open(no_stop_file ,'w') as f:
        simplejson.dump(final_list, f)
        
    # get rid of frequency, which is stored at final_list[:][1]
    final_list = [final_list[x][0] for x in range(len(final_list))]
    
    return final_list







def informative_bigrams(infile, outfile, final_list):
    pos_count = [0]*len(most_common)
    neg_count = [0]*len(most_common)

    i = 0
    with open(infile, 'r') as f:
        for line in f:
            line = json.loads(json.loads(line))
            text = line['text'].lower()
            star = line['stars']
            if star >= 4:
                star = 1
            else:
                star = 0

            word_list = word_tokenize(text)

            bigram_list = list(bigrams(word_list)) 
            
            bigram2 = []
            for pair in bigram_list:
                if pair[0].isalpha() and pair[1].isalpha():
                    if pair[0] not in stoplist or pair[1] not in stoplist:
                        bigram2.append(pair)
            
            if star == 1:
                for pair in bigram2:
                    try:
                        pos_count[most_common.index(pair)] += 1
                    except ValueError:
                        pass
            else:
                for pair in bigram2:
                    try:
                        neg_count[most_common.index(pair)] += 1
                    except ValueError:
                        pass    
            
            
            if i % 100 == 0:
                print i
            i+=1
            

    with open(outfile,'w') as f:
        for i in range(len(most_common)):
            json.dump(most_common[i],f)
            f.write(' : ')
            json.dump(pos_count[i],f)
            f.write(',')
            json.dump(neg_count[i],f)
            f.write('\n')




final_list = finding_bigrams('train_LV_reviews_False.json', \
                             'Mexican_LV_bigrams.txt', \
                             '(no_stop)Mexican_LV_final_bigrams.txt')


# ATTENTION: to run "informative_bigrams", you need to run "finding_bigrams" first
informative_bigrams('train_LV_reviews_False.json', \
                    'LV_informative_bigrams',\
                    final_list)
