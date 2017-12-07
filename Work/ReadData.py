#Importing Libraries
import json,pandas as pd

#Reading Business Data
business=pd.DataFrame.from_csv("../../Data/yelp_academic_dataset_business.csv")
business.drop(['type','postal_code','latitude','longitude','review_count','attributes','address','is_open','hours','stars'],inplace=True,axis=1)
business.index.name='neighborhood'
business.reset_index(inplace=True)
business.drop(business.columns[[0]],inplace=True,axis=1)
business=business.loc[business['state']=='NC']
#print(business)

#Reading Review Data
review=pd.DataFrame.from_csv("../../Data/review.csv")
#print(review)

#Merging both sets
br=business.merge(review,on='business_id',how='inner')

#Initialization of variables for creating mapping of userid and businessid to integer value
user_mapping = {}
user_mapping_code = 0
business_mapping = {}
business_mapping_code = 0

#Modifying the user rating based on the type of votes they receive according to the origial rating
for i in range(br.shape[0]):
    if br.loc[i,'stars']>=3:
        br.loc[i,'stars_m']=br.loc[i,'stars']+(0.1*br.loc[i,'funny']+.6*br.loc[i,'useful']+0.3*br.loc[i,'cool'])/(br.loc[i,'funny']+br.loc[i,'useful']+br.loc[i,'cool']+1)
    else:
        br.loc[i,'stars_m']=br.loc[i,'stars']-(0.1*br.loc[i,'funny']+.6*br.loc[i,'useful']+0.3*br.loc[i,'cool'])/(br.loc[i,'funny']+br.loc[i,'useful']+br.loc[i,'cool']+1)

    #Mapping of userid to integer value
    user_name=br.loc[i,'user_id']
    if(user_name not in user_mapping.keys()):
        user_mapping_code += 1
        user_mapping[user_name] = user_mapping_code
    br.loc[i,'user_code'] = user_mapping[user_name]

    #Mapping of businessid to integer value
    business_name = br.loc[i,'business_id']
    if(business_name not in business_mapping.keys()):
        business_mapping_code += 1
        business_mapping[business_name] = business_mapping_code
    br.loc[i,'business_code'] = business_mapping[business_name]

#Saving the pre-processing and filtered data
br.to_csv("../../Data/merged_BR3.csv")
