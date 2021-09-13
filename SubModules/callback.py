import pandas as pd 

#The initial function called by  DatasetPredictPage(), that selects the chosen csv file dataset as the set to be predicted by datasetPredict()	
def callbackDatasetPred():
	name2= askopenfilename()
	print(name2)
	print("Starting prediction on dataset in the chosen file")
	passedDS = pd.read_csv(name2)
	datasetPredict(passedDS)
    
	return name2

#The initial function called by  DatasetPredictPage(), that has the current database set in defaultdataset be predicted by datasetPredict()
def callbackDBPred():
	name2 = defaultdataset
	
	print("Starting prediction on current Database")
	datasetPredict(name2)
	return name2

#The initial function called by   PredictPage(), so that thee user can choose a single box office file for prediction for OpenBoxPrediction()
def callbackPredict():
	name2= askopenfilename()
	print(name2)
    
	OpenBoxPrediction(name2)
    
	return name2

#The initial function called by   PredictPage(), so that the user can choose a single no box office file for prediction for ClosedBoxPrediction()
def callbackPredict2():
	name2= askopenfilename()
	print(name2)
    
	ClosedBoxPrediction(name2)
    
	return name2