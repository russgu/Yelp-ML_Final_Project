import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


'''
read feature vectors from 'filename' into memory
'''
def feature_vectors(filename):
    f = open(filename, 'r')
    features = []
    labels = []
    i = 0
    countpos = 0
    countneg = 0
    for line in f:
        line = line.split()
        try:
            labels.append(int(line[0]))
        except:
            print line[0]

        if int(line[0]) == 1:
            countpos += 1
        elif int(line[0]) == 0:
            countneg += 1
        
        feats = []
        for j in range(1, len(line)):
            if "anchor" in filename:
                feats.append(float(line[j]))
            else:
                feats.append(int(line[j]))
        features.append(feats)
        #print feats[0]
        
        i += 1
        ##if i == 1000:
        ##    break

    print len(features)
    print str(countpos) + " positive reviews"
    print str(countneg) + " negative reviews"
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
        
train = feature_vectors('train_features.txt')
train_feats = np.array(train[0])
train_labels = np.array(train[1])

test = feature_vectors('validate_features.txt')
test_feats = np.array(test[0])
test_labels = np.array(test[1])

print "Bag of words features done"
##top_weights(train_feats, train_labels)

classifier = SVC()
classifier.fit(train_feats, train_labels)
print "trained"
train_score = classifier.score(train_feats, train_labels)
print "Baseline training accuracy using linear SVM " + str(train_score)
base_score = classifier.score(test_feats, test_labels)
print "Baseline prediction accuracy using linear SVM " + str(base_score)

train_a = feature_vectors('train_anchor_features.txt')
train_a_feats = np.array(train_a[0])
train_a_labels = np.array(train_a[1])

validate_a = feature_vectors('validate_anchor_features.txt')
validate_a_feats = np.array(validate_a[0])
validate_a_labels = np.array(validate_a[1])

print "anchor features done"

a_svc = SVC(kernel='linear')
print "trained"
a_svc.fit(train_a_feats, train_a_labels)
print "predicted"
train_svc_score = a_svc.score(train_a_feats, train_a_labels)
print "Training accuracy using anchor features and linear SVM " + str(train_svc_score)
svc_score = a_svc.score(validate_a_feats, validate_a_labels)
print "Prediction accuracy using anchor features and linear SVM " + str(svc_score)

##nums = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
##for i in range(0, len(nums)):
##    print nums[i]
##a_rforest = RandomForestClassifier(n_estimators=80, min_samples_leaf=10, max_depth=30)
##a_rforest.fit(train_a_feats, train_a_labels)
##rforest_score = a_rforest.score(validate_a_feats, validate_a_labels)
##print "Prediction accuracy using anchor features and random forest " + str(rforest_score)

##a_gaussian = SVC(kernel='rbf')
##a_gaussian.fit(train_a_feats, train_a_labels)
##gaussian_score = a_gaussian.score(validate_a_feats, validate_a_labels)
##print "Prediction accuracy using anchor features and gaussian kernel " + str(gaussian_score)
