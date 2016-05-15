from __future__ import division
import json
import numpy as np

class Partition_Reviews():
    
    def count_reviews(self, filename):
        f = open(filename, 'r')
        reviews = 0
        for line in f:
            reviews += 1
        return reviews


    #Don't run this!! Use pre-generated indices.txt file
    #Generates random indices for train, validate, test sets and writes them to a file
    def generate_set_indices(self, num_reviews):
        test = np.arange(num_reviews)
        train = np.random.choice(test, int(num_reviews*(8/10)), False)
        test = np.setdiff1d(test, train, True)
        validate = np.random.choice(train, int(len(train)*(2/10)), False)
        train = np.setdiff1d(train, validate, True)

        f = open('indices.txt', 'w')
        sets = [train, validate, test]
        set_names = ['train', 'validate', 'test']
        for i in range(0, len(sets)):
            f.write(set_names[i])
            f.write("\n")
            for j in sets[i]:
                f.write(str(j))
                f.write("\n")
        f.close()

    def partition_reviews(self, infile, indexfile):
        ind = infile.find('_')
        outfile = infile[ind:]
        
        f = open(indexfile, 'r')
        lines = f.readlines()
        train = []
        validate = []
        test = []
        i = 1
        while 'validate' not in lines[i]:
            lines[i] = lines[i].strip()
            train.append(int(lines[i]))
            i += 1
        i += 1
        while 'test' not in lines[i]:
            lines[i] = lines[i].strip()
            validate.append(int(lines[i]))
            i += 1
        i += 1
        while i < len(lines):
            lines[i] = lines[i].strip()
            test.append(int(lines[i]))
            i += 1

        reviews = []      
        f = open(infile, 'r')
        for line in f:
            reviews.append(line)
        reviews = np.array(reviews)
        f.close()

        f = open('train'+outfile, 'w')
        for r in reviews[train]:
            if 'json' in outfile:
                json.dump(r, f)
                f.write("\n")
            else:
                f.write(r)
        f.close()

        f = open('validate'+outfile, 'w')
        for r in reviews[validate]:
            if 'json' in outfile:
                json.dump(r, f)
                f.write("\n")
            else:
                f.write(r)
        f.close()

        f = open('test'+outfile, 'w')
        for r in reviews[test]:
            if 'json' in outfile:
                json.dump(r, f)
                f.write("\n")
            else:
                f.write(r)
        f.close()
