from __future__ import division
import json, re
from sklearn import linear_model
import numpy as np

def read_reviews(filename):
    f = open(filename, 'r')
    features = []
    j = 0
    for line in f:
        line = line.split()
        for i in range (0, len(line)):
            line[i] = int(line[i])

        features.append(line)
##        if j == 10000:
##            break
        j += 1

    return features

def read_dictionary(filename):
    f = open(filename, 'r')
    dictionary = []
    for line in f:
        line = line.replace("\n", "")
        dictionary.append(line)
        
    return dictionary

def anchor_index(anchor, dictionary):
    try:
        return dictionary.index(anchor)
    except:
        return False

def anchor_train(features, anchor, dictionary):    
    features = np.array(features)

    labels = np.array([0] * len(features))
    anchors = anchor.split(" / ")
    anchor_i = [0]
    for a in anchors:
        ##Remove individual parts of a bigram from feature vector
        for w in a.split():
            if w != a:
                w = anchor_index(w, dictionary)
                if w:
                    anchor_i.append(w)
            
        a = a.replace(" ", "_")
        a = anchor_index(a, dictionary)
        anchor_i.append(a)
        for i in range (0, len(features)):
            if features[i][a] == 1:
                labels[i] = 1
            
    feat_i = np.arange(len(features[0]))
    feat_i = np.setdiff1d(feat_i, anchor_i, True)
    features = features[:,feat_i]

    train_i = np.arange(len(features))
    validate_i = np.random.choice(train_i, len(features)*(0.5), False)
    train_i = np.setdiff1d(train_i, validate_i, True)

    train_feat = features[train_i]
    validate_feat = features[validate_i]

    train_lab = labels[train_i]
    validate_lab = labels[validate_i]

    log = linear_model.LogisticRegression()
    log.fit(train_feat, train_lab)
    probs = np.array(log.predict_proba(validate_feat))[:,[1]]
    
    c = 0
    n = 0
    for i in range(0, len(validate_feat)):
        if validate_lab[i] == 1:
            c += probs[i]
            n += 1
    c = c/n

    return [log, c]

def predict_anchor_proba(features, anchor, log, c):
    features = np.array(features)

    labels = np.array([0] * len(features))
    anchors = anchor.split(" / ")
    anchor_i = [0]
    for a in anchors:
        ##Remove individual parts of a bigram from feature vector
        for w in a.split():
            if w != a:
                w = anchor_index(w, dictionary)
                if w:
                    anchor_i.append(w)
            
        a = a.replace(" ", "_")
        a = anchor_index(a, dictionary)
        anchor_i.append(a)
        for i in range (0, len(features)):
            if features[i][a] == 1:
                labels[i] = 1
               
    feat_i = np.arange(len(features[0]))
    feat_i = np.setdiff1d(feat_i, anchor_i, True)
    features = features[:,feat_i]

    predictions = []
    probs = log.predict_proba(features)
    for i in range(0, len(features)):
        if labels[i] == 1:
            predictions.append(1.0)
        else:
            if float(probs[i][1]/c) > 1:
                predictions.append(1.0)
            else:
                predictions.append(float(probs[i][1]/c))

    return predictions

def write_anchor_features(trainfile, testfile, anchors):
    train_features = read_reviews(trainfile)
    test_features = read_reviews(testfile)
    dictionary = read_dictionary('dictionary.txt')

    trainoutfile = trainfile.replace('_features', '_anchor_features')
    testoutfile = testfile.replace('_features', '_anchor_features')
    
    train_labels = []
    for i in range(0, len(train_features)):
        train_labels.append(train_features[i][0])

    test_labels = []
    for i in range(0, len(test_features)):
        test_labels.append(test_features[i][0])

    train_anchor_feats = []
    test_anchor_feats = []
    train_anchor_feats.append(train_labels)
    test_anchor_feats.append(test_labels)
    for anchor in anchors:
        print anchor
        a = anchor_train(train_features, anchor, dictionary)
        log = a[0]
        c = a[1]
        train_anchor_feats.append(predict_anchor_proba(train_features, anchor, log, c))
        test_anchor_feats.append(predict_anchor_proba(test_features, anchor, log, c))

    f = open(trainoutfile, 'w')
    for j in range(0, len(train_anchor_feats[0])):
        for i in range(0, len(train_anchor_feats)):
            f.write(str(train_anchor_feats[i][j]))
            f.write(" ")
        f.write("\n")
    f.close()

    f = open(testoutfile, 'w')
    for j in range(0, len(test_anchor_feats[0])):
        for i in range(0, len(test_anchor_feats)):
            f.write(str(test_anchor_feats[i][j]))
            f.write(" ")
        f.write("\n")
    f.close()

anchors = [ "overpriced / over priced",
            "complimentary",
            "happy hour",
            "spicy / flavorful / hot",
            "fresh / tender / juicy",
            "bland",
            "stale / soggy / canned",
            "best tacos / best taco",
            "gourmet",
            "fresh / homemade",
            "decor / ambience",
            "laid back / casual",
            "date",
            "bright",
            "hidden gem / little gem",
            "rude",
            "took forever / finally came",
            "line",
            "authentic / traditional",
            "breakfast / brunch"]

#dictionary = read_dictionary('dictionary.txt')
write_anchor_features('train_features.txt', 'validate_features.txt', anchors)




