import pandas as pd 
import pymysql
import mysql.connector as mariadb
import sys

#Function that takes a single Box.csv or BoxSentiment.csv file and adds it to the main database, while also updating defaultdataset. In UpdatePage()

def callbackUpdateDB():

#Ask user for the single box office sentiment file name.
	name2= askopenfilename()
	print(name2)
	decf = pd.read_csv(name2)

#Access database here.
	mydbcon = mariadb.connect(
	host="localhost",
	user="Predaccount",
	passwd="pass",
	database = "linearReg"
	)
	mycursor = mydbcon.cursor()

#Add file data to database here

	sql = 'Insert into maindata (MovieName, PT, NT, NEGT, PF, NF, NEGF, PRT, NRT, NEGRT, PRL, NRL, NEGRL, Budget, Box, PROFIT) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	val = (decf.at[ 0, "MovieName"],  decf.at[ 0, "PositiveTweets"].item(), decf.at[ 0, "NeutralTweets"].item(), decf.at[ 0, "NegativeTweets"].item(),  decf.at[ 0, "PositiveFavorites"].item(),  decf.at[ 0, "NeutralFavorites"].item(),   decf.at[ 0, "NegativeFavorites"].item(),  decf.at[ 0, "PositiveRetweets"].item(),   decf.at[ 0, "NeutralRetweets"].item(),  decf.at[ 0, "NegativeRetweets"].item(),  decf.at[ 0, "PositiveReplies"].item(),  decf.at[ 0, "NeutralReplies"].item(),  decf.at[ 0, "NegativeReplies"].item(),decf.at[ 0, "Budget"].item(),decf.at[ 0, "BoxOfficeSales"].item() ,decf.at[ 0, "ProfitPercentage"].item())
	mycursor.execute(sql, val)
	mydbcon.commit()
	mydbcon.close()
	print("Database has been updated")

#Add file data to the default dataset of the program.
	rowCount = defaultdataset.shape[0]
	defaultdataset.loc[rowCount]=  [decf.at[ 0, "MovieName"]] + [decf.at[ 0, "PositiveTweets"]] + [decf.at[ 0, "NeutralTweets"]] + [decf.at[ 0, "NegativeTweets"]] +  [decf.at[ 0, "PositiveFavorites"]] +  [decf.at[ 0, "NeutralFavorites"]] +   [decf.at[ 0, "NegativeFavorites"]] +  [decf.at[ 0, "PositiveRetweets"]] +   [decf.at[ 0, "NeutralRetweets"]] +  [decf.at[ 0, "NegativeRetweets"]] +  [decf.at[ 0, "PositiveReplies"]] +  [decf.at[ 0, "NeutralReplies"]]  +  [decf.at[ 0, "NegativeReplies"]] +  [decf.at[ 0, "Budget"]] +  [decf.at[ 0, "BoxOfficeSales"]] + [decf.at[ 0, "ProfitPercentage"]] 
	return
	

#Function that deletes the current database and replaces it with a csv file. The program must restart after this is ran if the new database wishes to be used. In UpdatePage()

def callbackRewriteDB():

#Ask user for file name to repalce database with.
	name2= askopenfilename()
	print(name2)
	decf = pd.read_csv(name2)

#Access database here

	mydbcon = mariadb.connect(
	host="localhost",
	user="Predaccount",
	passwd="pass",
	database = "linearReg"
	)
	mycursor = mydbcon.cursor()
	mycursor.execute("delete from maindata")

#Replace database here

	sql = 'Insert into maindata (MovieName, PT, NT, NEGT, PF, NF, NEGF, PRT, NRT, NEGRT, PRL, NRL, NEGRL, Budget, Box, PROFIT) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
	for index,row in decf.iterrows():
		val = (decf.at[ index, "MovieName"],  decf.at[ index, "PositiveTweets"].item(), decf.at[ index, "NeutralTweets"].item(), decf.at[ index, "NegativeTweets"].item(),  decf.at[ index, "PositiveFavorites"].item(),  decf.at[ index, "NeutralFavorites"].item(),   decf.at[ index, "NegativeFavorites"].item(),  decf.at[ index, "PositiveRetweets"].item(),   decf.at[ index, "NeutralRetweets"].item(),  decf.at[ index, "NegativeRetweets"].item(),  decf.at[ index, "PositiveReplies"].item(),  decf.at[ index, "NeutralReplies"].item(),  decf.at[ index, "NegativeReplies"].item(),decf.at[ index, "Budget"].item(),decf.at[ index, "BoxOfficeSales"].item() ,decf.at[ index, "ProfitPercentage"].item())
		mycursor.execute(sql, val)
	mydbcon.commit()
	mydbcon.close()
	print("Database has been rewritten, please restart to have changes enforced")
	return