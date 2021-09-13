import pandas as pd
import numpy as np  
import os
import unicodedata
import math
import time
import glob


#A function that takes all the global result variables from the second group (the database_thing datasets) and creates a timestamped folder and then saves each one to that folder. Called from DatasetResultPage()

def SaveDatasetResults():
	if database_Used == 1:
		
		localtim= time.localtime(time.time())
		timestamp = str(localtim.tm_year) + '-'+ str(localtim.tm_mon) + '- '+ str(localtim.tm_mday) + '- ' + str(localtim.tm_hour) + '-' +str(localtim.tm_min) + '-' + str(localtim.tm_sec)  + "Results_Folder"
		try: 
			os.mkdir('./' + timestamp)
		except OSError:
			print("Can't create result folder")
		else:
			print("Result Folder created")
		
		
			m1name = './' + timestamp + '/module1_results.csv' 
			m2name ='./' + timestamp + '/module2_results.csv' 
			m3name ='./' + timestamp + '/module3_results.csv' 
			m4name ='./' + timestamp + '/module4_results.csv' 
			bestname ='./' + timestamp + '/bestcase_results.csv' 
			overallname ='./' + timestamp + '/overall_results.csv' 
			predictedname ='./' + timestamp + '/allvalues_results.csv' 
			coeff12name ='./' + timestamp + '/coefficients1and2_results.csv' 
			coeff34name ='./' + timestamp + '/coefficients3and4_results.csv' 
			correctname ='./' + timestamp + '/bestchosen_results.csv' 
			
			nml = database_correct.copy()
			sml = nml.sort_values(['Correct'], ascending=False)
			sml.to_csv(correctname, index=False, encoding='utf-8-sig')
			lml = database_predictedvalues.copy()
			mml = lml.sort_values(['Percentile Deviation'])
			
			mml.to_csv(predictedname, index=False, encoding='utf-8-sig')
			database_bestcase.to_csv(bestname, index=False, encoding='utf-8-sig')
			database_overall.to_csv(overallname, index=False, encoding='utf-8-sig')
			database_module1.to_csv(m1name, index=False, encoding='utf-8-sig')
			database_module2.to_csv(m2name, index=False, encoding='utf-8-sig')
			database_module3.to_csv(m3name, index=False, encoding='utf-8-sig')
			database_module4.to_csv(m4name, index=False, encoding='utf-8-sig')
			database_coefficients1and2.to_csv(coeff12name, index=False, encoding='utf-8-sig')
			database_coefficients3and4.to_csv(coeff34name, index=False, encoding='utf-8-sig')
		
	
	else:
		print("No Prediction has been run")

#Show the results of 'database_correct', part of DatasetResultPage()

def CorrectResult():
	if database_Used == 1:
		
		nml = database_correct.copy()
		sml = nml.sort_values(['Correct'], ascending=False)
		
		pd.set_option('display.max_rows',60)
		display(sml)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return
	
#Show the results of 'database_module1', part of DatasetResultPage()

def Module1Result():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_module1)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return


#Show the results of 'database_module2', part of DatasetResultPage()

def Module2Result():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_module2)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return

#Show the results of 'database_module3', part of DatasetResultPage()

def Module3Result():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_module3)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return


#Show the results of 'database_module4', part of DatasetResultPage()

def Module4Result():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_module4)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return


#Show the coefficients of 'database_coefficients1and2', part of DatasetResultPage()

def Coefficient12Result():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_coefficients1and2)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return

#Show the coefficients of 'database_coefficients3and4', part of DatasetResultPage()

def Coefficient34Result():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_coefficients3and4)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return

#Show the bestcase from 'database_bestcase', part of DatasetResultPage()

def BestCaseResult():
	if database_Used == 1:
			
		nml = database_bestcase.copy()
		sml = nml.sort_values(['Best module'])
		
		0
		pd.set_option('display.max_rows',60)
		display(sml)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return

#Show the overall results of 'database_overall', part of DatasetResultPage()

def OverallResult():
	if database_Used == 1:
		
		0
		pd.set_option('display.max_rows',60)
		display(database_overall)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return

#Show the coefficients of 'database_predictedvalues', part of DatasetResultPage()

def AllValuesResult():
	if database_Used == 1:
		
		nml = database_predictedvalues.copy()
		sml = nml.sort_values(['Percentile Deviation'])
	#print (sml)
	#display(dt)
		
		0
		pd.set_option('display.max_rows',60)
		display(sml)
	
	else:
		print("No Database or Dataset Prediction has been run")
	return

#The function called by PredictPage(), to display the results of the last OpenBoxPrediction done stored in predicted_results_open. 
def OpenResult():
	if p_r_o_Used == 1:
		
		display(predicted_results_open)
	
	else:
		print("No Box Office Prediction has been run")
	return

#The function called by  PredictPage(), to display the results of the last ClosedBoxPrediction done, stored in predicted_results_close.
def ClosedResult():
	if p_r_c_Used == 1:
		
		display(predicted_results_close)
	
	else:
		print("No Prediction has been run")

#The function called by  PredictPage(), to save the results of the last OpenBoxPrediction done, stored in predicted_results_open.
def SaveOpenResult():

	if p_r_o_Used == 1:
		
		dname = predicted_results_open.at[0, 'MovieName'] + 'BoxPredictResults.csv'
		predicted_results_open.to_csv(dname, index=False, encoding='utf-8-sig')
		print(dname, "has been made")
	
	else:
		print("No Box Office Prediction has been run")
	return

#The function called by  PredictPage(), to save the results of the last ClosedBoxPrediction done, stored in predicted_results_close.
def SaveClosedResult():
	
	if p_r_c_Used == 1:
		
		dname = predicted_results_close.at[0, 'MovieName'] + 'NoBoxResults.csv'
		predicted_results_close.to_csv(dname, index=False, encoding='utf-8-sig')
		print(dname, "has been made")
	
	else:
		print("No Prediction has been run")
	