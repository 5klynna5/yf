# yf

	3. Clean data for Kindness, Courage, and Respect surveys:
		a. Run conemu at this path - C:\Programming_Projects\python_new\youth_frontiers
		b. Command in conemu: activate sammy_3
		c. 'python remove_completed_data.py' in conemu
		d. Check for blanks and weird numbers in 'attendance', 'school_id' and 'retreat_id' columns in new_data files in 'new survey exports' folder
		e. Open in sublime text / vscode-  C:\Programming_Projects\python_new\youth_frontiers\data_export_clean.py
		f. Change retreat variable at top for each ('courage', 'kindness', 'respect')
		g. Command in conemu: python data_export_clean.py (run for each retreat type)
	4. Concatenate all survey counts data by running in command line - python concat_results_counts.py
	5. Enter current survey response counts in Evaluation Retreat List (google spreadsheet) from count_responses_ALL_[date].csv in this folder - C:\Users\KLA\Documents\Evaluation Projects\Youth Frontiers\Surveys\survey response counts
	6. Send count_responses_ALL_NEW_[date].csv to David Wasserman @ Youth Frontiers
	

For individual survey reports:

	1. Create list of retreats to analyze for today's date in the folder
Create files for analysis from that list (change date at top if necessary)  - in conemu run python analyze_retreat_data.py
