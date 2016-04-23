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

    predict_i = np.arange(len(features))
    train_i = np.random.choice(predict_i, len(features)*(0.8), False)
    predict_i = np.setdiff1d(predict_i, train_i, True)
    validate_i = np.random.choice(train_i, len(train_i)*(0.2), False)
    train_i = np.setdiff1d(train_i, validate_i, True)
    
    labels = np.array([0] * len(features))
    count = 0
    for i in range (0, len(features)):
        labels[i] = features[i][anchor]
        if labels[i] == 1:
            count += 1
    print "Count : " + str(count)

    feat_i = np.arange(len(features[0]))
    feat_i = np.setdiff1d(feat_i, [anchor], True)
    features = features[:,feat_i]

    train_feat = features[train_i]
    validate_feat = features[validate_i]
    predict_feat = features[predict_i]

    train_lab = labels[train_i]
    validate_lab = labels[validate_i]
    predict_lab = labels[predict_i]

    log = linear_model.LogisticRegression()
    log.fit(train_feat, train_lab)
    probs = np.array(log.predict_proba(validate_feat))[:,[1]]
    
    c = 0
    n = 0
    for i in range(0, len(validate_i)):
        if validate_lab[i] == 1:
            c += probs[i]
            n += 1
    c = c/n
    probs = np.array(log.predict_proba(predict_feat))[:,[1]]
    for i in range(0, len(predict_i)):
        if predict_lab[i] == 1:
            probs[i] = 1
        else:
            probs[i] = probs[i]/c

    ##count_errors(predict_lab, anchor, probs)
    ##print len(probs)
    return probs

def write_anchor_features(infile):
    features = read_reviews(infile)
    dictionary = read_dictionary('dictionary.txt')

    outfile = infile.replace('_features', '_anchor_features')

    f = open(outfile, 'w')

    anchors = ['disappointing_neg', 'microwav', 'fair', 'portion_neg']
                #'the', 'and', 'food', 'included_neg', 'bathroom', 'drunken', 'disappointing_neg', 'microwav',
                #'fair', 'struggl', 'lousi', 'portion_neg']
                #'bathroom', 
    anchors = anchor_indices(anchors, dictionary)
    anchor_feats = predict_latent_feature(features, anchors[0])
    for i in range(1, len(anchors)):
        ##print "anchor index: " + str(anchors[i])
        ##predict_latent_feature(features, anchors[i])
        ##print "\n"
        anchor_feats = np.hstack((anchor_feats, predict_latent_feature(features, anchors[i])))

    for i in range(0, len(anchor_feats)):
        for j in range(1, len(anchor_feats[0])):
            f.write(anchor_feats[i][j] + " ")
        f.write("\n")

write_anchor_features('train_features.txt')








