
import pandas as pd
import os, sys
print(pd.__version__)
import datetime as dt     
date = dt.datetime.today().strftime("%m%d%Y")
###this code functions using today's date as the date the export was saved
#######redefine date below if using a different one

##you need to create this file of the retreats for analysis today and save in the correct format
retreats_today_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\lists of retreats to analyze\\retreats_to_analyze_' + date + '.csv'
retreats_today = pd.read_csv(retreats_today_path, encoding = "ISO-8859-1")

#date = '01272018'
###this goes through data frame above and does the analysis for each row in that dataframe
for index, row in retreats_today.iterrows():

	retreat_num = row['retreat_id']
	retreat = row['retreat']
	school = row['school_id']

####ACTION REQUIRED! You need to put in retreat_id, retreat type, and school_id here that you want to analyze
	#retreat_num = 69063
	#retreat = 'kindness'
	#school = 20701

###using file of school names with ids to grab school name to add to the file names being exported
	school_and_id_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\schools_and_ids_sp18.csv'
	school_and_id = pd.read_csv(school_and_id_path, encoding = "ISO-8859-1")
	school_name = school_and_id.loc[school_and_id['school_id'] == school, 'school_name'].iloc[0]

	school_name = school_name.replace('/', '-')

##load in codebook to get question text for reporting
	codebook_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\' + retreat + '_survey_column_book.csv'
	codebook = pd.read_csv(codebook_path, encoding = "ISO-8859-1")

##load in cleaned data file
	results_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\cleaned survey exports\\' + retreat + '_data_clean_' + date + '.csv'
	results = pd.read_csv(results_path, encoding = "ISO-8859-1")


##create data frame of just the retreat id you are analyzing
	results = results.loc[(results['retreat_id'] == retreat_num) & (results['school_id'] == school)]

#delete extra index column
	del results['Unnamed: 0']

##make folder for files to go in for this retreat
	if len(results) > 0:
		folder = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\retreat files for analysis\\' + retreat + '_retreat_' + str(retreat_num)
		if not os.path.exists(folder):
			os.mkdir(folder)
#save the data frame of data for this retreat
		results.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '.csv')

###### FOR ALL RETREATS #######

###responses and attendance

#get the attendance by pulling the most frequently occuring number in the attendance column
##when this is empty has serious error. What do I do?
		if results['attendance'].notnull().values.any():
			total_attend = results['attendance'].value_counts().idxmax()
		else:
			total_attend = 0
		n = len(results)
		#n_respond = total_attend - n

		responses = [n, total_attend]
		responses_tab = pd.DataFrame(columns = ['n', 'total_attend'])
		responses_tab = responses_tab.append(pd.Series(responses, index = ['n', 'total_attend']), ignore_index = True)
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

		if retreat == 'courage':

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

##add the retreats analyzed to completed analyses DataFrames

today_complete_simple = retreats_today[['school_id', 'attendance', 'retreat_id']]

old_complete_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\lists of analyses completed\\completed_analyses.csv'
old_complete_simple = pd.read_csv(old_complete_path, encoding = "ISO-8859-1")

total_complete_simple = pd.concat([today_complete_simple, old_complete_simple])
#total_complete_simple = total_complete_simple.drop_duplicates()

today_complete_simple.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\lists of analyses completed\\completed_analyses_' + date + '.csv')
today_complete_simple.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\lists of analyses completed\\completed_analyses.csv')


###for dropbox

###this goes through data frame above and does the analysis for each row in that dataframe
for index, row in retreats_today.iterrows():

	retreat_num = row['retreat_id']
	retreat = row['retreat']
	school = row['school_id']

####ACTION REQUIRED! You need to put in retreat_id, retreat type, and school_id here that you want to analyze
	#retreat_num = 69063
	#retreat = 'kindness'
	#school = 20701

###using file of school names with ids to grab school name to add to the file names being exported
	school_and_id_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\schools_and_ids_sp18.csv'
	school_and_id = pd.read_csv(school_and_id_path, encoding = "ISO-8859-1")
	school_name = school_and_id.loc[school_and_id['school_id'] == school, 'school_name'].iloc[0]

	school_name = school_name.replace('/', '-')

##load in codebook to get question text for reporting
	codebook_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\' + retreat + '_survey_column_book.csv'
	codebook = pd.read_csv(codebook_path, encoding = "ISO-8859-1")

##load in cleaned data file
	results_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\cleaned survey exports\\' + retreat + '_data_clean_' + date + '.csv'
	results = pd.read_csv(results_path, encoding = "ISO-8859-1")


##create data frame of just the retreat id you are analyzing
	results = results.loc[(results['retreat_id'] == retreat_num) & (results['school_id'] == school)]

#delete extra index column
	del results['Unnamed: 0']
##make folder for files to go in for this retreat
	if len(results) > 0:
		folder = 'C:\\Users\\KLA\\Dropbox\\Youth Frontiers\\retreat files for analysis\\' + retreat + '_retreat_' + str(retreat_num)
		if not os.path.exists(folder):
			os.mkdir(folder)
#save the data frame of data for this retreat
		results.to_csv(folder + '\\' + retreat + '_retreat_' + str(retreat_num) + '_' + school_name + '.csv')

###### FOR ALL RETREATS #######

###responses and attendance

#get the attendance by pulling the most frequently occuring number in the attendance column
##when this is empty has serious error. What do I do?
		if results['attendance'].notnull().values.any():
			total_attend = results['attendance'].value_counts().idxmax()
		else:
			total_attend = 0
		n = len(results)
		#n_respond = total_attend - n

		responses = [n, total_attend]
		responses_tab = pd.DataFrame(columns = ['n', 'total_attend'])
		responses_tab = responses_tab.append(pd.Series(responses, index = ['n', 'total_attend']), ignore_index = True)
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

		if retreat == 'courage':

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

