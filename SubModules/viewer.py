import pandas as pd

#The function that runs in ViewResults() to show a csv file structure to a user. Mainly for results.
def ViewResults():
	name2= askopenfilename()
	print(name2)
	decf = pd.read_csv(name2)
	
	
	pd.set_option('display.max_rows',60)
	display(decf)
	return

#Functiom that runs in ViewResults() that allows a user to see the percentile averages of a module file. 
def ViewPercentileResults():
	name2= askopenfilename()
	print(name2)
	decf = pd.read_csv(name2)
	sum = 0.0
	rowCount = 0
	rowCount = decf.shape[0]

#for every movie, add the Percentile deviation, then once all deviations have been added, divide by total number of movies to get the average.
	for index,row in decf.iterrows():
		
		temp = decf.at[index, 'Percentile Deviation'].replace('[','')
		temp = temp.replace(']','')
		sum = sum + float(temp)
	
	display  ("Average Percentile Deviation", sum/rowCount)
	
		
	
	pd.set_option('display.max_rows',60)
	display(decf)
	return
