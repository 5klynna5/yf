
import pandas as pd
import os, sys
print(pd.__version__)
import datetime as dt     
date = dt.datetime.today().strftime("%m%d%Y")
###this code functions using today's date as the date the export was saved
#######redefine date below if using a different one


retreat = 'courage_retreat_69231'
file_name = 'courage_retreat_69231_Central Lyon Middle School.csv'

##load in cleaned data file
folder = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\retreat files for analysis\\' + retreat + '\\'
results = pd.read_csv(folder + file_name, encoding = "ISO-8859-1")


###### FOR ALL RETREATS #######

###responses and attendance

#get the attendance by pulling the most frequently occuring number in the attendance column
##when this is empty has serious error. What do I do?
if results['attendance'].notnull().values.any():
	total_attend = results['attendance'].value_counts().idxmax()
else:
    total_attend = 0
n = len(results)
non_respond = total_attend - n

responses = [n, total_attend, non_respond]
responses_tab = pd.DataFrame(columns = ['n', 'total_attend', 'non_respond'])
responses_tab = responses_tab.append(pd.Series(responses, index = ['n', 'total_attend', 'non_respond']), ignore_index = True)
responses_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_responses.csv')


##recommend question to file
recommend_tab = pd.DataFrame(columns = ['Number strongly agree', 'Number agree', 'Number disagree',	'Number strongly disagree'])

recommend_counts = [results['recommend_retreat'].str.match('Strongly Agree').sum(),
results['recommend_retreat'].str.match('Agree').sum(),
results['recommend_retreat'].str.match('Disagree').sum(),
results['recommend_retreat'].str.match('Strongly Disagree').sum()]

recommend_tab = recommend_tab.append(pd.Series(recommend_counts, index = ['Number strongly agree', 'Number agree', 'Number disagree',	'Number strongly disagree']), ignore_index=True)

recommend_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_recommend.csv')

###### END OF ALL RETREAT SECTION ######

###### COURAGE SPECIFIC SECTION ####

#if retreat == 'courage':

###create file of responses to "following through on act of courage"
followed_through_vals = [results['followed_through_act_courage'].str.match('I don\'t know').sum(),
results['followed_through_act_courage'].str.match('No').sum(),
results['followed_through_act_courage'].str.match('Partially').sum(),
results['followed_through_act_courage'].str.match('Yes').sum()]
    
followed_through_list = ['I don\'t know', 'No', 'Partially', 'Yes']
followed_through_tab = pd.DataFrame({'response' : followed_through_list, 'vals' : followed_through_vals})
    
followed_through_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_followed_through.csv')

####stacked bars data file

