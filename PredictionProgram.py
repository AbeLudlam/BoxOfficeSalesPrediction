#!/usr/bin/python3
#Created by Abraham Ludlam
#Box Office Sales prediction program using multiple linear regression. Predicts sales of movies.

from tkinter import *
import pandas as pd
import numpy as np  
import os
import re 
import glob
import sys
import unicodedata
import math
import time
from textblob import TextBlob
import pymysql
import mysql.connector as mariadb
from sqlalchemy import create_engine

import SubModules.callback as callback
import SubModules.results as results
import SubModules.tweetActs as tweetActs
import SubModules.updateDB as updateDB
import SubModules.viewer as resultsView

from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import mean_absolute_error
from tkinter   import filedialog   
from tkinter.filedialog import askopenfilename
#for sql script its 'source 'path_to_script''
LARGE_FONT= ("Verdana", 18)
Fine_font= ('Helvetica', 15)
small_font= ('Helvetica', 12)


db_connection = 'mysql+pymysql://Predaccount:pass@localhost/linearReg'
dbc= create_engine(db_connection)
mydb = pd.read_sql('select * from maindata', con=dbc)

tempDB = pd.DataFrame(columns = ["MovieName", "PositiveTweets", 	"NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", 	"PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", 	"NeutralReplies","NegativeReplies", "Budget", "BoxOfficeSales", "ProfitPercentage"])

for index,row in mydb.iterrows():
	tempDB.loc[index] = [mydb.at[ index, "MovieName"]] + [mydb.at[ index, "PT"]] + [mydb.at[ index, "NT"]] + [mydb.at[ index, "NEGT"]] +  [mydb.at[ index, "PF"]] +  [mydb.at[ index, "NF"]] +   [mydb.at[ index, "NEGF"]] +  [mydb.at[ index, "PRT"]] +   [mydb.at[ index, "NRT"]] +  [mydb.at[ index, "NEGRT"]] +  [mydb.at[ index, "PRL"]] +  [mydb.at[ index, "NRL"]]  +  [mydb.at[ index, "NEGRL"]] +  [mydb.at[ index, "Budget"]] +  [mydb.at[ index, "Box"]] + [mydb.at[ index, "PROFIT"]]


defaultdataset = tempDB



ListofCSVS = {"firstCSV": '', "secondCSV": ''}

predicted_results_open = pd.DataFrame(columns = ["MovieName", "Module 1",  "Module 2",   "Module 3",   "Module 4", "Best Module", "Chosen Module", "Predicted Sales", "Actual Sales", "Percentile Deviation"])


p_r_o_Used = 0
predicted_results_close = pd.DataFrame(columns = ["MovieName", "Module 1",  "Module 2",   "Module 3",   "Module 4", "Chosen Module", "Predicted Sales"])


p_r_c_Used = 0

database_module1 = pd.DataFrame(columns = ["MovieName", "Actual", "Module 1 Prediction", "Percentile Deviation", 'Best'])
database_module2 = pd.DataFrame(columns = ["MovieName", "Actual", "Module 2 Prediction", "Percentile Deviation",  'Best'])
database_module3 = pd.DataFrame(columns = ["MovieName", "Actual", "Module 3 Prediction", "Percentile Deviation",  'Best'])
database_module4 = pd.DataFrame(columns = ["MovieName", "Actual", "Module 4 Prediction", "Percentile Deviation",  'Best'])
database_coefficients1and2 =  pd.DataFrame(columns = ['Coefficients',"Module 1", "Module 2"])
database_coefficients3and4 =  pd.DataFrame(columns = ['Coefficients',"Module 3", "Module 4"])
database_predictedvalues =  pd.DataFrame(columns =["MovieName", "Module 1" ,  "Module 2",  "Module 3",  "Module 4",  "Predicted Module","Best", "Predicted Value", 'Actual', "Percentile Deviation" ])
database_correct = pd.DataFrame(columns =["MovieName", "Correct"])
database_bestcase = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted", "Percentile Deviation", "Best module"])
database_overall =  pd.DataFrame(columns =["Total Movies", "Best Cases chosen", "Best Case Percentile Deviation", "Best Case MAE", "Predicted Percentile Deviation", "Predicted MAE"])

database_Used = 0 


