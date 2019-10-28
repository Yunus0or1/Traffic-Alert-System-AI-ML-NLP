from django.shortcuts import render,redirect,HttpResponse
from django.db import connection
from .models import data


import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
import datetime
from datetime import timedelta
import mysql.connector
from django.db import connection
import MySQLdb

# Create your views here.

def home(request):
	
	cursor = connection.cursor()
	cursor.execute("select * from alert_data where seen=0")
	data = cursor.fetchall()
	
	cursor.execute("SELECT * FROM alert_data where seen=1 ORDER BY id DESC limit 10 ")
	data_previous = cursor.fetchall()
	
	
	
	
	cursor.execute("SELECT * FROM alert_data where seen=0 ORDER BY id DESC limit 10 ")
	data_now = cursor.fetchall()
	

	if data_now: #Means data presents
	
			now_time = datetime.datetime.now()	
			prev_time = data_now[0][5]	
			prev_time = data_now[0][5]  + timedelta(minutes=1)
	
			if now_time > prev_time:
				cursor.execute("update alert_data set seen=1 where seen=0")


	
	
	return render(request, 'a.html', {
		'data'			: data,	
		'what'			:'Traffic alert on time ',
		'data_previous' : data_previous,
		})
		
		
def search_area_func(request):

	if request.method == "GET":
		
		search_area = request.GET['search_area']
		
		
		if search_area is not None and search_area != u"":
		
			search_area = request.GET['search_area']
			
			search_area = search_area.lower()
			
			
			search_area = data.objects.filter(extracted_info__contains = search_area).order_by('-id')[:5]
			
			return render(request, 'ajax.html', {
			'search_area':search_area})
			
			
			
		if search_area == u"":	#If blank in search area
		
			cursor = connection.cursor()
			cursor.execute("SELECT * FROM alert_data where seen=1 ORDER BY id DESC limit 10 ")
			data_previous = cursor.fetchall()
			
			return render(request, 'ajax.html', {
				'data_previous' : data_previous,
				})
			

def information(request):

	if request.method == "POST":
	
		status = request.POST['data']	
	
	url = "../traffic_data.txt"
	names = ['message', 'outcome']
	dataset = pandas.read_csv(url, names=names)

	dataset_x = dataset["message"]
	dataset_y = dataset["outcome"]
	
	print(dataset_x)
	print(dataset_y)





	cv = TfidfVectorizer(min_df=1,stop_words='english')

	x_train, x_test, y_train, y_test = model_selection.train_test_split(dataset_x, dataset_y, test_size=0.8, random_state=2)

	x_train_cv = cv.fit_transform(x_train)

	x_test_cv = cv.transform(x_test)


	classifier = MultinomialNB()
	classifier.fit(x_train_cv, y_train)

	predictions = classifier.predict(x_test_cv)




	sentence = status
	sentence = sentence.lower()
	words = word_tokenize(sentence)



	#Make of NER code.

	filename = "../place.txt"
	data_place = pandas.read_csv(filename,names=['place'])
	data_placename = data_place['place']



	jam_place_integer = 0 #This will be needed for first and second phase
	jam_place2_integer = 0 #This will be needed for third phase
	jam_place3_integer = 0 #This will be needed for third phase because 'to' will have two places
	enter_to_second_phase = 0
	enter_to_third_phase = 0
	enter_to_fourth_phase = 0

	if 'near' in words or 'at' in words or 'of' in words :
		for x in range(0,len(words)):
			if words[x] == 'near' or words[x] ==  'at' or words[x] ==  'of' :
				jam_place_integer = x + 1
	else :
		enter_to_second_phase = 1




	if enter_to_second_phase == 1:
		if 'in' in words :
			for x in range(0, len(words)):
				if words[x] == 'in' :
					if (str(words[x+1]) == 'traffic' or str(words[x+1]) == 'jam'  or str(words[x+1]) == 'grid' or str(words[x+1]) == 'lock') :
						enter_to_third_phase = 1
					else:
						pos_tag_of_next_word = nltk.pos_tag(word_tokenize(words[x + 1]))
						word, tag = zip(*pos_tag_of_next_word)
						pos_tag_of_next_word_str = str(''.join(tag))
						if pos_tag_of_next_word_str =='NN' or pos_tag_of_next_word_str == 'NNP':
							jam_place_integer = x + 1
		else:
			enter_to_third_phase = 1



	if enter_to_third_phase==1 :
		if 'to' in words :
			for x in range(0, len(words)):
				if words[x] == 'to':
					jam_place2_integer = x + 1
					#Now finding if previous word is a place also
					pos_tag_of_previous_word = nltk.pos_tag(word_tokenize(words[x - 1]))
					word, tag = zip(*pos_tag_of_previous_word)
					pos_tag_of_previous_word_str = str(''.join(tag))
					if pos_tag_of_previous_word_str == 'NN' or pos_tag_of_previous_word_str == 'NNP':
						jam_place3_integer = x - 1

		else :
			enter_to_fourth_phase = 1

	#This method creates problem which name has two separate parts. like Manik mia
	if enter_to_fourth_phase == 1 :
		for w in words:
			for x in range(data_placename.count()):
				if str(w) == str(data_placename[x]):
					jam_place = w

	#This method creates problem which name has two separate parts.


	jam_place_final_result = ''


	if jam_place_integer != 0:
		jam_place = words[jam_place_integer]
		jam_place_final_result = jam_place


	if enter_to_third_phase == 1 and enter_to_fourth_phase == 0:
		if jam_place3_integer ==0:
			jam_place = words[jam_place2_integer]
			jam_place_final_result =  jam_place
		if jam_place3_integer !=0:
			jam_place2 = words[jam_place2_integer]
			jam_place3 = words[jam_place3_integer]
			jam_place_final_result =  jam_place3 + ' to ' + jam_place2


	if  enter_to_fourth_phase == 1:
		jam_place_final_result = jam_place


	#End of NER


	test_line_tfidf = cv.transform([sentence])
	prediction = classifier.predict(test_line_tfidf)



	final_result = ''

	if str(prediction) == '[0]' :
		final_result = 'There may be no traffic jam at ' + jam_place_final_result
	if str(prediction) == '[1]' :
		final_result = 'There may be traffic jam at ' + jam_place_final_result
	if str(prediction) == '[2]' :
		final_result = 'Someone is trying to know the road condition of ' + jam_place_final_result


	#Saving the result in Database for further mining
	time = str(datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))
	time = datetime.datetime.now()

	try:
		connection = MySQLdb.connect(host="localhost",user="root",password="",db="traffic_alert")
	except Exception as e:
		print('Not connected')


	cursor = connection.cursor()
	cursor.execute("insert into alert_data (main_status,extracted_info,place,time) values (%s,%s,%s,%s)",[sentence,final_result,jam_place_final_result,time])
	connection.commit()

		
	return redirect('home')
			
		
		
		
		
		
		