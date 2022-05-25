# youtube-spam-comment-detection
# youtubecommentspamdetectionusinglink

install chromedriver according to chrome version

Steps to run:

1. Goto the folder and locate test3.py file

2. Then run the file in cmd python test3.py

3. Open http://127.0.0.1/5000 in browser

4. Enter a youtube link in the text box and press predict button


Youtube spam comments detection is a Flask web app which detects all spam comments of a given Youtube link. In this project, different machine learning models were used and the one with highest accuracy has been implemented. RANDOM FOREST is selected as it got highest average accuracy among all models.

ACCURACY OF EACH MODEL AT DIFFERENT TEST SIZES PROPORTION

Test date size Proportion 0.2 Logistic Regression 0.93 Random Forest 0.93 MultinomialNB 0.89 SVM 0.93

Test date size Proportion 0.33 Logistic Regression 0.93 Random Forest 0.95 MultinomialNB 0.89 SVM 0.93

Test date size Proportion 0.43 Logistic Regression 0.94 Random Forest 0.95 MultinomialNB 0.87 SVM 0.94
