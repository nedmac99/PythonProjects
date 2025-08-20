from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

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

#model learns from training data
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(predictions[:10]) #first 10 predicted labels
print(y_test[:10]) #first 10 actual labels