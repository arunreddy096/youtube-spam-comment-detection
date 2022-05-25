from flask import Flask,render_template,url_for,request
import csv
import io
from selenium import webdriver
from selenium.common import exceptions
import sys
import time
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
cv = CountVectorizer()

app=Flask(__name__)

@app.route('/')
def home():
	return render_template('home1.html')

@app.route('/scrape1',methods=['POST'])
def scrape1():
	if request.method=='POST':
		result=request.form.get("l")
		scrape(result)
		x=predict()
		return render_template('result1.html',data=x)
def scrape(url):
	driver = webdriver.Chrome(R'chromedriver.exe')

	driver.get(url)
	driver.maximize_window()
	time.sleep(5)

	try:

		title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
		comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
	except exceptions.NoSuchElementException:

		error = "Error: Double check selector OR "
		error += "element may not yet be on the screen at the time of the find operation"
		print(error)



	driver.execute_script("arguments[0].scrollIntoView();", comment_section)
	time.sleep(7)


	last_height = driver.execute_script("return document.documentElement.scrollHeight")

	while True:

		driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")


		time.sleep(2)


		new_height = driver.execute_script("return document.documentElement.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


	driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

	try:

		username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
		comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
	except exceptions.NoSuchElementException:
		error = "Error: Double check selector OR "
		error += "element may not yet be on the screen at the time of the find operation"
		print(error)

	print("> VIDEO TITLE: " + title + "\n")

	with io.open('results.csv', 'w', newline='', encoding="utf-16") as file:
		writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
		writer.writerow(["Comment"])
		for username, comment in zip(username_elems, comment_elems):
			writer.writerow([username.text, comment.text])

	driver.close()
def predict():
	df= pd.read_csv("modified.csv")
	df_data = df[["CONTENT","CLASS"]]
	# Features and Labels
	df_x = df_data['CONTENT']
	df_y = df_data.CLASS
	# Extract Feature With CountVectorizer
	corpus = df_x
	#cv = CountVectorizer()
	X = cv.fit_transform(corpus) # Fit the Data
	from sklearn.model_selection import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.20, random_state=57)
	clf = RandomForestClassifier()
	clf.fit(X_train,y_train)
	sc=clf.score(X_test,y_test)
	print("With an accuracy of",sc)
	df = pd.read_csv(r"results.csv",encoding = 'utf-16')
	ef=pd.DataFrame(columns=['Spam','Not spam'])
	li={}
	li.setdefault(0,[])
	li.setdefault(1,[])
	li1=[]
	for data in df['Comment']:
		input = cv.transform([data]).toarray()
		my_prediction = clf.predict(input)
		if(my_prediction[0]):
			li[0].append(data)
		else:
			li[1].append(data)
	return li

if __name__ == '__main__':
	app.run(debug=True)
