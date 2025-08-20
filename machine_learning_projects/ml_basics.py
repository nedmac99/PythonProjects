from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

'''
x = np.array([[1], [2], [3], [4], [5]]) #Features (e.g., size)
y = np.array([1.5, 3.5, 4.5, 5.0, 6.5]) #Targets (e.g., price)
model = LinearRegression()
model.fit(x,y)
# Predict price for a house size 6
print(model.predict([[6]])) #Answer = 7.65
'''

#Commonly used ML functions
'''
Function                         Purpose
-----------                      ----------------
train_test_split()               Splits data into training/test sets
.fit(x,y)                        Trains the model
.predict(x)                      Makes prediction
.score(x,y)                      Evaluates accuracy to R^2 score
classification_report()          Gives precision, recall f1-score
confusion_matrix()               Breakdown of prediction vs truth
StandardScaler()                 Normalizes data (important for ML)
'''

#Exercise 1
'''
x = np.array([[1], [3], [5], [7], [9]])
y = np.array([2, 6, 10, 14, 18])
model = LinearRegression()
model.fit(x,y)
print(model.predict([[11]])) #Produces 22
'''

#Data splitting
'''
Training set ---> model learns from this
Test set ---> model is evaluated on this
The training set is where the model learns the relationship
The test set is where we check if the model can apply that knowledge to new situations

This is done using train_test_split from sklearn.model_selection
'''

#Structure of splitting data
'''
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)

test_size=0.2 ---> means 2-% of the data goes into testing, 80% goes to training
random_state=42 ---> ensures reproducibility (same random split every time)
'''

#Example 2

x = np.array([[1], [3], [5], [7], [9]])
y = np.array([2, 6, 10, 14, 18])

#Step 1: Split the data
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Step 2: Create and train model
model = LinearRegression()
model.fit(X_train, Y_train)

#Step 3: Test the model on unseen data
print(model.predict(X_test))
print(Y_test)

'''
Ml usually uses a score or error metric to measure performance
For regression problems (like prediction numbers), one common score is R^2 score
EX: model.score(X_test, Y_test)
This gives a number between:
1.0 ---> Perfect Prediction
0.0 ---> Model is no better than guessing the average
Negative ---> Model is worse than a simple guess
'''

#Types of classification
'''
-Linear Regression → predicts continuous numbers (like house prices).
-Logistic Regression → despite the name, it’s used for classification problems (predicting categories).
-Decision Tree → another great option for classification (splits data into rules, like a flowchart).
'''