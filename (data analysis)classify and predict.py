import numpy as np
from sklearn.svm import LinearSVC

'''
read feature vectors from 'filename' into memory
'''
def feature_vectors(filename):
    f = open(filename, 'r')
    features = []
    labels = []
    i = 0
    for line in f:
        line = line.split()
        labels.append(int(line[0]))
        
        feats = []
        for j in range(1, len(line)):
            if "anchor" in filename:
                feats.append(float(line[j]))
            else:
                feats.append(int(line[j]))
        features.append(feats)
        
        i += 1
        ##if i == 1000:
        ##    break
        
    return [features, labels]

'''
Get weight vectors for each word in dictionary from sklearn.svm's LinearSVC
Weight vectors are sorted by their absolute values and saved to "l1topweights.txt" with corresponding words(i.e. [word,weight])
'''
def top_weights(train_feats, train_labels):
    classifier = LinearSVC(penalty="l1", dual=False)
    classifier.fit(train_feats, train_labels)
    coefs = list((classifier.coef_)[0])
    
    f = open('dictionary.txt', 'r')
    words = []
    for line in f:
        words.append(line.split())

    f = open('l1topweights.txt', 'w')
    m = 1
    while (m != 0):
        maxc = max(coefs)
        minc = min(coefs)

        if abs(minc) > maxc:
            m = minc
        else:
            m = maxc
            
        f.write(str(words[coefs.index(m)][0]) + " : " + str(m) + "\n")
        # print str(words[coefs.index(m)][0]) + " : " + str(m)
        coefs.remove(m)
        
##train = feature_vectors('train_features.txt')
##train_feats = np.array(train[0])
##train_labels = np.array(train[1])

##test = feature_vectors('validate_features.txt')
##test_feats = np.array(test[0])
##test_labels = np.array(test[1])

##top_weights(train_feats, train_labels)

##classifier = LinearSVC()
##classifier.fit(train_feats, train_labels)
##predictions = classifier.predict(test_feats)
##print "Baseline prediction accuracy " + str(classifier.score(test_feats, test_labels))

train_a = feature_vectors('train_anchor_features.txt')
train_a_feats = np.array(train_a[0])
train_a_labels = np.array(train_a[1])

validate_a = feature_vectors('validate_anchor_features.txt')
validate_a_feats = np.array(validate_a[0])
validate_a_labels = np.array(validate_a[1])

a_classifier = LinearSVC()
a_classifier.fit(train_a_feats, train_a_labels)
print "Anchors prediction accuracy " + str(a_classifier.score(validate_a_feats, validate_a_labels))
