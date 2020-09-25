# Traffic-Alert-System-AI-ML-NLP
A traffic alert system using Machine learning, Artificial Intelligence and Natural Language Processing. Website developed in Django.

  >Think of a situation where people get stucked in traffic jam at the same road daily. But it can be easily avoided if the exact time of traffic jam news can be broadcasted. This project  inteds to circulate the traffic jam news accross various user. Whenever someone gets stucked in traffic jam and sends out the news via this website , the back-end code will immediately detects what the user is saying whether there is traffic jam or not or either the user is just trying to know the road situation. There is also a custom made NER which detects the place name where the traffic jam is occuring. This is rather a good project for beginners for learning ML,AI and NLP.

The full code can be found in **main_code.py** file.
This is an web based project in Django Framework.
First install Django and Xampp.
Open cmd and set the path to Traffic_alert folder
Load traffic_alert.sql in Database.
Run the project from cmd as any other Django project.

Python 3.6.2 required as this uses mysqlclient

You may need to install many libraries :

```
pip install mysqlclient
pip install matplotlib
pip install sklearn
pip install mysql-connector
pip install nltk
```


And many more may be needed. Run the project you will find errors and the 
terminal will specify which library is needed.
Nltk will need all the punkt library. You will see error. Just follow the instructions from the errors.
