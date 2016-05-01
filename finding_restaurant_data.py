import json
import time

# #======== BUSINESS CRITERIA ==========#
# business_type = 'Chinese' 
##city = 'Las Vegas'
# #=====================================#

def finding_restaurants(business_type, city, debug_flag):
    start = time.time()
    res_b_id = [] # qualified businesses (represented by their business id)
    outfile = '(yelp)'+str(business_type)+'_'+str(city)+'_reviews_'+str(debug_flag)+'.json'


    # finding all qualified restaurants
    with open('yelp_academic_dataset_business.json','r') as json_file:
        for line in json_file:
            b_temp = json.loads(line)
            if city == 'None':
                if business_type in b_temp['categories']:
                    res_b_id.append(b_temp['business_id'])
            else:
                if business_type in b_temp['categories'] and city in b_temp['city']:
                    res_b_id.append(b_temp['business_id'])
                
             
    review_count = 0 # customer reviews on selected businesses

    with open('yelp_academic_dataset_review.json','r') as json_file,\
    open(outfile,'w') as file:
        for line in json_file:
            review_temp = json.loads(line)
            if review_temp['business_id'] in res_b_id:
                json.dump({'business_id':review_temp['business_id'],  \
                    'user_id': review_temp['user_id'], 'stars':review_temp['stars'], \
                    'text':review_temp['text']}, file, ensure_ascii=True)
                file.write('\n')
                review_count += 1

                if debug_flag == True:
                    if review_count == 500:
                        break
                                   
    end = time.time()                        
    print 'There are ', str(len(res_b_id)), '', str(business_type), ' restaurants '
    print 'There are ', str(review_count), ' reviews on selected businesses'
    print 'All data saved to '+ outfile
    print 'Entire process took ' + str(end-start)



finding_restaurants('Mexican', 'Las Vegas', False)
