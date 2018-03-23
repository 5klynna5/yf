import pandas as pd
print(pd.__version__)
import datetime as dt     
date = dt.datetime.today().strftime("%m%d%Y")
from glob import glob
import os
###this code functions using today's date as the date the export was saved
#######redefine date below if using a different one
#date = '11062017'

path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\final retreat reports'
files = glob(path + '/*.pdf')
completed_retreats = []
for item in files:
	filename = os.path.basename(item)
	filename = filename.split('_')[1]
	completed_retreats.append(filename)

completed_retreats = list(map(float,completed_retreats))
print(completed_retreats)


###ACTION REQUIRED HERE! - add in the name of retreat here, either 'respect', 'courage', or 'kindness'
retreat_types = ['courage', 'kindness', 'respect']

for item in retreat_types:
	retreat = item
	results_path = 'C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\survey results downloads\\' + retreat + '_results_export_' + date +'.csv'
	results = pd.read_csv(results_path, encoding = "UTF-8")
	results['school_id'] = pd.to_numeric(results['school_id'], errors = 'coerce')
	results['retreat_id'] = pd.to_numeric(results['retreat_id'], errors = 'coerce')
	results['school_id'] = results['school_id'].replace([257058,26705], 25705)
	results['school_id'] = results['school_id'].replace([21233, 222222000000, 212438], 21243)
	results['school_id'] = results['school_id'].replace(220835, 20835)

	print(len(results))
	
	results_new = results.loc[~results['retreat_id'].isin(completed_retreats)]

	###try this approach next time

	print(results_new['retreat_id'].value_counts())

	results_new.to_csv('C:\\Users\\KLA\\Documents\\Evaluation Projects\\Youth Frontiers\\Surveys\\new survey exports\\' + retreat + '_data_new_' + date + '.csv')
