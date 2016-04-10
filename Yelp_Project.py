import json

#======== BUSINESS CRITERIA ==========#
geography = 'city'
geo_name = 'Madison'
business_type = 'Restaurants' 
#=====================================#

res_b_id = [] # qualified businesses (represented by their business id)

# finding all qualified restaurants
with open('yelp_academic_dataset_business.json','r') as json_file:
    for line in json_file:
        b_temp = json.loads(line)
        if b_temp[geography] == geo_name and business_type in b_temp['categories']:
            res_b_id.append(b_temp['business_id'])
            
            
            
            
review_count = 0 # customer reviews on selected businesses

with open('yelp_academic_dataset_review.json','r') as json_file,\
open('(yelp)selected_reviews.json','w') as file:
    for line in json_file:
        review_temp = json.loads(line)
        if review_temp['business_id'] in res_b_id:
            json.dump({'business_id':review_temp['business_id'],  'user_id': review_temp['user_id'], 'stars':review_temp['stars'], 'text':review_temp['text']}, file, ensure_ascii=True)
            file.write('\n')
            review_count += 1
                     
                     
                     
print('There are ', str(len(res_b_id)), ' restaurants in ', geo_name)
print('There are ', str(review_count), ' reviews on selected businesses')
