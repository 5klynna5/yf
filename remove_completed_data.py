import pandas as pd
print(pd.__version__)
import datetime as dt     
date = dt.datetime.today().strftime("%m%d%Y")
from glob import glob
import os
###this code functions using today's date as the date the export was saved
#######redefine date below if using a different one
#date = '11062017'


completed_retreats = [69171.0, 68856.0, 68980.0, 69046.0, 69061.0, 69066.0, 69067.0, 69073.0, 69097.0, 69106.0, 69114.0, 69126.0, 69135.0, 69163.0, 69174.0, 69187.0, 69202.0, 69231.0, 69231.0, 69234.0, 69235.0, 69236.0, 69237.0, 69239.0, 69245.0, 69253.0, 69254.0, 69258.0, 69292.0, 69311.0, 69327.0, 69331.0, 69357.0, 69371.0, 69385.0, 69443.0, 69507.0, 69560.0, 69579.0, 69648.0, 69710.0, 69710.0, 69746.0, 69775.0, 69778.0, 70031.0, 70092.0, 70120.0, 70259.0, 70351.0, 70360.0, 70361.0, 70435.0, 70473.0, 70565.0, 70617.0, 69238.0, 69010.0, 70177.0, 68791.0, 68859.0, 68983.0, 68988.068990.0 69004.0 69013.0 69018.0 69028.0 69040.0 69041.0 69045.0 69057.0 69063.0 69063.0 69063.0 69063.0 69072.0 69104.0 69111.0 69167.0 69185.0 69204.0 69259.0 69261.0 69262.0 69263.0 69264.0 69275.0 69277.0 69279.0 69280.0 69287.0 69297.0 69309.0 69313.0 69326.0 69328.0 69334.0 69340.0 69343.0 69343.0 69356.0 69380.0 69391.0 69395.0 69947.0 70065.0 70352.0 70355.0 70425.0 70425.0 69339.0 68888.0 69026.0 69031.0 69058.0 69080.0 69113.0 69115.0 69134.0 69160.0 69192.0 69192.0 69212.0 69217.0 69219.0 69276.0 69283.0 69286.0 69312.0 69363.0 69368.0 69381.0 69448.0 69573.0 69573.0 69878.0 69937.0 70121.0 70124.0 70212.0 70297.0 70400.0 70749.0 69186.0]

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
