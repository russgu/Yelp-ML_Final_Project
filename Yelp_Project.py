import json

#======== BUSINESS CRITERIA ==========#
geography = 'city'
geo_name = 'Las Vegas'
business_type = 'Restaurants'
#=====================================#



res_b_id = [] # qualified businesses (represented by their business id)

# finding all qualified restaurants
with open('yelp_academic_dataset_business.json','r') as json_file:
    for line in json_file:
        b_temp = json.loads(line)
        if b_temp[geography] == geo_name and business_type in b_temp['categories']:
            res_b_id.append(b_temp['business_id'])
            


res_review = [] # customer reviews on selected businesses

with open('yelp_academic_dataset_review.json','r') as json_file:
    for line in json_file:
        review_temp = json.loads(line)
        if review_temp['business_id'] in res_b_id:
            res_review.append(review_temp['text'])
            
            
            
with open('(yelp)selected_revews.json','w') as file:
    json.dumps(res_review, file)
    
    
print('There are ', len(res_b_id), ' restaurants in ', geo_name)
print('There are ', len(res_review), ' reviews on selected businesses')
