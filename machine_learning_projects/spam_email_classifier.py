from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import matplotlib.pyplot as plt

#Goal and core challenge
'''
-Predict if an email is spam or not using classification
-Representing text as features the model can understand
-Understand the difference between threshold tuning and precision vs recall tradeoffs
'''

#Ways to represent content numerically
'''
-Categorize real/trusted vs suspicious/fake(But emails are mostly text)
-Bag-of-Words(BoW): Count how many times each word appears in the email.
-TF-IDF(Term Frequency-Inverse Document Frequency): Weighs words by importance across all emails.
-Keyword flags: Check for suspicious words like "free", "prize", "click here", etc. --> 1/0 features.
-Length of punctuation features: Number of words, number of exclamation marls, number of links, etc.
'''

#Roadmap
'''
-Preparing Features (Categorize the sender and a few suspicious keyword flags)
-Explore Bag-of-Words or TF-IDF (Captures the full content but more complex)
'''

#Using keywords to flag spam
'''
#Encode sender as 0 (Trusted) or 1 (Suspicious)
df['send_flag'] = df['sender'].map({'trusted': 0, 'suspicious': 1})

#Flag suspicious keywords
keywords = ['free', 'win', 'prize', 'click', 'urgent']
for word in keywords:
    df[f'has_{word}'] = df['email_text'].str.contains(word, case=False, regex=True).astype(int)

#Target
y = df['spam'] #0 = not spam, 1 = spam

#Features
X = df[['sender_flag'] + [f'has_{word}' for word in keywords]]

#Split Training and Testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Train Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#Prediction
predictions = model.predict(X_test)

#Evaluate accuracy
#accuracy = accuracy_score(y_test, predictions)
#print("Accuracy:", accuracy)

#Confusion Matrix
#cm = confusion_matrix(y_test, predictions)
#disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
#disp.plot()
#plt.show()

#To lower false positives (blocking good emails from coming through) we tune the model threshold.
#To change the model threshold we have to adjust the spam probability during the prediction step. (Default is 0.5)
y_probs = model.predict_proba(X_test)[:,1] #probability of spam
y_pred_custom = (y_probs > 0.8).astype(int) #classify as spam only if probability is > 0.8

'''


#Improving Spam filter by using features like vectorization with TF-IDF
'''
-Represent the email text as numbers using TF-IDF
-Train a classifier (Logistic Regression or Random Forest)
-Compare performance to our keyword-based approach
'''

#Understanding TF-IDF
'''
-TF(Term-Frequency): How often a word appears in the document
-IDF(Inverse Document Frequency): How rare the word is across all documents (downweights common words like "the" or "and")
-TF-IDF score: TF x IDF ---> highlights important, rare words that can distinguish spam vs not spam
'''

#Split into training/testing sets
#X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

#Limit too many rare words that may become too noisy and lower the accuracy
vectorizer = TfidfVectorizer(max_features=1000, min_df=5) #Focuses on informative words that actually help distinguish spam, while reducing noise and false positives

#Train Logisitic Regression Model
model = LogisticRegression(max_iter=500) #Increases max_iter for convergence
#model.fit(X_train, y_train)

#Predictions
#predictions = model.predict(X_test)

#Evaluate accuracy
#accuracy = accuracy_score(y_test, predictions)
#print("Accuracy:", accuracy)

#Confusion Matrix
#cm = confusion_matrix(y_test, predictions)
#disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
#disp.plot()
#plt.show()

#Combine the TF-IDF features (sparse matrix) with the numeric sender_flag column into a single feature matrix
#sender_flag = df['sender_flag'].values.reshape(-1,1)
#X_combined = hstack([X_tfidf, sender_flag])

#Split Train/Test set with combined Features
#X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

#Fit model
#model.fit(X_train, y_train)
#Predictions
#predictions = model.predict(X_test)

#Check Precision
#precision = precision_score(y_test, predictions)
#print("Precision:", precision)

#Completed
'''
-TF-IDF features
-Combining numeric data
-Training a classifier
-Evaluating with confusion matrices and precision
'''