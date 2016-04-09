import json, re
from sklearn import linear_model
import numpy as np

def read_reviews(filename):
    f = open(filename, 'r')
    features = []
    for line in f:
        line = line.split()
        for i in range (0, len(line)):
            line[i] = int(line[i])
        features.append(line)

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
    return errors

def predict_latent_feature(features, anchor):
    train = features[:200]
    validate = features[200:400]
    predict = features[400:]
    
    labels = [0] * len(features)
    for i in range (0, len(features)):
        labels[i] = features[i][anchor]           
        features[i] = features[i][:anchor]+features[i][anchor+1:]

    log = linear_model.LogisticRegression()
    log.fit(train, labels[:200])
    probs = np.array(log.predict_proba(validate))[:,[1]]

    c = 0
    n = 0
    for i in range(200, 400):
        if labels[i] == 1:
            c += probs[i-200]
            n += 1
    c = c/n

    probs = np.array(log.predict_proba(predict))[:,[1]]
    for i in range(400, 500):
        if labels[i] == 1:
            probs[i-400] = 1
        else:
            probs[i-400] = probs[i-400]/c

    print count_errors(labels[400:500], anchor, probs) 
    return probs
    
features = read_reviews('features_0.txt')
dictionary = read_dictionary('dictionary_0.txt')

anchors = ['over']
anchors = anchor_indices(anchors, dictionary)

predictions = predict_latent_feature(features, anchors[0])







