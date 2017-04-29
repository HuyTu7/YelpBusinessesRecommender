import json,pandas as pd
"""#import pandas as pd
fname = "../../Data/yelp_academic_dataset_business.json"
unformated_data = list()
with open(fname,encoding="utf-8") as f:
    line = f.readlines()
    unformated_data.append(line)
data_list = list()
unformated_data = unformated_data[0]
for _dict in unformated_data:
    data_list.append(_dict)
print(data_list[1])

business=pd.DataFrame.from_dict(list(iter(data_list).iteritems()), orient='columns', dtype=None)
print(business)
#pd.dataframe(data_list)"""

#Reading Business Data
"""business=pd.DataFrame.from_csv("../../Data/yelp_academic_dataset_business.csv")
business.drop(['type','postal_code','latitude','longitude','review_count','attributes','address','is_open','hours','stars'],inplace=True,axis=1)
business.index.name='neighborhood'
business.reset_index(inplace=True)
business.drop(business.columns[[0]],inplace=True,axis=1)"""
#print(business)

#Reading Review Data
review=pd.DataFrame.from_csv("../../Data/yelp_academic_dataset_review.csv")
#business.drop(['type','postal_code','latitude','longitude','review_count','attributes','address','is_open','hours'],inplace=True,axis=1)
business.index.name='reviewid'
business.reset_index(inplace=True)
business.drop(business.columns[[0,4,5,6,7,8,9,10]],inplace=True,axis=1)
print(review)
