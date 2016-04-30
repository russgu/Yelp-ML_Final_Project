import json 

with open ("(yelp)selected_reviews.json","r") as file,\
open("Anchor-Bigrams.txt","r") as anchor_file,\
open("(yelp)selected_reviews_new.json","w") as new_file:

	anchors=[]
	for line in anchor_file:
		line=line.strip('\n');
		anchors.append(line);

	for line in file:
		data = json.loads(line)
		review = data["text"]

		for word in anchors:
			if word in review: #searching bigrams in review text
				replace=word.replace(" ", "_")
				review=review.replace(" "+word+""," "+replace+"");
		data["text"] = review;
		json.dump({'business_id':data['business_id'],  'user_id': data['user_id'], 'stars':data['stars'], 'text':data['text']}, new_file, ensure_ascii=True)
		new_file.write('\n')
   
