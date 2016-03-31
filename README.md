
Project Proposal
Zi Gu, Erika Lage, Jielei Zhu March 28th, 2016
Machine Learning

                                Finding Clusters in Yelp Reviews to Predict Star Ratings 
Introduction:                            
Yelp’s Dataset Challenge includes several suggestions for topics of research on its website. One of the suggestions under Natural Language Processing is: “How well can you guess a review's rating from its text alone?” As a standalone problem, this is not particularly interesting, since text reviews are always posted with an accompanying star rating. But if we were able to perform this kind of prediction with an acceptable amount of accuracy, we could use it to predict the ratings of new users from the reviews that a restaurant already has—in other words, to build a recommendation
system. Yelp’s dataset challenge included a competition for building a recommender system, so several of the past winning papers deal with the problem of building good models for recommending new restaurants to existing users. Specifically, “Hidden Factors and Hidden Topics: Understanding Rating Dimensions with Review Text,” by Julian McAuley and Jure Leskovec and “Personalizing Yelp Star Ratings: a Semantic Topic Modeling Approach” by Jack Linshi, both address the problem of incorporating the text of reviews into recommendation systems. Both systems use variations on the LDA topic model, which extracts latent features from reviews that affect star ratings. Our project also aims to explore patterns in Yelp reviews that can be exploited to better predict ratings and make recommendations. We plan to use clustering to partition the data set into subsets with the goal of finding a clustering that approximates separating the restaurants by topics that users care about when choosing a place to eat (eg. ambience, food quality, service). We will then train a model on each of these subcategories to predict the number of stars a restaurant has based on its reviews as a way of evaluating which clusterings are useful for our purposes.

Algorithms:
Our project consists of 3 steps: 1) predict restaurant ratings directly 2) find latent topics 3) use latent topics to predict restaurant ratings.
Predict restaurant ratings directly:
To predict restaurant ratings directly, we will use the text portion of user reviews with stop words removed. For the remaining words, we will use WordNet to determine its part of speech. For this step, we are only interested in parts of speech that convey sentiment––such as adjectives and adverbs––as we are trying to predict restaurant ratings, which are essentially customers’ sentiment in numbers. As mentioned earlier, we will construct the feature vectors using bag-of-words approach. We will then use either regression to predict ratings on a continuous scale or SVM to predict discreet ratings.
Find latent topics:
As an attempt to improve our prediction accuracy in step 1, we would like to focus on sentiment on topics that are more indicative of each restaurant. To do so, we will select out the topics in text reviews using clustering (topics might be around ambience, food quality etc. if our clustering works well), which can be achieved by finding all the nouns(with proper nouns removed, of course). Therefore, the feature vectors for this step will be constructed using the bag-of-word approach on all nouns. We will then apply agglomerative clustering to separate restaurants into clusters and try different horizontal cuts to find the best. A good grouping will separate restaurants into similar categories to the dimensions that users rate reviews along.
Use latent topics to predict restaurant ratings:
Once we know the important topics, we could then find the sentiment-loaded words that are immediately connected to those topics and use them to construct more focused feature vectors. Lastly, we will repeat our prediction algorithm in step 1. The prediction step will be used in judging the effectiveness of each particular clustering.

Dataset Preprocessing:
Yelp’s dataset includes user, tip, check-in, review and business data for businesses in 10 cities and several different countries. They estimate they have data from about 40,000 businesses. For this project, we are primarily interested in businesses and users, and the reviews associated with each. The reviews are currently linked to a particular user or business by an id, so we will need to store all the reviews for a particular user or restaurant together, since we are treating them as the same document.
For features, we initially plan to use a bag of words representation with the number of occurrences of a word stored in the feature vector instead of just whether a word appears once or not. This should show the relative weights of terms, which is important since we are trying to find the features that matter the most to many users instead of trying to find every feature that matters to anyone. From there, we plan on trying several different ways of processing the text to see what gets the best
results. Some of these steps include stemming, removing stop words (the, and, etc.), using just nouns for the clustering step, selecting terms that appear more frequently in the corpus of Yelp reviews, or in one of the clusters than in a more general corpus, normalizing adjectives (for example, good and great could both be classified as the same feature. Linshi uses a version of this in his system) and maybe others.

Evaluation:
Clustering is relatively difficult to evaluate since it is a method of unsupervised learning and there is no ground truth to compare the clusters against. What makes a good cluster is also, to some extent, subjective. In this project, we are trying to find clusters that correspond as closely as possible to dimensions along which users evaluate restaurants. We plan to use the scores of the predictions for the models trained on the clusters as a proxy for estimating how well we reached this goal. The reasoning behind this choice is that the scores of models trained on subsystems with similar values will be higher than the scores from a general purpose model, so if we are getting good results in prediction, it is because we partitioned the data along lines that are close to the lines that users rank restaurants along. As a baseline, we will use the prediction accuracy of a model trained on the entire corpus, and we will assume that any partition that improves accuracy of predictions is a good one, but we will also be able to rank different partitions or clusterings against each other to see which ones are the best.
It will also be helpful to be able to do some manual inspection of the terms that different models think are important. If we end up using an SVM, we can pull the n largest values from the prediction vector and the terms these correspond to, and inspect them to try to visualize how well that particular clustering worked, and to try to think of ways to improve on it.

Timeline:
Deadline: no later than May 1st Total: a month approximately
• Data Preprocessing---by April 4th, Mon.(approximately a week) o Storing reviews for a particular business/user
o Stemming, removing stop words, etc.
• Clustering---by April 18th, Sat.(2 weeks approximately)
o Trying different ways of clustering; for example, using nouns. • Training and testing---by April 28th, Thurs.(1.5 weeks in estimate)
o Multiclass SVM/Regression
o Predict restaurant rating directly( work on baseline) • Report/Evaluation---by May 1st, Sun.(0.5 week roughly)

Conclusion:
We do not expect this system to perform at the same level as the systems that won the Yelp dataset challenge (for obvious reasons), but by using algorithms we are familiar with, we can spend more time fine tuning our system relative to itself. This should give us insight into what kind of features lend themselves to separating the data into categories that will be useful in recommendation systems.

Cited Sites:
https://wordnet.princeton.edu/
https://www.yelp.com/dataset_challenge https://www.yelp.com/html/pdf/YelpDatasetChallengeWinner_HiddenFactors.pdf
https://www.yelp.com/html/pdf/YelpDatasetChallengeWinner_PersonalizingRatings.pdf
