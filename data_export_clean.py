
import pandas as pd
print(pd.__version__)
import datetime as dt     
date = dt.datetime.today().strftime("%m%d%Y")
###this code functions using today's date as the date the export was saved
#######redefine date below if using a different one


###ACTION REQUIRED HERE! - add in the name of retreat here, either 'respect', 'courage', or 'kindness'
retreat = 'respect'

results_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\new survey exports\\' + retreat + '_data_new_' + date +'.csv'
results = pd.read_csv(results_path, encoding = "ISO-8859-1")

codebook_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\' + retreat + '_survey_column_book.csv'
codebook = pd.read_csv(codebook_path, encoding = "ISO-8859-1")

school_and_id_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\schools_and_ids_sp18.csv'
school_and_id = pd.read_csv(school_and_id_path, encoding = "ISO-8859-1")


#delete first row
results = results.drop(0)

#delete columns don't want
del results['Collector ID']
del results['IP Address']
del results['Email Address']
del results['First Name']
del results['Last Name']
del results['Custom Data 1']
del results['Unnamed: 0']
#del results['Unnamed: 24']
#del results['Unnamed: 25']

#replace column names with simplified columns in codebook
columns = codebook['simple'].tolist()

results.columns = columns

#results  = results.loc[results['attendance'].isnull(),'attendance'] = results['retreat_id'].map(results.attendance)

###add school name in by merging with school name and id file
results['school_id'] = pd.to_numeric(results['school_id'])

results = pd.merge(results, school_and_id, on = 'school_id', how = 'left')

###put cleaned data in cleaned data folder
results.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\cleaned survey exports\\' + retreat + '_data_clean_' + date + '.csv')

###pivot table to count the number of responses for each retreat_id and school_id combination
count_responses = pd.DataFrame(pd.pivot_table(results, index=['retreat_id', 'school_id'], values='respondent_id', aggfunc='count'))

##renaming the count column to be number of responses
count_responses['number_responses_' + date] = count_responses['respondent_id']
del count_responses['respondent_id']
count_responses['retreat'] = retreat

##save this count table as a csv in the appropriate counts folder
count_responses.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_' + retreat +'_'+ date +'_.csv')
