from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

'''
Data set has:

Features(X):
------------
-Sepal length
-Sepal width
-Petal length
-Petal width

Target(y):
------------
-Flower species(Setosa, Versicolor, Virginica)
'''

#Example loading in dataset and checking attributes
'''
iris = load_iris()
print(iris.feature_names)  #Names of features
print(iris.target_names)   #Names of species
print(iris.data[:5])       #First 5 rows of feature data
print(iris.target[:5])     #First 5 labels
'''

#Workflow
'''
1. Load the dataset
2. Split into train/test sets
3. Train a classifier (instead of Regression, we'll use Logistic Regression or Decision Tree)
4. Make predictions
5. Evaluate performance
'''

#Load dataset
iris = load_iris()
X = iris.data
y = iris.target

#Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#print(X_train.shape, X_test.shape) #See the sizes

#Train Logistic Regression model
model = LogisticRegression(max_iter=200) #max_iter increased so it fully converges

#Model learns from training data
model.fit(X_train, y_train)

predictions = model.predict(X_test)
#print(predictions[:10]) #first 10 predicted labels
#print(y_test[:10]) #first 10 actual labels
#Both produce same result showing the predicted labels matched the actual labels 100%

#Measuring accuracy
#accuracy = accuracy_score(y_test, predictions)
#print("Accuracy: ", accuracy)

#Training a decision tree classifier
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

#Predictions
dt_predictions = dt_model.predict(X_test)
#print(dt_predictions[:10]) #Produced same results as before

#Setting up confusion matrix(rows = actual, cols = predicted)
cm = confusion_matrix(y_test, dt_predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=iris.target_names)
#disp.plot()
#plt.show()
#Diagonal = correct predictions
#Off-diagonal = mistakes

#Comparing Logistic Regression vs Decision Tree accuracy
log_acc = accuracy_score(y_test, predictions)
dt_acc = accuracy_score(y_test, dt_predictions)
print("Logistic Regression accuracy:", log_acc)
print("Decision tree accuracy:", dt_acc)

#Key differences between Logistic Regression and Decision tree
'''
Logistic Regression → learns a linear boundary between classes.
Decision Tree → splits data into rule-based conditions (like “if petal length < 2.5 then Setosa”).
Both can do really well on Iris, but in bigger/messier datasets, you’d likely see differences in performance.
'''
