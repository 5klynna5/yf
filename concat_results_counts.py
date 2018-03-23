import pandas as pd
print(pd.__version__)
import datetime as dt     
date = dt.datetime.today().strftime("%m%d%Y")
week_ago = (dt.datetime.today() - dt.timedelta(days=7)).strftime("%m%d%Y")
#week_ago = '02112018'

count_responses_kindness_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_kindness_'+ date +'_.csv'
count_responses_courage_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_courage_'+ date +'_.csv'
count_responses_respect_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_respect_'+ date +'_.csv'

count_kindness = pd.read_csv(count_responses_kindness_path, encoding = "ISO-8859-1")
count_courage = pd.read_csv(count_responses_courage_path, encoding = "ISO-8859-1")
count_respect = pd.read_csv(count_responses_respect_path, encoding = "ISO-8859-1")

count_all = pd.concat([count_kindness, count_courage, count_respect])

count_all.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_ALL_'+ date +'_.csv')

count_old_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_ALL_'+ week_ago +'_.csv'
count_old = pd.read_csv(count_old_path, encoding = "ISO-8859-1")

count_new = pd.merge(count_all, count_old, on = ['retreat_id', 'school_id', 'retreat'], how = 'outer')
del count_new['Unnamed: 0']
count_new = count_new.loc[~(count_new['number_responses_' + date] == count_new['number_responses_' + week_ago])]

count_new = count_new.loc[count_new['number_responses_' + date].notnull()]

count_new.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey response counts\\count_responses_ALL_NEW_'+ date +'_.csv')