##creating list of columns that needs to go into the stacked bar chart
cols = list(results.columns)
stacked_bars = cols[3:10]
stacked_bars = [w.replace('Â', '') for w in stacked_bars]
stacked_bars_tab = pd.DataFrame(columns = ['simple', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree'])

for item in stacked_bars:
    item = ([item, results[item].str.match('Strongly Disagree').sum(),
    results[item].str.match('Disagree').sum(),
    results[item].str.match('Agree').sum(),
    results[item].str.match('Strongly Agree').sum()])
    stacked_bars_tab = stacked_bars_tab.append(pd.Series(item, index = ['simple', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree']), ignore_index=True)


##merge question text into data file and keep that instead of simple label
stacked_bars_tab = stacked_bars_tab.merge(codebook, on = "simple", how = "left")
stacked_bars_tab = stacked_bars_tab[['exported', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree']]
	
###creating column to sort on, sorting, then deleting
stacked_bars_tab['sum_agree_percent'] = (stacked_bars_tab['Number strongly agree'] + stacked_bars_tab['Number agree'])/(stacked_bars_tab['Number strongly agree'] + stacked_bars_tab['Number agree'] + stacked_bars_tab['Number disagree'] + stacked_bars_tab['Number strongly disagree'])
stacked_bars_tab = stacked_bars_tab.sort_values('sum_agree_percent')
    
del stacked_bars_tab['sum_agree_percent']
##save file to folder
stacked_bars_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_stacked_bars.csv')
'''
#### END OF COURAGE SECTION #####
#### RESPECT SPECIFIC SECTION #####
elif retreat == 'respect':

###create file of responses to "following through on commitment to respect"
	followed_through_vals = [results['followed_through_commitment'].str.match('I don\'t know').sum(),
	results['followed_through_commitment'].str.match('No').sum(),
	results['followed_through_commitment'].str.match('Partially').sum(),
	results['followed_through_commitment'].str.match('Yes').sum()]

	followed_through_list = ['I don\'t know', 'No', 'Partially', 'Yes']

	followed_through_tab = pd.DataFrame({'response' : followed_through_list, 'vals' : followed_through_vals})

	followed_through_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_followed_through.csv')

###creating stacked bars subset by getting the specific columns included
	cols = list(results.columns)
	stacked_bars = cols[3:12]

	stacked_bars_tab = pd.DataFrame(columns = ['simple', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree'])

	for item in stacked_bars:
		item = ([item, results[item].str.match('Strongly Disagree').sum(),
		results[item].str.match('Disagree').sum(),
		results[item].str.match('Agree').sum(),
		results[item].str.match('Strongly Agree').sum()])
		stacked_bars_tab = stacked_bars_tab.append(pd.Series(item, index = ['simple', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree']), ignore_index=True)


##merge question text into data file and keep that instead of simple label
	stacked_bars_tab = stacked_bars_tab.merge(codebook, on = "simple", how = "left")
	stacked_bars_tab = stacked_bars_tab[['exported', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree']]
	
###creating column to sort on, sorting, then deleting
	stacked_bars_tab['sum_agree_percent'] = (stacked_bars_tab['Number strongly agree'] + stacked_bars_tab['Number agree'])/(stacked_bars_tab['Number strongly agree'] + stacked_bars_tab['Number agree'] + stacked_bars_tab['Number disagree'] + stacked_bars_tab['Number strongly disagree'])
    stacked_bars_tab = stacked_bars_tab.sort_values('sum_agree_percent')
	del stacked_bars_tab['sum_agree_percent']

##save file to folder
	stacked_bars_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_stacked_bars.csv')

#### END OF RESPECT SECTION #####

####KINDNESS SPECIFIC SECTION #######

else:
###create file of responses to "following through on commitment to respect"
	kinder_vals = [results['school_kinder_place'].str.match('Strongly Disagree').sum(),
	results['school_kinder_place'].str.match('Disagree').sum(),
	results['school_kinder_place'].str.match('Agree').sum(),
	results['school_kinder_place'].str.match('Strongly Agree').sum()]

	kinder_list = ['Strongly Disagree', 'Disagree', 'Agree', 'Strongly Agree']

	kinder_tab = pd.DataFrame({'response' : kinder_list, 'vals' : kinder_vals})

	kinder_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_kinder.csv')

###creating stacked bars subset by getting the specific columns included
	cols = list(results.columns)
	###not sure these numbers are right so check
	stacked_bars = cols[3:9] 
	stacked_bars.append('adults_care_all_students')

	stacked_bars_tab = pd.DataFrame(columns = ['simple', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree'])

	for item in stacked_bars:
		item = ([item, results[item].str.match('Strongly Disagree').sum(),
		results[item].str.match('Disagree').sum(),
		results[item].str.match('Agree').sum(),
		results[item].str.match('Strongly Agree').sum()])
		stacked_bars_tab = stacked_bars_tab.append(pd.Series(item, index = ['simple', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree']), ignore_index=True)


##merge question text into data file and keep that instead of simple label
	stacked_bars_tab = stacked_bars_tab.merge(codebook, on = "simple", how = "left")
	stacked_bars_tab = stacked_bars_tab[['exported', 'Number strongly disagree', 'Number disagree',	'Number agree',	'Number strongly agree']]

###creating column to sort on, sorting, then deleting
	stacked_bars_tab['sum_agree_percent'] = (stacked_bars_tab['Number strongly agree'] + stacked_bars_tab['Number agree'])/(stacked_bars_tab['Number strongly agree'] + stacked_bars_tab['Number agree'] + stacked_bars_tab['Number disagree'] + stacked_bars_tab['Number strongly disagree'])
	stacked_bars_tab = stacked_bars_tab.sort_values('sum_agree_percent')
	del stacked_bars_tab['sum_agree_percent']

##save file to folder
	stacked_bars_tab.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '_stacked_bars.csv')
'''