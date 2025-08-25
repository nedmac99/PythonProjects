import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#Goal
#Predict whether a passenger survived or not
#Use seaborns built-in dataset and pandas for cleaning and preparing data

#Roadmap
'''
1. Load Titanic dataset
2. Explore it (Look at columns, missing values, etc.)
3. Prepare the data(cleaning, handling missing values, encoding categorical variables)
4. Split into train/test sets
5. Train models (Logistic Regression, Decision Tree, maybe Random Forest)
6. Evaulate accuracy + confusion matrix
7. Compare models
Bonus
-Train Random Forest Classifier
-Add Feature Engineering (add embarked, create family_size = sibsp + parch, etc.)
'''

#Load Titanic dataset
df = sns.load_dataset("titanic")
#print(df.head())
#df.info()

#Cleaning the data
df = df.drop(columns=['deck']) #Drop the deck column due to how many missing values it has 
df['age'] = df['age'].fillna(df['age'].median()) #Fill missing age values with median
df['sex'] = df['sex'].map({'male': 0, 'female': 1}) #Convert sex to numeric values

#Check that there are no more missing values in the dataframe
#print(df.isnull().sum())

#Assigning Feature(X) and Target(y)
y = df['survived']
X = df[['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare']] #Numeric columns only

#Split data into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#print(X_train.shape, X_test.shape) #See the size of X_train and X_test

#Create and train model
model = LogisticRegression(max_iter= 200)
model.fit(X_train, y_train)

#Make predictions on test set
predictions = model.predict(X_test)

#Check accuracy on predictions
accuracy = accuracy_score(y_test, predictions)
#print(accuracy)

#Creating and checking using a confusion matrix to see why accuracy was scored the way it was 
#cm = confusion_matrix(y_test, predictions)
#disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
#disp.plot()
#plt.show()

#Matrix explanation
'''
Top-left = correctly predicted deaths
Bottom-right = correctly predicted survivors
Off-diagonals = mistakes
'''

#Classification Report
class_report = classification_report(y_test, predictions, target_names=['Died', 'Survived'])
#print(class_report)

#Classification_Report explained
'''
Precision → of those predicted “Survived”, how many actually survived
Recall → of the people who survived, how many did we correctly predict
F1-score → balance of precision and recall
'''

#Comparing models
#Train Decision Tree
dt_model = DecisionTreeClassifier(random_state=42)
dt_model.fit(X_train, y_train)

#Predictions
dt_predictions = dt_model.predict(X_test)

#Accuracy check
#print("Logistic Regression Accuracy:", accuracy)
#print("Decision Tree Accuracy:", accuracy_score(y_test, dt_predictions))

#Results
'''
-Logistic Regression finds a smooth, linear decision boundary. On the Titanic dataset, a few features (like sex, pclass, age) have pretty clean patterns that logistic regression captures well.
-Decision Trees tend to overfit small datasets if you don’t limit their depth. They try to memorize exact rules (e.g., if passenger is 32 years old, in 2nd class, with fare $10.5, then …). That can hurt generalization, especially with noisy/missing data.
-Logistic Regression often outperforms a raw Decision Tree on Titanic.
-But if we use Random Forests (an ensemble of many trees), performance usually jumps up.
'''

#Train Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

#Predictions
rf_predictions = rf_model.predict(X_test)

#Accuracy check (Logistic Regression has highest)
#print("Logistic Regression Accuracy:", accuracy_score(y_test, predictions)) #0.8100558659217877
#print("Decision Tree Accuracy:", accuracy_score(y_test, dt_predictions)) #0.7597765363128491
#print("Random Forest Accuracy:", accuracy_score(y_test, rf_predictions)) #0.8044692737430168

#Feature Engineering
'''
-Create family_size variable by combining SibSp(siblings/spouses aboard) and Parch(parents/children aboard)
-Create title by extracting titles(Mr, Mrs, Miss, Master) from passengers names. It can often help predict survival. (e.g. Children with Master had higher survival)
-Then map rare titles into a few categories(Mr, Mrs, Miss, Master, Other)
'''
#Extract title from name
df['title'] = df['who'].str.extract(r' ([A-Za-z]+)\.', expand=False)

#Simplify rare titles
df['title'] = df['title'].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
df['title'] = df['title'].replace(['Mlle', 'Ms'], 'Miss')
df['title'] = df['title'].replace('Mme', 'Mrs')

#Encode titles numerically
df['title'] = df['title'].map({'Mr': 0, 'Miss': 1, 'Mrs': 2, 'Master': 3, 'Rare': 4})

#Create family size
df['family_size'] = df['sibsp'] + df['parch'] + 1

#Converts sex and title into numeric dummy variables
df = pd.get_dummies(df, columns=['sex', 'title'], drop_first=True)

#New features
features = ['pclass', 'age', 'fare', 'sibsp', 'parch', 'family_size'] + \
           [col for col in df.columns if col.startswith('sex_') or col.startswith('title_')]

#Retrain Random Forest classifier with new variables/data
X = df[features]
y = df['survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

#Accuracy has increased to: 0.8156424581005587 and now has the highest accuracy
print("Accuracy:", accuracy)