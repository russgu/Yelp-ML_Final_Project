import Anchors as a

preprocessing = a.Preprocessing()
anchor = a.Anchor()

datafile = "(yelp)selected_reviews.json"
anchorfile = "anchors.txt"
dictfile = "dictionary.txt"
windowsize = 0

datafile = preprocessing.process_anchors(datafile, anchorfile, windowsize)
print datafile
preprocessing.write_dictionary(datafile, dictfile)
datafile = preprocessing.write_features(datafile, dictfile)
print datafile

##Pull in partitioning reviews into test and train sets

anchor.write_anchor_features(trainfile, testfile, dictfile, anchorfile)



