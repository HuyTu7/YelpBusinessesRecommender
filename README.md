# YelpBusinessesRecommender

### Dataset:

The json has been converted into csv files using the sample code provided by the Yelp at https://github.com/Yelp/dataset-examples. The converted CSV can't be loaded into Github due to large size.

### Pre-Processing:
1. Converting all files from json to csv for easier reading and utlizing the existing resources. [ref: https://github.com/Yelp/dataset-examples]

2. Loading business data. Dropping variables ['type','postal_code','latitude','longitude','review_count','attributes','address','is_open','hours','stars']

3. Filtered data to contain only state 'NC'

4. Loading review data. keeping only business id, user id, stars, funny, cool, and useful votes.

5. Merging both datasets by business id.

6. Updating value of the rating 'stars' by the formula (definiately it includes bias):

  ```
  if stars>=3
          stars=stars+(0.1*funny+.6*useful+0.3*cool)/(funny+useful+cool+1)
  else
          stars=stars-(0.1*funny+.6*useful+0.3*cool)/(funny+useful+cool+1)
  ```


### Files:

|\_ Work: where all code resides. <br>
|\_ Documents: All the documents provided by the professor. <br>
|\_ Sample Data: The filtered data files and sample initial files. <br>

```
├── Work\
|   ├── ReadData_AG.py            
|   ├── recommender.ipynb  
├── Documents\
|   ├── Business Questions.txt
|   ├── FinalProjectProblemsProposal.pdf
├── Sample_Data\
|   ├── business.txt          
|   ├── checkin.txt
|   ├── merged_BR3.csv        
|   ├── tip.txt
```

Works Folder Details:
- The ReadData\_AG.py is used for reading csv files, merging data, reducing dimensionality of data and data modification like modifying the rating. After completing data pre-processing, the final dataframe is stored in file to avoid processing the code again and again. Take a look at the path folder of data file. 


### Contributors:

+ Anshuman Goel (agoel5@ncsu.edu)
+ Siddharth Heggadahalli (ssheggad@ncsu.edu)
+ Huy Tu (hqtu@ncsu.edu)