#The initial start up of the tkinter windows. All page layouts are defined here. Basically it keeps track of the windows that can appear in the program. 
class SeaofBTCapp(Tk):

	def __init__(self, *args, **kwargs):
        
		Tk.__init__(self, *args, **kwargs)
		container = Frame(self)

		container.pack(side="top", fill="both", expand = True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure((0,1), weight=1)

		self.frames = {}

		for F in (StartPage, SentimentPage, PredictPage, BoxSentimentPage, NoBoxSentimentPage, CombinePage, DatasetPredictPage, UpdatePage, DatasetResultPage, ViewResultPage):

			frame = F(container, self)

			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")
			

		self.show_frame(StartPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

#The start menu, that links to every other page and its function.  
class StartPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Start Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

     
		button= Button(self, text='Run the Database or another File', font=Fine_font, command=lambda: controller.show_frame(DatasetPredictPage))
		button.pack(pady=15,padx=15)
		
		
		button2= Button(self, text='Select Twitter dataset to apply sentiment', font=Fine_font, command=lambda: controller.show_frame(SentimentPage))
		button2.pack(pady=15,padx=15)

		button3= Button(self, text='Predict a Movie\'s Box Office', font=Fine_font, command=lambda: controller.show_frame(PredictPage))
		button3.pack(pady=15,padx=15)

		button5= Button(self, text='Combine datasets', font=Fine_font, command=lambda: controller.show_frame(CombinePage))
		button5.pack(pady=15,padx=15)

		button6= Button(self, text='Update the database', font=Fine_font, command=lambda: controller.show_frame(UpdatePage))
		button6.pack(pady=15,padx=15)

		button7= Button(self, text='Read a Result file', font=Fine_font, command=lambda: controller.show_frame(ViewResultPage))
		button7.pack(pady=15,padx=15)
		

		#button10= Button(self, text='Exit', font=Fine_font, command= lambda: exi(self))
		#button10.pack(side = BOTTOM)

#A page that lets the user see the structure of any CSV file, mainly for the use of seeing result files either with ViewResults() or ViewPercentileResults()     
class ViewResultPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="View Result Files", font=LARGE_FONT)
		label.pack(pady=10,padx=10)
		
		button= Button(self, text='Choose a Results file to view its contents',  font=Fine_font, command=ViewResults)
		button.pack(pady=40,padx=40)
		button2= Button(self, text='Choose a module file to gets its average Percentile Deviation and other values',  font=Fine_font, command=ViewPercentileResults)
		button2.pack(pady=40,padx=40)
		button3= Button(self, text='Back to main menu',  font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)


#The page where a user can update the main database with callbackUpdateDB(): or replace the database with  callbackRewriteDB():
class UpdatePage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Choose file to update database with", font=LARGE_FONT)
		label.pack(pady=20,padx=20)

     
		button= Button(self, text='Update database with a single entry (Sentiment.csv or Box.csv file)',  font=Fine_font, command=callbackUpdateDB)
		button.pack(pady=20,padx=20)
		
		
		button2= Button(self, text='Rewrite the database to have a file act as the new default database',  font=Fine_font, command=callbackRewriteDB)
		button2.pack(pady=20,padx=20)

		button3= Button(self, text='Back to main menu',  font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)


#The page where a user can predict for every movie in the database, a dataset, or to see the results. For prediction, datasetPredict() is used, and to see results is DatasetResultPage()

class DatasetPredictPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Choose file to use for prediction", font=LARGE_FONT)
		label.pack(pady=20,padx=20)

     		
		button2= Button(self, text='See the prediction statistics for the current database',  font=Fine_font, command=callbackDBPred).pack()

		button= Button(self, text='See the prediction statistics for a file that is a dataset of movies',  font=Fine_font, command=callbackDatasetPred).pack()
		
		

		button4= Button(self, text='See the most recent results from a run',  font=Fine_font, command=lambda: controller.show_frame(DatasetResultPage)).pack()

		

		label3 = Label(self, text="There are 4 linear regressions modules total. Modules 1 and 2 have 13 coefficients. Modules 3 and 4 have 4", font=small_font)
		label3.pack(pady=10,padx=10)
		label4 = Label(self, text="Module 1 predicts the Percentage of profit based on the number of positive, negative, and neutral tweets, replies, retweets, and favorites.", font=small_font)
		label4.pack(pady=10,padx=10)
		label5 = Label(self, text="Module 2 predicts the  of Box Number Sales based on the number of positive, negative, and neutral tweets, replies, retweets, and favorites.", font=small_font)
		label5.pack(pady=10,padx=10)

		label6 = Label(self, text="Module 3 predict the Percentage of Profit purely based on the combined total of positive, negative, and neutral Twitter interactions.", font=small_font)
		label6.pack(pady=10,padx=10)
		label7 = Label(self, text="Module 4 predict the Box Office Sales purely based on the combined total of positive, negative, and neutral Twitter interactions.", font=small_font)		
		label7.pack(pady=10,padx=10)
		button3= Button(self, text='Back to main menu',  font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)

#Function to exit the program and windows for the none jupyter notebook version.	
def exi(sel):
	sel.destroy()
	
#The page that allows a user to choose whether they want to apply sentiment to a dataset and give the box office, or to a dataset and don't give box office. BoxSentimentPage() and NoBoxSentimentPage() are the linked pages.
class SentimentPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Choose Twitter dataset to apply sentiment and count values", font=LARGE_FONT)
		label.pack(pady=20,padx=20)

     
		button= Button(self, text='Twitter dataset plus Box Office Values',  font=Fine_font, command=lambda: controller.show_frame(BoxSentimentPage))
		button.pack(pady=20,padx=20)
		
		
		button2= Button(self, text='Twitter dataset without Box Office Values',  font=Fine_font, command=lambda: controller.show_frame(NoBoxSentimentPage))
		button2.pack(pady=20,padx=20)
	
		button3= Button(self, text='Back to main menu',  font=Fine_font,command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)

#Page that has 3 text fields for a user to input the Name of the movie, the budget of the movie, and the box office a movie. Once done, the inside Twitcall() function is called, which takes the chosen twitter dataset and applies sentiment to it and then counts the totals for all relevant values.
class BoxSentimentPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Sentiment Page", font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		
		def Twitcall():
			
			csvD = askopenfilename()
			print(csvD)
			decf = pd.read_csv(csvD)
			decf['movie'] = MovName.get()
			decf['Sentiment'] = 'neutral'

			for index,row in decf.iterrows():
	
				decf.at[index, 'Sentiment'] = get_tweet_sentiment(row['content'])
			#twitGeter(name2)
			print("Done applying Sentiment, now counting")
			pt = 0
			prt = 0
			pf = 0
			prl = 0
			negt = 0
			negrt = 0
			negf = 0
			negrl = 0
			neut = 0
			neurt = 0
			neuf = 0
			neurl = 0

			lop = pd.DataFrame(columns = ["MovieName", "PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget", "BoxOfficeSales", "ProfitPercentage"])

			for index,row in decf.iterrows():
	
				if decf.at[index, 'Sentiment'] == 'positive':
					pt = pt + 1
					if (math.isnan(float(decf.at[index, 'replies'])) == False):
						prl = prl + float(decf.at[index, 'replies'])
					if (math.isnan(float(stringparser(decf.at[index, 'favorites']))) == False):
						pf = pf + float(stringparser(decf.at[index, 'favorites']))
					if (math.isnan(float(stringparser(decf.at[index, 'retweets']))) == False):
						prt = prt + float(stringparser(decf.at[index, 'retweets']))

				elif  decf.at[index, 'Sentiment'] == 'negative':
					negt = negt + 1
					if (math.isnan(float(decf.at[index, 'replies'])) == False):
						negrl = negrl + float(decf.at[index, 'replies'])
					if (math.isnan(float(stringparser(decf.at[index, 'favorites']))) == False):
						negf = negf + float(stringparser(decf.at[index, 'favorites']))
					if (math.isnan(float(stringparser(decf.at[index, 'retweets']))) == False):
						negrt = negrt + float(stringparser(decf.at[index, 'retweets']))

				else:
					neut = neut + 1
					if (math.isnan(float(decf.at[index, 'replies'])) == False):
						neurl = neurl + float(decf.at[index, 'replies'])
					if (math.isnan(float(stringparser(decf.at[index, 'favorites']))) == False):
						neuf = neuf + float(stringparser(decf.at[index, 'favorites']))
					if (math.isnan(float(stringparser(decf.at[index, 'retweets']))) == False):
						neurt = neurt + float(stringparser(decf.at[index, 'retweets']))

			profit= (float(BoxOfficeIn.get())) / (float(BudgetIn.get()))
			lop.loc[0] = [decf.at[0, 'movie']] + [pt] + [neut] + [negt] + [pf] + [neuf] + [negf] + [prt] + [neurt] + [negrt] + [prl] + [neurl] + [negrl] + [BudgetIn.get()] + [BoxOfficeIn.get()] + [profit]		
			dname = decf.at[0,'movie'] + "Sentiment.csv"
			lop.to_csv(dname, index=False, encoding='utf-8-sig')	
			print("File", dname, "has been created")
			return 0
			
		MovName = StringVar()
		label3 = Label(self, text="Movie Name", font=Fine_font).pack(side=TOP)
		e = Entry(self, width=25, justify = CENTER, font=Fine_font,textvariable= MovName).pack(side=TOP)
		BudgetIn = StringVar()
		label3 = Label(self, text="Budget", font=Fine_font).pack(side=TOP)
		e1 = Entry(self, width=25, justify = CENTER, font=Fine_font,textvariable= BudgetIn).pack(side=TOP)
		BoxOfficeIn = StringVar()
		label3 = Label(self, text="Box Office Sales", font=Fine_font).pack(side=TOP)
		e2 = Entry(self, width=25, justify = CENTER, font=Fine_font, textvariable= BoxOfficeIn).pack(side=TOP)
		button2 = Button(self, text="Choose File and submit",  font=Fine_font, command= Twitcall).pack()

		label7 = Label(self, text="Choose a regular twitter data set file that are seen in the format \"~.csv\", where ~ is a movie name", font=LARGE_FONT)
		label7.pack(pady=20,padx=20)
		button3= Button(self, text='Back to main menu',  font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)

#The same as BoxSentimentPage(), just now only two text fields as box office is no longer inputted. The functionality is the same.

class NoBoxSentimentPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Sentiment Page", font=LARGE_FONT)
		label.pack(pady=5,padx=5)

		
		def Twitcall():
			
			csvD = askopenfilename()
			print(csvD)
			decf = pd.read_csv(csvD)
			decf['movie'] = MovName.get()
			decf['Sentiment'] = 'neutral'

			for index,row in decf.iterrows():
	
				decf.at[index, 'Sentiment'] = get_tweet_sentiment(row['content'])
			#twitGeter(name2)
			print("Done applying Sentiment, now counting")
			pt = 0
			prt = 0
			pf = 0
			prl = 0
			negt = 0
			negrt = 0
			negf = 0
			negrl = 0
			neut = 0
			neurt = 0
			neuf = 0
			neurl = 0

			lop = pd.DataFrame(columns = ["MovieName", "PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"])

			for index,row in decf.iterrows():
	
				if decf.at[index, 'Sentiment'] == 'positive':
					pt = pt + 1
					if (math.isnan(float(decf.at[index, 'replies'])) == False):
						prl = prl + float(decf.at[index, 'replies'])
					if (math.isnan(float(stringparser(decf.at[index, 'favorites']))) == False):
						pf = pf + float(stringparser(decf.at[index, 'favorites']))
					if (math.isnan(float(stringparser(decf.at[index, 'retweets']))) == False):
						prt = prt + float(stringparser(decf.at[index, 'retweets']))

				elif  decf.at[index, 'Sentiment'] == 'negative':
					negt = negt + 1
					if (math.isnan(float(decf.at[index, 'replies'])) == False):
						negrl = negrl + float(decf.at[index, 'replies'])
					if (math.isnan(float(stringparser(decf.at[index, 'favorites']))) == False):
						negf = negf + float(stringparser(decf.at[index, 'favorites']))
					if (math.isnan(float(stringparser(decf.at[index, 'retweets']))) == False):
						negrt = negrt + float(stringparser(decf.at[index, 'retweets']))

				else:
					neut = neut + 1
					if (math.isnan(float(decf.at[index, 'replies'])) == False):
						neurl = neurl + float(decf.at[index, 'replies'])
					if (math.isnan(float(stringparser(decf.at[index, 'favorites']))) == False):
						neuf = neuf + float(stringparser(decf.at[index, 'favorites']))
					if (math.isnan(float(stringparser(decf.at[index, 'retweets']))) == False):
						neurt = neurt + float(stringparser(decf.at[index, 'retweets']))

			
			lop.loc[0] = [decf.at[0, 'movie']] + [pt] + [neut] + [negt] + [pf] + [neuf] + [negf] + [prt] + [neurt] + [negrt] + [prl] + [neurl] + [negrl] + [BudgetIn.get()]		
			dname = decf.at[0,'movie'] + "NoSaleSentiment.csv"
			lop.to_csv(dname, index=False, encoding='utf-8-sig')	
			print("File", dname, "has been created")
			return 0
			
		MovName = StringVar()
		label2 = Label(self, text="MovieName", font=Fine_font).pack(side=TOP)
		e = Entry(self, width=25, font=Fine_font, justify = CENTER, textvariable= MovName).pack(side = TOP)
		
		BudgetIn = StringVar()
		label3 = Label(self, text="Budget", font=Fine_font).pack(side=TOP)
		e1 = Entry(self, width=25, justify = CENTER, font=Fine_font,textvariable= BudgetIn).pack(side=TOP)
		
		button2 = Button(self, text="Choose File and submit",  font=Fine_font, command= Twitcall).pack()
		label7 = Label(self, text="Choose a regular twitter data set file that are seen in the format \"~.csv\", where ~ is a movie name", font=LARGE_FONT).pack()
		button3= Button(self, text='Back to main menu',  font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)
		
		

#The page that allows a user to combine two datasets of the same shape by choosing them and then uses the Comcall() inner function to combine them.
class CombinePage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Choose Twitter dataset to apply sentiment and count values", font=LARGE_FONT)
		label.pack(pady=20,padx=20)

		def Comcall():
			
			fd = pd.read_csv(ListofCSVS['firstCSV'])
			sd = pd.read_csv(ListofCSVS['secondCSV'])
			combined_csv = pd.concat([fd, sd])
			dname = ListofCSVS['firstCSV'].replace('.csv', 'Combined.csv')
			#fname = dname + "Combined" 
			combined_csv.to_csv(dname, index=False, encoding='utf-8-sig')
			print("Files have been combined into", dname)
     
		button= Button(self, text='Choose first CSV file to combine',  font=Fine_font, command=lambda *args: getCSV('firstCSV'))
		button.pack(pady=15,padx=15)
		
		
		button2= Button(self, text='Choose second CSV file to combine', font=Fine_font,   command=lambda *args : getCSV('secondCSV'))
		button2.pack(pady=15,padx=15)
		
		button4 = Button(self, text="Combine", font=Fine_font, command= Comcall)
		button4.pack(pady=15,padx=15)
	
		button3= Button(self, text='Back to main menu', font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack(side = BOTTOM)

#The page that connects to DatasetPredictPage() to show all the results from the previous dataset prediction. Uses SaveDatasetResults() to save all results to a file.

class DatasetResultPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Choose which result you want to see", font=LARGE_FONT)
		label.pack(pady=20,padx=20)

     
		button= Button(self, text='See all the values', font=small_font, command=AllValuesResult).pack()
		
		
		button2= Button(self, text='Module 1 Values', font=small_font, command=Module1Result).pack()
		
		button9= Button(self, text='Module 2 Values', font=small_font, command=Module2Result).pack()
	
		button10= Button(self, text='Module 3 Values', font=small_font, command=Module3Result).pack()

		button11= Button(self, text='Module 4 Values', font=small_font, command=Module4Result).pack()

		button5= Button(self, text='Show results for the best case scenario', font=small_font, command=BestCaseResult).pack()
		
		
		button4= Button(self, text='See overall results', font=small_font, command= OverallResult).pack()
	
		
		
		button7= Button(self, text='See coefficients for module 1 and 2', font=small_font, command=Coefficient12Result).pack()
		
		button8= Button(self, text='See coefficients for module 3 and 4', font=small_font, command=Coefficient34Result).pack()

		button15= Button(self, text='See the movies that were correctly predicted their best module', font=small_font, command=CorrectResult).pack()
	
		button13= Button(self, text='Create a timestamped folder to save results', font=small_font, command=SaveDatasetResults).pack()

		

		button3= Button(self, text='Back to main menu', font=small_font, command=lambda: controller.show_frame(StartPage)).pack()



#The prediction function of the entire program. A more in depth explanation of it is in the 'Dataset_Predict_comments.py" file. All global 'database_name' variables are used and obtain values here. Both  callbackDBPred(): and  callbackDatasetPred(), send files to it.
def datasetPredict(csvF):
	dataset = csvF.copy()
	#print(dataset)
	global database_correct
	global database_predictedvalues
	global database_bestcase
	global database_overall
	global database_Used 
	global database_module1
	global database_module2
	global database_module3
	global database_module4
	global database_coefficients1and2
	global database_coefficients3and4
	if database_Used == 1:
		database_overall = database_overall.drop([0],axis = 0)
		for index,row in database_module1.iterrows():
			database_module1 =  database_module1.drop([index], axis=0)
			database_module2 =  database_module2.drop([index], axis=0)
			database_module3 =  database_module3.drop([index], axis=0)
			database_module4 =  database_module4.drop([index], axis=0)
			database_bestcase = database_bestcase.drop([index], axis=0)
			database_correct = database_correct.drop([index], axis=0)
			database_predictedvalues = database_predictedvalues.drop([index], axis=0)
		for index,row in database_coefficients1and2.iterrows():
			database_coefficients1and2 = database_coefficients1and2.drop([index], axis=0)
		
		for index,row in database_coefficients3and4.iterrows():
			database_coefficients3and4 = database_coefficients3and4.drop([index], axis=0)
	pol = 0.0
	rowCount = 0
	rowCount = dataset.shape[0]
	
	
	dataset.loc[rowCount] = ["Control"] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + 	[pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol]
	inet = 0
	inet = rowCount + 1
	while inet < rowCount*10:
		dataset.loc[inet]= ["Control"] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + 	[pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol]
	#print('COntrol')
		inet = inet + 1

	temp = pd.DataFrame(columns = ["MovieName", "PositiveTweets", 	"NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", 	"PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", 	"NeutralReplies","NegativeReplies", "Budget", "BoxOfficeSales", "ProfitPercentage"])

	new = pd.DataFrame(columns = ["MovieName", "Positive", "Negative" , "Neutral", "Budget", "BoxOfficeSales", "ProfitPercentage"])

	temp2 = pd.DataFrame(columns = ["MovieName", "Positive", "Negative" , "Neutral", "Budget", "BoxOfficeSales", "ProfitPercentage"])
	inet = 0
	while inet < rowCount*10:
		new.loc[inet] = [dataset.at[inet, "MovieName"]] + [(dataset.at[inet, "PositiveTweets"] + dataset.at[inet, "PositiveFavorites"] + dataset.at[inet, "PositiveRetweets"] + dataset.at[inet, "PositiveReplies"])] + [(dataset.at[inet, "NegativeTweets"] + dataset.at[inet, "NegativeFavorites"] + dataset.at[inet, "NegativeRetweets"] + dataset.at[inet, "NegativeReplies"])] + [(dataset.at[inet, "NeutralTweets"] + dataset.at[inet, "NeutralFavorites"] + dataset.at[inet, "NeutralRetweets"] + dataset.at[inet, "NeutralReplies"])] +   [dataset.at[ inet, "Budget"]] +  [dataset.at[ inet, "BoxOfficeSales"]] + [dataset.at[ inet, "ProfitPercentage"]]
		#if inet < rowCount:
		#	print (new.loc[inet]) 
		inet = inet + 1
	#new.describe()
	
	df = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted"])
	predf = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted"])
	M2predf =  pd.DataFrame(columns = ["MovieName", "Actual", "Module 2 Prediction","Percentile Deviation", 'Best'])
	M1predf = pd.DataFrame(columns = ["MovieName", "Actual", "Module 1 Prediction", "Percentile Deviation",'Best'])
	M3predf =  pd.DataFrame(columns = ["MovieName", "Actual", "Module 3 Prediction", "Percentile Deviation", 'Best'])
	M4predf = pd.DataFrame(columns = ["MovieName", "Actual", "Module 4 Prediction",  "Percentile Deviation", 'Best'])
	predicted_values =  pd.DataFrame(columns = ["MovieName", "Module 1", "M1 Ranking",  "Module 2", "M2 Ranking",  "Module 3", "M3 Ranking",  "Module 4", "M4 Ranking"])
	Best_modules =  pd.DataFrame(columns = ["MovieName", "Module 1" ,  "Module 2",  "Module 3",  "Module 4", "Best"])
	Module12Coeff =  pd.DataFrame(columns = ["Module 1", "Module 2"])
	ModuleCoeff13 =  pd.DataFrame(columns = ['Coefficients',"Module 1", "Module 2"])
	Module34Coeff =  pd.DataFrame(columns = ["Module 3", "Module 4"])
	ModuleCoeff4 =  pd.DataFrame(columns = ['Coefficients',"Module 3", "Module 4"])

#print(temp.loc[0])


	iterations = 0

	while iterations < rowCount:
	
		temp.loc[0] = [dataset.at[ iterations, "MovieName"]] + [dataset.at[ iterations, "PositiveTweets"]] + [dataset.at[ iterations, "NeutralTweets"]] + [dataset.at[ iterations, "NegativeTweets"]] +  [dataset.at[ iterations, "PositiveFavorites"]] +  [dataset.at[ iterations, "NeutralFavorites"]] +   [dataset.at[ iterations, "NegativeFavorites"]] +  [dataset.at[ iterations, "PositiveRetweets"]] +   [dataset.at[ iterations, "NeutralRetweets"]] +  [dataset.at[ iterations, "NegativeRetweets"]] +  [dataset.at[ iterations, "PositiveReplies"]] +  [dataset.at[ iterations, "NeutralReplies"]]  +  [dataset.at[ iterations, "NegativeReplies"]] +  [dataset.at[ iterations, "Budget"]] +  [dataset.at[ iterations, "BoxOfficeSales"]] + [dataset.at[ iterations, "ProfitPercentage"]] 
		X_test = temp[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
		y_test = temp["ProfitPercentage"].values
		trainset = dataset
		trainset = trainset.drop([iterations], axis=0)
		X_train = trainset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
		y_train = trainset['ProfitPercentage'].values
		regressor = LinearRegression()
		regressor.fit(X_train, y_train)
		y_pred = regressor.predict(X_test)
	#print(iterations)
		if(iterations == 1):		
			coeff_df = pd.DataFrame(regressor.coef_,  columns= ['Coefficients'])
			for index,row in coeff_df.iterrows():
				Module12Coeff.loc[index] = [coeff_df.at[index, 'Coefficients']] + [0]
				
			#print  ( coeff_df)
		df.loc[iterations] = [temp.at[0, "MovieName"]] + [temp.at[0, "ProfitPercentage"]] + [y_pred]
		predicted_values.loc[iterations] =  [temp.at[0, "MovieName"]] +  [abs(y_pred*dataset.at[iterations, 'Budget'])] + [1] + [0] + [0] + [0] + [0] + [0] + [0]
	#dataset = dataset.drop([0], axis=0)
	#print(dataset.loc[0])
		M1predf.loc[iterations] =  [temp.at[0, "MovieName"]] + [temp.at[0, "BoxOfficeSales"]] + [abs(y_pred*dataset.at[iterations, 'Budget'])] + [0]+['']
		
		if M1predf.at[iterations, 'Module 1 Prediction'] < 0:
			M1predf.at[iterations, 'Module 1 Prediction']= (abs(M1predf.at[iterations, 'Predicted'])/3)
		accuracy = 0
		accuracy = (M1predf.at[iterations, 'Module 1 Prediction']/M1predf.at[iterations, 'Actual'])
		if accuracy < 1 :
			accuracy = accuracy * 100.0
			M1predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		elif accuracy < 2:
			accuracy =(1.0 - (accuracy - 1.0)) * 100.0
			M1predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		else:
			accuracy = (accuracy - 1.0) * 100.0
			M1predf.at[iterations, "Percentile Deviation"] = accuracy
		
		iterations = iterations + 1
		temp = temp.drop([0], axis=0)
		
		#print('firstPred')
	iterations = 0
	print ("Done with module 1")
	while iterations < rowCount:
	
		temp.loc[0] = [dataset.at[ iterations, "MovieName"]] + [dataset.at[ iterations, "PositiveTweets"]] + [dataset.at[ iterations, "NeutralTweets"]] + [dataset.at[ iterations, "NegativeTweets"]] +  [dataset.at[ iterations, "PositiveFavorites"]] +  [dataset.at[ iterations, "NeutralFavorites"]] +   [dataset.at[ iterations, "NegativeFavorites"]] +  [dataset.at[ iterations, "PositiveRetweets"]] +   [dataset.at[ iterations, "NeutralRetweets"]] +  [dataset.at[ iterations, "NegativeRetweets"]] +  [dataset.at[ iterations, "PositiveReplies"]] +  [dataset.at[ iterations, "NeutralReplies"]]  +  [dataset.at[ iterations, "NegativeReplies"]] +  [dataset.at[ iterations, "Budget"]] +  [dataset.at[ iterations, "BoxOfficeSales"]] + [dataset.at[ iterations, "ProfitPercentage"]] 
		X_test = temp[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
		y_test = temp["BoxOfficeSales"].values
		trainset = dataset
		trainset = trainset.drop([iterations], axis=0)
		X_train = trainset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
		y_train = trainset['BoxOfficeSales'].values
		regressor = LinearRegression()
		regressor.fit(X_train, y_train)
		y_pred = regressor.predict(X_test)
	#print(iterations)
		if(iterations == 1):		
			coeff_df = pd.DataFrame(regressor.coef_,  columns= ['Coefficients'])
			for index,row in coeff_df.iterrows():
				Module12Coeff.at[index, 'Module 2'] = coeff_df.at[index, 'Coefficients']
		if (abs(df.at[iterations, 'Actual'] - df.at[iterations, 'Predicted'])) > (abs((y_pred/ temp.at[0, 'Budget']) - temp.at[0, 'ProfitPercentage'])):
		#print('changed' , iterations)
			df.at[iterations, 'Predicted'] = (y_pred/ temp.at[0, 'Budget'])
			predicted_values.at[iterations, 'M2 Ranking'] = 1
			predicted_values.at[iterations, 'M1 Ranking'] = 0
			
	#dataset = dataset.drop([0], axis=0)
	#print(dataset.loc[0])
		predicted_values.at[iterations, 'Module 2'] = y_pred
		M2predf.loc[iterations] =  [temp.at[0, "MovieName"]] + [temp.at[0, "BoxOfficeSales"]]+[abs(y_pred)] + [0] +['']
		if M2predf.at[iterations, 'Module 2 Prediction'] < 0:
			M2predf.at[iterations, 'Module 2 Prediction']= (abs(M2predf.at[iterations, 'Predicted'])/3)
		accuracy = 0
		accuracy = (M2predf.at[iterations, 'Module 2 Prediction']/M2predf.at[iterations, 'Actual'])
		if accuracy < 1 :
			accuracy = accuracy * 100.0
			M2predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		elif accuracy < 2:
			accuracy =(1.0 - (accuracy - 1.0)) * 100.0
			M2predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		else:
			accuracy = (accuracy - 1.0) * 100.0
			M2predf.at[iterations, "Percentile Deviation"] = accuracy
		iterations = iterations + 1
		temp = temp.drop([0], axis=0)
		#print('secondPred')
	print ("Done with module 2")
	iterations = 0
	while iterations < rowCount:
	
		temp2.loc[0] = [new.at[ iterations, "MovieName"]] + [new.at[ iterations, "Positive"]] + [new.at[ iterations, "Negative"]] + [new.at[ iterations, "Neutral"]] +  [new.at[ iterations, "Budget"]] +  [new.at[ iterations, "BoxOfficeSales"]] + [new.at[ iterations, "ProfitPercentage"]] 
		X_test = temp2[["Positive", "Negative", "Neutral", "Budget"]].values
		y_test = temp2["ProfitPercentage"].values
		trainset = new
		trainset = trainset.drop([iterations], axis=0)
		X_train = trainset[["Positive", "Negative", "Neutral", "Budget"]].values
		y_train = trainset['ProfitPercentage'].values
		regressor = LinearRegression()
		regressor.fit(X_train, y_train)
		y_pred = regressor.predict(X_test)
		if(iterations == 1):		
			coeff_df = pd.DataFrame(regressor.coef_,  columns= ['Coefficients'])
			for index,row in coeff_df.iterrows():
				Module34Coeff.loc[index] = [coeff_df.at[index, 'Coefficients']] + [0]
		#if(iterations == 1):		
		#	coeff_df = pd.DataFrame(regressor.coef_, X_train.columns, columns= ['Coefficients'])
		#	print (coeff_df)
			#print(regressor.coef)
		if (abs(df.at[iterations, 'Actual'] - df.at[iterations, 'Predicted'])) > (abs((y_pred) - temp2.at[0, 'ProfitPercentage'])):
		#print('changed' , iterations)
			df.at[iterations, 'Predicted'] = (y_pred)
			predicted_values.at[iterations, 'M3 Ranking'] = 1
			predicted_values.at[iterations, 'M1 Ranking'] = 0
			predicted_values.at[iterations, 'M2 Ranking'] = 0
	#dataset = dataset.drop([0], axis=0)
	#print(dataset.loc[0])
		predicted_values.at[iterations, 'Module 3'] = abs(y_pred * dataset.at[iterations, 'Budget']) 
	#dataset = dataset.drop([0], axis=0)
	#print(dataset.loc[0])
		M3predf.loc[iterations] =  [temp2.at[0, "MovieName"]] + [temp2.at[0, "BoxOfficeSales"]] + [abs(y_pred*dataset.at[iterations, 'Budget'])]  + [0] + ['']
		if M3predf.at[iterations, 'Module 3 Prediction'] < 0:
			M3predf.at[iterations, 'Module 3 Prediction']= (abs(M3predf.at[iterations, 'Predicted'])/3)
		accuracy = 0
		accuracy = (M3predf.at[iterations, 'Module 3 Prediction']/M3predf.at[iterations, 'Actual'])
		if accuracy < 1 :
			accuracy = accuracy * 100.0
			M3predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		elif accuracy < 2:
			accuracy =(1.0 - (accuracy - 1.0)) * 100.0
			M3predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		else:
			accuracy = (accuracy - 1.0) * 100.0
			M3predf.at[iterations, "Percentile Deviation"] = accuracy
		iterations = iterations + 1
		temp2 = temp2.drop([0], axis=0)
		#print('thirdPred')
	print ("Done with module 3")
	iterations = 0
	while iterations < rowCount:
	
		temp2.loc[0] = [new.at[ iterations, "MovieName"]] + [new.at[ iterations, "Positive"]] + [new.at[ iterations, "Negative"]] + [new.at[ iterations, "Neutral"]] +  [new.at[ iterations, "Budget"]] +  [new.at[ iterations, "BoxOfficeSales"]] + [new.at[ iterations, "ProfitPercentage"]] 
		X_test = temp2[["Positive", "Negative", "Neutral", "Budget"]].values
		y_test = temp2["BoxOfficeSales"].values
		trainset = new
		trainset = trainset.drop([iterations], axis=0)
		X_train = trainset[["Positive", "Negative", "Neutral", "Budget"]].values
		y_train = trainset['BoxOfficeSales'].values
		regressor = LinearRegression()
		regressor.fit(X_train, y_train)
		y_pred = regressor.predict(X_test)
		if(iterations == 1):		
			coeff_df = pd.DataFrame(regressor.coef_,  columns= ['Coefficients'])
			for index,row in coeff_df.iterrows():
				Module34Coeff.at[index, 'Module 4'] = coeff_df.at[index, 'Coefficients']
		if (abs(df.at[iterations, 'Actual'] - df.at[iterations, 'Predicted'])) > (abs((y_pred/temp2.at[0, 'Budget']) - temp2.at[0, 'ProfitPercentage'])):
		#print('changed' , iterations)
			df.at[iterations, 'Predicted'] = (y_pred/temp2.at[0, 'Budget'])
			predicted_values.at[iterations, 'M4 Ranking'] = 1
			predicted_values.at[iterations, 'M1 Ranking'] = 0
			predicted_values.at[iterations, 'M2 Ranking'] = 0
			predicted_values.at[iterations, 'M3 Ranking'] = 0
	#dataset = dataset.drop([0], axis=0)
	#print(dataset.loc[0])
		predicted_values.at[iterations, 'Module 4'] = y_pred
	#dataset = dataset.drop([0], axis=0)
	#print(dataset.loc[0])
		M4predf.loc[iterations] =  [temp2.at[0, "MovieName"]] + [temp2.at[0, "BoxOfficeSales"]]+[abs(y_pred)] + [0] + ['']
		if M4predf.at[iterations, 'Module 4 Prediction'] < 0:
			M4predf.at[iterations, 'Module 4 Prediction']= (abs(M4predf.at[iterations, 'Predicted'])/3)
		accuracy = 0
		accuracy = (M4predf.at[iterations, 'Module 4 Prediction']/M4predf.at[iterations, 'Actual'])
		if accuracy < 1 :
			accuracy = accuracy * 100.0
			M4predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		elif accuracy < 2:
			accuracy =(1.0 - (accuracy - 1.0)) * 100.0
			M4predf.at[iterations, "Percentile Deviation"] = abs(100.0 - accuracy)
			
		else:
			accuracy = (accuracy - 1.0) * 100.0
			M4predf.at[iterations, "Percentile Deviation"] = accuracy
		iterations = iterations + 1
		temp2 = temp2.drop([0], axis=0)
		#print('fourthPred')
	print ("Done with module 4")
	iterations = 0
	accuracy = 0.0
	sum1 = 0.0
	df['Accuracy'] = 0.0
	while iterations < rowCount:
		if df.at[iterations, 'Predicted'] < 0:
			df.at[iterations, 'Predicted']= (abs(df.at[iterations, 'Predicted'])/3)
		accuracy = (df.at[iterations, 'Predicted']/df.at[iterations, 'Actual'])
		if accuracy < 1 :
			accuracy = accuracy * 100.0
			df.at[iterations, 'Accuracy'] = abs(100.0 - accuracy)
			sum1 = sum1 + (abs(100.0 - accuracy))
		elif accuracy < 2:
			accuracy =(1.0 - (accuracy - 1.0)) * 100.0
			df.at[iterations, 'Accuracy'] = abs(100.0 - accuracy)
			sum1 = sum1 + (abs(100.0 - accuracy))
		else:
			accuracy = (accuracy - 1.0) * 100.0
			df.at[iterations, 'Accuracy'] = accuracy
			sum1 = sum1 + accuracy
		iterations = iterations + 1
		#print('accuracy')
	iterations = 0
	
	while iterations < rowCount:
		df.at[iterations, 'Actual'] = dataset.at[iterations, 'BoxOfficeSales']
		df.at[iterations, 'Predicted']= (df.at[iterations, 'Predicted']*dataset.at[iterations, 'Budget'])
		database_predictedvalues.loc[iterations] = [predicted_values.at[iterations, 'MovieName']] + [predicted_values.at[iterations, 'Module 1']] + [predicted_values.at[iterations, 'Module 2']]  + [predicted_values.at[iterations, 'Module 3']]  + [predicted_values.at[iterations, 'Module 4']] + [''] + [''] + [0] + [0] + [0]


		database_bestcase.loc[iterations] = [df.at[iterations, "MovieName"]] + ['$' + ('%.2f' % (df.at[iterations, 'Actual']))] + ['$' + ('%.2f' % df.at[iterations, 'Predicted'])] + ['%.2f' % df.at[iterations, 'Accuracy']] + ['']
		iterations = iterations + 1
	iterations = 0 
	mean_act = []
	mean_pred = []
	while iterations < rowCount:
		
		mean_act.append(df.at[iterations, 'Actual'])
		mean_pred.append(df.at[iterations, 'Predicted'])
		iterations = iterations + 1
	#dt = df.sort_values(['Accuracy'])
	
	database_overall.loc[0] = [rowCount] + [0] + ['%' + ('%.2f' %(sum1/rowCount))] + [ '$' + ('%.2f' % (mean_absolute_error(mean_act,mean_pred)))] + [0] + [0]

	#print(dt)
	print("")
	#print (sum1/rowCount, "= Mean Difference")
	print("")

	iterations = 0
	totalRig = 0

	while iterations < rowCount:
	
		holdval = 'Module 2'
		holdnow = "M2 Ranking"

		Coldval = dataset.at[ iterations, "Budget"]

	
	

		if (Coldval >= 40000000.0):
			store = 1
			
			if ((Coldval <= 50000000.0 ) and (dataset.at[ iterations, "PositiveTweets"] + dataset.at[ iterations, "NeutralTweets"] + dataset.at[ iterations, "NegativeTweets"] +  dataset.at[ iterations, "PositiveFavorites"] +  dataset.at[ iterations, "NeutralFavorites"] +   dataset.at[ iterations, "NegativeFavorites"] +  dataset.at[ iterations, "PositiveRetweets"] +   dataset.at[ iterations, "NeutralRetweets"] +  dataset.at[ iterations, "NegativeRetweets"] +  dataset.at[ iterations, "PositiveReplies"] +  dataset.at[ iterations, "NeutralReplies"]  +  dataset.at[ iterations, "NegativeReplies"]) < 12000):
			
				holdval = 'Module 3'
				holdnow = 'M3 Ranking'
	
			if ((Coldval <= 50000000.0 ) and (dataset.at[ iterations, "NegativeFavorites"]) < 4000):
			
				holdval = 'Module 3'
				holdnow = 'M3 Ranking'
		
			
			
			
			

		else:
			holdval = 'Module 1'
			holdnow = 'M1 Ranking'

			if (dataset.at[ iterations, "PositiveTweets"] + dataset.at[ iterations, "NeutralTweets"] + dataset.at[ iterations, "NegativeTweets"] +  dataset.at[ iterations, "PositiveFavorites"] +  dataset.at[ iterations, "NeutralFavorites"] +   dataset.at[ iterations, "NegativeFavorites"] +  dataset.at[ iterations, "PositiveRetweets"] +   dataset.at[ iterations, "NeutralRetweets"] +  dataset.at[ iterations, "NegativeRetweets"] +  dataset.at[ iterations, "PositiveReplies"] +  dataset.at[ iterations, "NeutralReplies"]  +  dataset.at[ iterations, "NegativeReplies"]) > 100000 and Coldval < 30000000:
				holdval = 'Module 2'
				holdnow = 'M2 Ranking'

			elif (dataset.at[ iterations, "PositiveTweets"] + dataset.at[ iterations, "NeutralTweets"] + dataset.at[ iterations, "NegativeTweets"] +  dataset.at[ iterations, "PositiveFavorites"] +  dataset.at[ iterations, "NeutralFavorites"] +   dataset.at[ iterations, "NegativeFavorites"] +  dataset.at[ iterations, "PositiveRetweets"] +   dataset.at[ iterations, "NeutralRetweets"] +  dataset.at[ iterations, "NegativeRetweets"] +  dataset.at[ iterations, "PositiveReplies"] +  dataset.at[ iterations, "NeutralReplies"]  +  dataset.at[ iterations, "NegativeReplies"]) > 100000 and Coldval > 35000000:
				holdval = 'Module 2'
				holdnow = 'M2 Ranking'
	

		if (dataset.at[ iterations, "PositiveTweets"] + dataset.at[ iterations, "NeutralTweets"] + dataset.at[ iterations, "NegativeTweets"] +  dataset.at[ iterations, "PositiveFavorites"] +  dataset.at[ iterations, "NeutralFavorites"] +   dataset.at[ iterations, "NegativeFavorites"] +  dataset.at[ iterations, "PositiveRetweets"] +   dataset.at[ iterations, "NeutralRetweets"] +  dataset.at[ iterations, "NegativeRetweets"] +  dataset.at[ iterations, "PositiveReplies"] +  dataset.at[ iterations, "NeutralReplies"]  +  dataset.at[ iterations, "NegativeReplies"]) < 10000 and (Coldval <= 20000000):
			holdnow = 'M4 Ranking'
			holdval = 'Module 4'
		if predicted_values.at[iterations, holdnow] == 1:
		#print (holdnow)
			totalRig = totalRig + 1

		#best_module = ''
		for index,row in predicted_values.iterrows():
			if predicted_values.at[index, 'M1 Ranking'] == 1:
		
				Best_modules.loc[index] = [predicted_values.at[index, 'MovieName']]  + [predicted_values.at[index, 'Module 1']]  + [predicted_values.at[index, 'Module 2']] +  [predicted_values.at[index, 'Module 3']] +  [predicted_values.at[index, 'Module 4']] + ['Module 1']
				#best_module = 'Module 1'
			elif predicted_values.at[index, 'M2 Ranking'] == 1:
				
				Best_modules.loc[index] = [predicted_values.at[index, 'MovieName']]  + [predicted_values.at[index, 'Module 1']]  + [predicted_values.at[index, 'Module 2']] +  [predicted_values.at[index, 'Module 3']] +  [predicted_values.at[index, 'Module 4']] + ['Module 2']

			elif predicted_values.at[index, 'M3 Ranking'] == 1:

				Best_modules.loc[index] = [predicted_values.at[index, 'MovieName']]  + [predicted_values.at[index, 'Module 1']]  + [predicted_values.at[index, 'Module 2']] +  [predicted_values.at[index, 'Module 3']] +  [predicted_values.at[index, 'Module 4']] + ['Module 3']
	
			else :
				Best_modules.loc[index] = [predicted_values.at[index, 'MovieName']]  + [predicted_values.at[index, 'Module 1']]  + [predicted_values.at[index, 'Module 2']] +  [predicted_values.at[index, 'Module 3']] +  [predicted_values.at[index, 'Module 4']] + ['Module 4']

				
		if holdnow == 'M1 Ranking':
			M1predf.at[iterations, 'Best'] = 'yes'
			M2predf.at[iterations, 'Best'] = 'no'
			M3predf.at[iterations, 'Best'] = 'no'
			M4predf.at[iterations, 'Best'] = 'no'
			
		elif holdnow == 'M2 Ranking':
			M1predf.at[iterations, 'Best'] = 'no'
			M2predf.at[iterations, 'Best'] = 'yes'
			M3predf.at[iterations, 'Best'] = 'no'
			M4predf.at[iterations, 'Best'] = 'no'
			
		elif holdnow == 'M3 Ranking':
			
			M1predf.at[iterations, 'Best'] = 'no'
			M2predf.at[iterations, 'Best'] = 'no'
			M3predf.at[iterations, 'Best'] = 'yes'
			M4predf.at[iterations, 'Best'] = 'no'
		else:
			
			M1predf.at[iterations, 'Best'] = 'no'
			M2predf.at[iterations, 'Best'] = 'no'
			M3predf.at[iterations, 'Best'] = 'no'
			M4predf.at[iterations, 'Best'] = 'yes'
			

	#else:
	#	print (predicted_values.at[iterations, 'MovieName'], holdnow, Coldval)
	
		predf.loc[iterations]= [predicted_values.at[iterations, 'MovieName']] + [dataset.at[iterations, 'BoxOfficeSales']] + [predicted_values.at[iterations, holdval]]	
		
		database_predictedvalues.at[iterations, 'Predicted Module'] = holdval
		
		iterations = iterations + 1
	

	
	iterations = 0
	accuracy = 0.0
	sum1 = 0.0
	predf['Accuracy'] = 0.0
	while iterations < rowCount:
		if predf.at[iterations, 'Predicted'] < 0:
			predf.at[iterations, 'Predicted']= (abs(predf.at[iterations, 'Predicted'])/3)
		accuracy = (predf.at[iterations, 'Predicted']/predf.at[iterations, 'Actual'])
		if accuracy < 1 :
			accuracy = accuracy * 100.0
			predf.at[iterations, 'Accuracy'] = abs(100.0 - accuracy)
			sum1 = sum1 + (abs(100.0 - accuracy))
		elif accuracy < 2:
			accuracy =(1.0 - (accuracy - 1.0)) * 100.0
			predf.at[iterations, 'Accuracy'] = abs(100.0 - accuracy)
			sum1 = sum1 + (abs(100.0 - accuracy))
		else:
			accuracy = (accuracy - 1.0) * 100.0
			predf.at[iterations, 'Accuracy'] = accuracy
			sum1 = sum1 + accuracy
		iterations = iterations + 1
	#print('accuracy')
	iterations = 0
	mean_actual = []
	mean_predicted = []
	while iterations < rowCount:
		predf.at[iterations, 'Actual'] = dataset.at[iterations, 'BoxOfficeSales']
		mean_actual.append(predf.at[iterations, 'Actual'])
		mean_predicted.append(predf.at[iterations, 'Predicted'])
		database_bestcase.at[iterations, 'Best module'] = Best_modules.at[iterations, 'Best']
		database_predictedvalues.at[iterations, 'Best'] = Best_modules.at[iterations, 'Best']
		database_predictedvalues.at[iterations, 'Predicted Value'] = predf.at[iterations, 'Predicted']
		database_predictedvalues.at[iterations, 'Percentile Deviation'] = predf.at[iterations, 'Accuracy']
		database_predictedvalues.at[iterations, 'Actual'] = predf.at[iterations, 'Actual']
		if database_predictedvalues.at[iterations, 'Best'] == database_predictedvalues.at[iterations, 'Predicted Module']:
			database_correct.loc[iterations]=[database_predictedvalues.at[iterations, 'MovieName']] + ['Yes']
		else:
			database_correct.loc[iterations]=[database_predictedvalues.at[iterations, 'MovieName']] + ['No']
		iterations = iterations + 1
	
	dt = predf.sort_values(['Accuracy'])
	#print(database_bestcase)
	
	nml = database_predictedvalues.copy()
	sml = nml.sort_values(['Percentile Deviation'])
	database_predictedvalues = sml
	for index,row in database_predictedvalues.iterrows():
		database_predictedvalues.at[index, 'Predicted Value'] = '$' + '%.2f' % database_predictedvalues.at[index, 'Predicted Value']
		database_predictedvalues.at[index, 'Actual'] = '$' + '%.2f' % database_predictedvalues.at[index, 'Actual']
		database_predictedvalues.at[index, 'Module 1'] = '$' + '%.2f' % database_predictedvalues.at[index, 'Module 1']
		database_predictedvalues.at[index, 'Module 2'] = '$' + '%.2f' % database_predictedvalues.at[index, 'Module 2']
		database_predictedvalues.at[index, 'Module 3'] = '$' + '%.2f' % database_predictedvalues.at[index, 'Module 3']
		database_predictedvalues.at[index, 'Module 4'] = '$' + '%.2f' % database_predictedvalues.at[index, 'Module 4']
		database_predictedvalues.at[index, 'Percentile Deviation'] = '%' + '%.2f' % database_predictedvalues.at[index, 'Percentile Deviation']
		dt.at[index, 'Predicted'] = '$' + '%.2f' % dt.at[index, 'Predicted']
		#dt.at[index, 'Actual'] = dt.at[index, 'Actual']
		dt.at[index, 'Accuracy'] =   dt.at[index, 'Accuracy']
	display (database_predictedvalues)
	#display(dt)
	
	
	pd.set_option('display.max_rows',60)
	
	print ("Total Best Modules Chosen:")
	print (totalRig, "/", rowCount)
	print ( '%.2f' % (sum1/rowCount), "= Mean Percentile Deviation")
	print('MAE', '$' + '%.2f' % (mean_absolute_error(mean_actual,mean_predicted)))
	database_overall.at[0,'Predicted MAE'] = '$' + '%.2f' % (mean_absolute_error(mean_actual,mean_predicted))
	database_overall.at[0,'Best Cases chosen'] = totalRig
	database_overall.at[0,'Predicted Percentile Deviation'] = '%' + '%.2f' % (sum1/rowCount)
	
	

		
	
	database_module1 = M1predf.sort_values(['Best'],ascending=False)
	database_module2 = M2predf.sort_values(['Best'],ascending=False)
	database_module3 = M3predf.sort_values(['Best'],ascending=False)
	database_module4 = M4predf.sort_values(['Best'],ascending=False)
	
	database_Used = 1
	columnames = dataset.columns.values.tolist()
	for index,row in Module12Coeff.iterrows():
				ModuleCoeff13.loc[index] = [columnames[index+1]] + [Module12Coeff.at[index, 'Module 1']] + [Module12Coeff.at[index, 'Module 2']] 
	columname = temp2.columns.values.tolist()
	for index,row in Module34Coeff.iterrows():
				ModuleCoeff4.loc[index] = [columname[index+1]] + [Module34Coeff.at[index, 'Module 3']] + [Module34Coeff.at[index, 'Module 4']] 
	
	database_coefficients1and2 = ModuleCoeff13
	database_coefficients3and4 = ModuleCoeff4
	
	bt = Best_modules.sort_values(['Best'])
	
	return



#The function used by CombinePage() to store the files chosen by user that will be combined.
def getCSV(name):
	ListofCSVS[name] =  askopenfilename()

#The page where a user can predict the box office of a single movie against the main database set in defaultdataset. The movie can either have box office values, or not have box office values. A user can then see the results and save them. OpenResult(), ClosedResult(), SaveOpenResult(), SaveClosedResult(), OpenBoxPrediction(), and ClosedBoxPrediction() are all called from here.

class PredictPage(Frame):

	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self, text="Choose file to use for prediction", font=LARGE_FONT)
		label.pack(pady=20,padx=20)

     
		button= Button(self, text='Select File with Box Office information', font=Fine_font, command=callbackPredict).pack()
		
		
		button2= Button(self, text='Select File that has no Box Office information', font=Fine_font, command=callbackPredict2).pack()

		button5= Button(self, text='Show results for the last Box Office information prediction', font=Fine_font, command=OpenResult).pack()
		
		
		button4= Button(self, text='Show results for the last prediction that didn\'t have box office information', font=Fine_font, command= ClosedResult).pack()
	
		button6= Button(self, text='Save for last prediction that had Box Office Information', font=Fine_font, command=SaveOpenResult).pack()
		
		
		button7= Button(self, text='Save for last prediction that has no Box Office information', font=Fine_font, command=SaveClosedResult).pack()

		label3 = Label(self, text="Results are saved in the format \"~BoxPredictResults.csv\" or  \"~NoBoxResults.csv\" respectively, where ~ is the name of the movie", font=small_font).pack(pady=10,padx=10)

		button3= Button(self, text='Back to main menu', font=Fine_font, command=lambda: controller.show_frame(StartPage)).pack()


#The functionality of this program is similar as datasetPredict(), so refer to "Dataset_Predict_comments.py" file if you wish to understand the structure. The only difference is that only the chosen file is predicted, and the main defaultdataset is used for training. p_r_o_Used and predicted_results_open obtain their values here.

def OpenBoxPrediction(csvP):

	
	dataset = defaultdataset.copy()
	testset = pd.read_csv(csvP)
	pol = 0.0
	rowCount = dataset.shape[0]

	dataset.loc[rowCount] = ["Control"] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol]

	inet = rowCount + 1
	while inet < rowCount*10:
		dataset.loc[inet]= ["Control"] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + 	[pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol]

		inet = inet + 1
	new = pd.DataFrame(columns = ["MovieName", "Positive", "Negative" , "Neutral", "Budget", "BoxOfficeSales", "ProfitPercentage"])

	temp2 = pd.DataFrame(columns = ["MovieName", "Positive", "Negative" , "Neutral", "Budget", "BoxOfficeSales", "ProfitPercentage"])

	inet = 0
	while inet < rowCount*10:
		new.loc[inet] = [dataset.at[inet, "MovieName"]] + [(dataset.at[inet, "PositiveTweets"] + dataset.at[inet, "PositiveFavorites"] + dataset.at[inet, "PositiveRetweets"] + dataset.at[inet, "PositiveReplies"])] + [(dataset.at[inet, "NegativeTweets"] + dataset.at[inet, "NegativeFavorites"] + dataset.at[inet, "NegativeRetweets"] + dataset.at[inet, "NegativeReplies"])] + [(dataset.at[inet, "NeutralTweets"] + dataset.at[inet, "NeutralFavorites"] + dataset.at[inet, "NeutralRetweets"] + dataset.at[inet, "NeutralReplies"])] +   [dataset.at[ inet, "Budget"]] +  [dataset.at[ inet, "BoxOfficeSales"]] + [dataset.at[ inet, "ProfitPercentage"]]
		
		inet = inet + 1
	

	df = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted"])
	predf = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted"])
	predicted_values =  pd.DataFrame(columns = ["MovieName", "Module 1", "M1 Ranking",  "Module 2", "M2 Ranking",  "Module 3", "M3 Ranking",  "Module 4", "M4 Ranking", "Best", "Ranking"])

	
	X_test = testset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	y_test = testset["ProfitPercentage"].values
	trainset = dataset
	X_train = trainset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	y_train = trainset['ProfitPercentage'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	df.loc[0] = [testset.at[0, "MovieName"]] + [testset.at[0, "ProfitPercentage"]] + [y_pred]
	predicted_values.loc[0] =  [testset.at[0, "MovieName"]] +  [abs(y_pred*testset.at[0, 'Budget'])] + [1] + [0] + [0] + [0] + [0] + [0] + [0] + ['Module 1'] + ['M1 Ranking']
	print("Done with module 1")
	X_test = testset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	y_test = testset["BoxOfficeSales"].values
	trainset = dataset
	X_train = trainset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	y_train = trainset['BoxOfficeSales'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	if (abs(df.at[0, 'Actual'] - df.at[0, 'Predicted'])) > (abs((y_pred/ testset.at[0, 'Budget']) - testset.at[0, 'ProfitPercentage'])):
		
		df.at[0, 'Predicted'] = (y_pred/ testset.at[0, 'Budget'])
		predicted_values.at[0, 'M2 Ranking'] = 1
		predicted_values.at[0, 'M1 Ranking'] = 0
		predicted_values.at[0, 'Best'] = 'Module 2'
		predicted_values.at[0, 'Ranking'] = 'M2 Ranking'
			
	
	predicted_values.at[0, 'Module 2'] = y_pred
	print("Done with module 2")
	temp2.loc[0] = [testset.at[0, "MovieName"]] + [(testset.at[0, "PositiveTweets"] + testset.at[0, "PositiveFavorites"] + testset.at[0, "PositiveRetweets"] + testset.at[0, "PositiveReplies"])] + [(testset.at[0, "NegativeTweets"] + testset.at[0, "NegativeFavorites"] + testset.at[0, "NegativeRetweets"] + testset.at[0, "NegativeReplies"])] + [(testset.at[0, "NeutralTweets"] + testset.at[0, "NeutralFavorites"] + testset.at[0, "NeutralRetweets"] + testset.at[0, "NeutralReplies"])] +   [testset.at[ 0, "Budget"]] +  [testset.at[0, "BoxOfficeSales"]] + [testset.at[ 0, "ProfitPercentage"]] 
	X_test = temp2[["Positive", "Negative", "Neutral", "Budget"]].values
	y_test = temp2["ProfitPercentage"].values
	trainset = new
	
	X_train = trainset[["Positive", "Negative", "Neutral", "Budget"]].values
	y_train = trainset['ProfitPercentage'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	if (abs(df.at[0, 'Actual'] - df.at[0, 'Predicted'])) > (abs((y_pred) - testset.at[0, 'ProfitPercentage'])):
		
		df.at[0, 'Predicted'] = (y_pred)
		
		predicted_values.at[0, 'M3 Ranking'] = 1

		predicted_values.at[0, 'M2 Ranking'] = 0
		predicted_values.at[0, 'M1 Ranking'] = 0
		predicted_values.at[0, 'Best'] = 'Module 3'
		predicted_values.at[0, 'Ranking'] = 'M3 Ranking'
	
	print("Done with module 3")
	predicted_values.at[0, 'Module 3'] = abs(y_pred* testset.at[0,'Budget'])
	temp2 = temp2.drop([0], axis=0)
	temp2.loc[0] = [testset.at[0, "MovieName"]] + [(testset.at[0, "PositiveTweets"] + testset.at[0, "PositiveFavorites"] + testset.at[0, "PositiveRetweets"] + testset.at[0, "PositiveReplies"])] + [(testset.at[0, "NegativeTweets"] + testset.at[0, "NegativeFavorites"] + testset.at[0, "NegativeRetweets"] + testset.at[0, "NegativeReplies"])] + [(testset.at[0, "NeutralTweets"] + testset.at[0, "NeutralFavorites"] + testset.at[0, "NeutralRetweets"] + testset.at[0, "NeutralReplies"])] +   [testset.at[ 0, "Budget"]] +  [testset.at[0, "BoxOfficeSales"]] + [testset.at[ 0, "ProfitPercentage"]] 
	X_test = temp2[["Positive", "Negative", "Neutral", "Budget"]].values
	y_test = temp2["BoxOfficeSales"].values
	trainset = new
	
	X_train = trainset[["Positive", "Negative", "Neutral", "Budget"]].values
	y_train = trainset['BoxOfficeSales'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	if (abs(df.at[0, 'Actual'] - df.at[0, 'Predicted'])) > (abs((y_pred/ testset.at[0, 'Budget']) - testset.at[0, 'ProfitPercentage'])):
		
			
		df.at[0, 'Predicted'] = (y_pred/ testset.at[0, 'Budget'])
		
		predicted_values.at[0, 'M4 Ranking'] = 1

		predicted_values.at[0, 'M3 Ranking'] = 1

		predicted_values.at[0, 'M2 Ranking'] = 0
		predicted_values.at[0, 'M1 Ranking'] = 0
		predicted_values.at[0, 'Best'] = 'Module 4'
		predicted_values.at[0, 'Ranking'] = 'M4 Ranking'

	print("Done with module 4")
	predicted_values.at[0, 'Module 4'] = y_pred
	
	holdval = 'Module 2'
	holdnow = "M2 Ranking"

	Coldval = testset.at[ 0, "Budget"]

	
	

	if (Coldval >= 40000000.0):
		store = 1
		
		if ((Coldval <= 50000000.0 ) and (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) < 12000):
			
			holdval = 'Module 3'
			holdnow = 'M3 Ranking'

		if ((Coldval <= 50000000.0 ) and (testset.at[ 0, "NegativeFavorites"]) < 4000):
			
			holdval = 'Module 3'
			holdnow = 'M3 Ranking'
		
			
			
			
			

	else:
		holdval = 'Module 1'
		holdnow = 'M1 Ranking'

		if (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) > 100000 and Coldval < 30000000:
			holdval = 'Module 2'
			holdnow = 'M2 Ranking'

		elif (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) > 100000 and Coldval > 35000000:
			holdval = 'Module 2'
			holdnow = 'M2 Ranking'
	

	if (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) < 10000 and (Coldval <= 20000000):
		holdnow = 'M4 Ranking'
		holdval = 'Module 4'
	if predicted_values.at[0, holdnow] == 1:
		print ('Best Prediction Chosen')
	
	best_module = ''
	if predicted_values.at[0, 'M1 Ranking'] == 1:
		
		best_module = 'Module 1'
	elif predicted_values.at[0, 'M2 Ranking'] == 1:
		
		best_module = 'Module 2'

	elif predicted_values.at[0, 'M3 Ranking'] == 1:

		best_module = 'Module 3'
	
	else :

		best_module = 'Module 4'
	
	predf.loc[0]= [predicted_values.at[0, 'MovieName']] + [testset.at[0, 'BoxOfficeSales']] + [predicted_values.at[0, holdval]]
	accuracy = 0.0	
	if predf.at[0, 'Predicted'] < 0:
		predf.at[0, 'Predicted']= (abs(predf.at[0, 'Predicted'])/3)
	accuracy = (predf.at[0, 'Predicted']/predf.at[0, 'Actual'])
	if accuracy < 1 :
		accuracy = accuracy * 100.0
		predf.at[0, 'Accuracy'] = abs(100.0 - accuracy)
		
	elif accuracy < 2:
		accuracy =(1.0 - (accuracy - 1.0)) * 100.0
		predf.at[0, 'Accuracy'] = abs(100.0 - accuracy)
		
	else:
		accuracy = (accuracy - 1.0) * 100.0
		predf.at[0, 'Accuracy'] =   accuracy
		
	#predf.at[0, 'Accuracy'] = ('%' + ('%.2f' %predf.at[0, 'Accuracy']))
	predf.at[0, 'Actual']= testset.at[0, 'BoxOfficeSales']
	
	predf.at[0, 'Predicted']= ('$' + ('%.2f' %predf.at[0, 'Predicted']))
	display(predf)
	global p_r_o_Used
	global predicted_results_open
	if p_r_o_Used == 1:
		predicted_results_open = predicted_results_open.drop([0], axis=0)
	
	
	predicted_results_open.loc[0] = [predicted_values.at[0, 'MovieName']] +  [('$' + ('%.2f' %predicted_values.at[0, 'Module 1']))] + [('$' + ('%.2f' %predicted_values.at[0, 'Module 2']))] + [('$' + ('%.2f' %predicted_values.at[0, 'Module 3']))] + [('$' + ('%.2f' %predicted_values.at[0, 'Module 4']))] + [best_module] + [holdval] + [('$' + ('%.2f' %predicted_values.at[0, holdval]))] + [ ('$' + ('%.2f' %predf.at[0, 'Actual']))] + [ ('%' + ('%.2f' %predf.at[0, 'Accuracy']))]
	p_r_o_Used = 1
	return
	
#Similar to OpenBoxPrediction(), the only difference being that the final predicted value is not compared to its actual box office, as that data was not given. p_r_c_Used and predicted_results_closed obtain their values here.
	
def ClosedBoxPrediction(csvP):
	
	dataset = defaultdataset.copy()
	testset = pd.read_csv(csvP)
	pol = 0.0
	rowCount = dataset.shape[0]

	dataset.loc[rowCount] = ["Control"] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol]

	inet = rowCount + 1
	while inet < rowCount*10:
		dataset.loc[inet]= ["Control"] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + 	[pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol] + [pol]

		inet = inet + 1
	new = pd.DataFrame(columns = ["MovieName", "Positive", "Negative" , "Neutral", "Budget", "BoxOfficeSales", "ProfitPercentage"])

	temp2 = pd.DataFrame(columns = ["MovieName", "Positive", "Negative" , "Neutral", "Budget"])

	inet = 0
	while inet < rowCount*10:
		new.loc[inet] = [dataset.at[inet, "MovieName"]] + [(dataset.at[inet, "PositiveTweets"] + dataset.at[inet, "PositiveFavorites"] + dataset.at[inet, "PositiveRetweets"] + dataset.at[inet, "PositiveReplies"])] + [(dataset.at[inet, "NegativeTweets"] + dataset.at[inet, "NegativeFavorites"] + dataset.at[inet, "NegativeRetweets"] + dataset.at[inet, "NegativeReplies"])] + [(dataset.at[inet, "NeutralTweets"] + dataset.at[inet, "NeutralFavorites"] + dataset.at[inet, "NeutralRetweets"] + dataset.at[inet, "NeutralReplies"])] +   [dataset.at[ inet, "Budget"]] +  [dataset.at[ inet, "BoxOfficeSales"]] + [dataset.at[ inet, "ProfitPercentage"]]
		
		inet = inet + 1
	

	#df = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted"])
	#predf = pd.DataFrame(columns = ["MovieName", "Actual", "Predicted"])
	predicted_values =  pd.DataFrame(columns = ["MovieName", "Module 1",  "Module 2", "Module 3",  "Module 4"])

	
	X_test = testset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	
	trainset = dataset
	X_train = trainset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	y_train = trainset['ProfitPercentage'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	
	predicted_values.loc[0] =  [testset.at[0, "MovieName"]] +  [abs(y_pred*testset.at[0, 'Budget'])] + [''] + [''] + [''] 
	print("Done with module 1")
	X_test = testset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	
	trainset = dataset
	X_train = trainset[["PositiveTweets", "NeutralTweets","NegativeTweets",  "PositiveFavorites", "NeutralFavorites","NegativeFavorites", "PositiveRetweets", "NeutralRetweets","NegativeRetweets", "PositiveReplies", "NeutralReplies","NegativeReplies", "Budget"]].values
	y_train = trainset['BoxOfficeSales'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	
			
	
	predicted_values.at[0, 'Module 2'] = y_pred
	print("Done with module 2")
	
	temp2.loc[0] = [testset.at[0, "MovieName"]] + [(testset.at[0, "PositiveTweets"] + testset.at[0, "PositiveFavorites"] + testset.at[0, "PositiveRetweets"] + testset.at[0, "PositiveReplies"])] + [(testset.at[0, "NegativeTweets"] + testset.at[0, "NegativeFavorites"] + testset.at[0, "NegativeRetweets"] + testset.at[0, "NegativeReplies"])] + [(testset.at[0, "NeutralTweets"] + testset.at[0, "NeutralFavorites"] + testset.at[0, "NeutralRetweets"] + testset.at[0, "NeutralReplies"])] +   [testset.at[ 0, "Budget"]] 
	X_test = temp2[["Positive", "Negative", "Neutral", "Budget"]].values
	
	trainset = new
	
	X_train = trainset[["Positive", "Negative", "Neutral", "Budget"]].values
	y_train = trainset['ProfitPercentage'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	
	
	predicted_values.at[0, 'Module 3'] = abs(y_pred* testset.at[0,'Budget'])
	print("Done with module 3")
	temp2 = temp2.drop([0], axis=0)
	temp2.loc[0] = [testset.at[0, "MovieName"]] + [(testset.at[0, "PositiveTweets"] + testset.at[0, "PositiveFavorites"] + testset.at[0, "PositiveRetweets"] + testset.at[0, "PositiveReplies"])] + [(testset.at[0, "NegativeTweets"] + testset.at[0, "NegativeFavorites"] + testset.at[0, "NegativeRetweets"] + testset.at[0, "NegativeReplies"])] + [(testset.at[0, "NeutralTweets"] + testset.at[0, "NeutralFavorites"] + testset.at[0, "NeutralRetweets"] + testset.at[0, "NeutralReplies"])] +   [testset.at[ 0, "Budget"]]
	X_test = temp2[["Positive", "Negative", "Neutral", "Budget"]].values
	
	trainset = new
	
	X_train = trainset[["Positive", "Negative", "Neutral", "Budget"]].values
	y_train = trainset['BoxOfficeSales'].values
	regressor = LinearRegression()
	regressor.fit(X_train, y_train)
	y_pred = regressor.predict(X_test)
	

	
	predicted_values.at[0, 'Module 4'] = y_pred
	print("Done with module 4")
	
	holdval = 'Module 2'
	

	Coldval = testset.at[ 0, "Budget"]

	
	

	if (Coldval >= 40000000.0):
		store = 1
		
		if ((Coldval <= 50000000.0 ) and (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) < 12000):
			
			holdval = 'Module 3'
			

		if ((Coldval <= 50000000.0 ) and (testset.at[ 0, "NegativeFavorites"]) < 4000):
			
			holdval = 'Module 3'
	
		
			
			
			
			

	else:
		holdval = 'Module 1'
		

		if (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) > 100000 and Coldval < 30000000:
			holdval = 'Module 2'
			

		elif (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) > 100000 and Coldval > 35000000:
			holdval = 'Module 2'
			
	

	if (testset.at[ 0, "PositiveTweets"] + testset.at[ 0, "NeutralTweets"] + testset.at[ 0, "NegativeTweets"] +  testset.at[ 0, "PositiveFavorites"] +  testset.at[ 0, "NeutralFavorites"] +   testset.at[ 0, "NegativeFavorites"] +  testset.at[ 0, "PositiveRetweets"] +   testset.at[ 0, "NeutralRetweets"] +  testset.at[ 0, "NegativeRetweets"] +  testset.at[ 0, "PositiveReplies"] +  testset.at[ 0, "NeutralReplies"]  +  testset.at[ 0, "NegativeReplies"]) < 10000 and (Coldval <= 20000000):
		
		holdval = 'Module 4'
	
	pdf = predicted_values.copy()
	pdf.at[0, 'Module 1'] = ('$' + ('%.2f' %pdf.at[0, 'Module 1']))
	pdf.at[0, 'Module 2'] = ('$' + ('%.2f' %pdf.at[0, 'Module 2']))
	pdf.at[0, 'Module 3'] = ('$' + ('%.2f' %pdf.at[0, 'Module 3']))
	pdf.at[0, 'Module 4'] = ('$' + ('%.2f' %pdf.at[0, 'Module 4']))
	display(pdf)
	print('Chosen Prediction', '$' + ('%.2f' %predicted_values.at[0, holdval]), holdval)
	
	global p_r_c_Used 
	global predicted_results_close
	if p_r_c_Used == 1:
		predicted_results_close = predicted_results_close.drop([0], axis=0)
	
	
	
	predicted_results_close.loc[0] = [predicted_values.at[0, 'MovieName']] +  ['$' + ('%.2f' %predicted_values.at[0, 'Module 1'])] + ['$' + ('%.2f' %predicted_values.at[0, 'Module 2'])] + ['$' + ('%.2f' %predicted_values.at[0, 'Module 3'])] + ['$' + ('%.2f' %predicted_values.at[0, 'Module 4'])] + [holdval] + ['$' + ('%.2f' %predicted_values.at[0, holdval])]
	
	p_r_c_Used = 1
	
	return

if __name__ == "__main__":
	app = SeaofBTCapp()
	app.mainloop()

