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
        ##if j == 100:
        ##    break
        j += 1

    return features

def read_dictionary(filename):
    f = open(filename, 'r')
    dictionary = []
    for line in f:
        line = line.replace("\n", "")
        dictionary.append(line)
        
    return dictionary

def anchor_indices(anchors, dictionary):
    indices = []
    for anchor in anchors:
        indices.append(dictionary.index(anchor))
    return indices

def count_errors(labels, anchor, predictions):
    i = 0
    errors = 0
    for i in range(0, len(predictions)):
        if predictions[i] > 0.5:
            if labels[i] != 1:
                errors += 1
        else:
            if labels[i] != 0:
                errors += 1
        i += 1
    print str((errors/len(predictions)) * 100) + "% error"
    ##Is this really useful?  Whether the review has the anchor in it isn't actually the ground truth.

    return errors

def predict_latent_feature(features, anchor):
    features = np.array(features)
    
    ##t = (len(features)*(0.6))
    ##v = (len(features)*(0.2))

    ##predict_i = np.arange(len(features))
    ##train_i = np.random.choice(predict_i, len(features)*(0.8), False)
    ##predict_i = np.setdiff1d(predict_i, train_i, True)
    ##validate_i = np.random.choice(train_i, len(train_i)*(0.2), False)
    ##train_i = np.setdiff1d(train_i, validate_i, True)
    
    labels = np.array([0] * len(features))
    count = 0
    for i in range (0, len(features)):
        labels[i] = features[i][anchor]
        if labels[i] == 1:
            count += 1
    print "Count : " + str(count)

    ##return

    feat_i = np.arange(len(features[0]))
    feat_i = np.setdiff1d(feat_i, [0, anchor], True)
    features = features[:,feat_i]

    train_feat = features[:int(len(features)*(0.5))]
    validate_feat = features[int(len(features)*(0.5)):int(len(features)*(0.8))]
    predict_feat = features[int(len(features)*(0.8)):]

    train_lab = labels[:int(len(features)*(0.5))]
    validate_lab = labels[int(len(features)*(0.5)):int(len(features)*(0.8))]
    predict_lab = labels[int(len(features)*(0.8)):]

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
    probs = log.predict_proba(predict_feat)
    labels = []
    for i in range(0, len(predict_feat)):
        if predict_lab[i] == 1:
            labels.append(1.0)
        else:
            if float(probs[i][1]/c) > 1:
                labels.append(1.0)
            else:
                labels.append(float(probs[i][1]/c))

    ##count_errors(predict_lab, anchor, probs)
    ##print len(probs)
    return labels

def write_anchor_features(infile, anchors):
    features = read_reviews(infile)
    dictionary = read_dictionary('dictionary.txt')

    outfile = infile.replace('_features', '_anchor_features')

    f = open(outfile, 'w')

    anchors = anchor_indices(anchors, dictionary)
    labels = []
    for i in range(int(len(features)*(0.8)), len(features)):
        labels.append(features[i][0])

    anchor_feats = []
    anchor_feats.append(labels)
    for i in range(0, len(anchors)):
        anchor_feats.append(predict_latent_feature(features, anchors[i]))
        ##predict_latent_feature(features, anchors[i])
    print len(anchor_feats)
    #print type(anchor_feats)
    print len(anchor_feats[0])
    print len(anchor_feats[1])
    #print type(anchor_feats[0])
    #print type(anchor_feats[0][0])
    for j in range(0, len(anchor_feats[0])):
        for i in range(0, len(anchor_feats)):
            f.write(str(anchor_feats[i][j]))
            f.write(" ")
        f.write("\n")

##anchors = ['wait', 'flavor', 'full', 'decor', 'nice', 'best', 'favorit', 'worst'] ##0.
#anchors = ['full', 'decor', 'nice', 'best', 'flavor', 'set', 'favorit', 'taco', 'special', 'wait', 'includ', 'hot', 'amount', 'disappoint_NEG', 'disappoint', 'portion', 'well', 'high', 'drink', 'wait_NEG', 'best_NEG'] 
anchors = ['full', 'decor', 'flavor', 'hot', 'disappoint_NEG', 'high'] ## Accuracy: 0.659292035398
write_anchor_features('validate_features.txt', anchors)
write_anchor_features('train_features.txt', anchors)




