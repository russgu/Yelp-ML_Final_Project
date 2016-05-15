import os
import Anchors as a
import finding_restaurant_data as fr
import partition_reviews as pr
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

preprocessing = a.Preprocessing()
anchor = a.Anchors()
rd = a.Read_Data()
fr = fr.Finding_Restaurants()
pr = pr.Partition_Reviews()

path = "../"
anchorfile = "anchors.txt"
dictfile = "dictionary.txt"
restauranttype = "Mexican"
city = "Phoenix"
windowsize = 0
indexfile = city+"indices.txt"

while windowsize <= 5:
    print "Window size = " + str(windowsize)
   
    datafile = fr.finding_restaurants(path, restauranttype, city)
    datafile = "(yelp)selected_reviews.json"
    datafile = preprocessing.process_anchors(datafile, anchorfile, windowsize)
    print datafile

    ##num_reviews = pr.count_reviews(datafile)
    ##pr.generate_set_indices(num_reviews)
    pr.partition_reviews(datafile, indexfile)

    trainfile = 'train'+datafile[datafile.index('_'):]
    validatefile = 'validate'+datafile[datafile.index('_'):]

    preprocessing.write_dictionary(trainfile, dictfile)

    trainfile = preprocessing.write_features(trainfile, dictfile)
    validatefile = preprocessing.write_features(validatefile, dictfile)

    trainfile = "train_features.txt"
    validatefile = "validate_features.txt"

    anchor.write_anchor_features(trainfile, validatefile, dictfile, anchorfile)

    train_a = rd.read_features('train_anchor_features.txt')
    train_a_feats = np.array(train_a[0])
    train_a_labels = np.array(train_a[1])

    validate_a = rd.read_features('validate_anchor_features.txt')
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

    a_rforest = RandomForestClassifier(n_estimators=80, min_samples_leaf=10, max_depth=30)
    a_rforest.fit(train_a_feats, train_a_labels)
    rforest_score = a_rforest.score(validate_a_feats, validate_a_labels)
    print "Prediction accuracy using anchor features and random forest " + str(rforest_score)

    if windowsize == 0:
        windowsize += 1
    else:
        windowsize += 2
