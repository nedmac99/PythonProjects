from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#SEE BOTTOM TO VIEW CLEAN VERSION OF PROGRAM

#Goal
'''
Predict house prices based on features like:
-Number of bedrooms/bathrooms
-Square footage
-Neighborhood
-Year built
-Lot size
'''

#Concepts
'''
-Regression problem, not classification
-Instead of predicting categories, we predict a continuous number(Price)
-We'll practice:
    -Handling missing data
    -Encoding categorical features
    -Scaling numeric features (like LotArea because values might be much larger and could throw off weight of evaluation)
    -Training regression models (Linear Regression, Random Forest Regressor)
    -Evaluating performance with metrics like RMSE(Root Mean Squared Error) or R²
    -Mean Squared Error (MSE (average of squared errors)) vs Root Mean Squared Error (RMSE (result is in the same units as the target variable))
'''

#Dataset
housing = fetch_california_housing()

#Convert dataset into dataframe for analyzing
df_features = pd.DataFrame(housing.data, columns=housing.feature_names)
#Drop Latitude and longitude as they have lowest correlation to predictions
df_features.drop(['Latitude','Longitude', 'Population', 'AveBedrms'], axis=1, inplace=True)

#Create Target for testing/analyzing
df_features['MedHouseVal'] = housing.target

#Create correlations variable
correlations = df_features.corr()

#Check which columns correlate to ['MedHouseVal']
#print(correlations['MedHouseVal'].sort_values(ascending=False))

#Check first 5 entries
#print(df_features.head())

#Check columns and if isnull
#df_features.info()

#Establish Features (X) and Target (y)(Prices in $1000s)
X = df_features.drop('MedHouseVal', axis=1) 
y = df_features['MedHouseVal']
feature_names = X.columns

#Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Initialize RF Model
rf = RandomForestRegressor(n_estimators=100, random_state=42)

#Intialize GBR Model
gbr = GradientBoostingRegressor(
    n_estimators=200, 
    learning_rate=0.1, 
    max_depth=3, 
    random_state=42
)
'''
n_estimators → number of sequential trees
learning_rate → controls how much each tree contributes
max_depth → depth of each tree
random_state → for reproducibility
'''

#Train
gbr.fit(X_train, y_train)
rf.fit(X_train, y_train)

#Predict
gbr_predictions = gbr.predict(X_test)
rf_predictions = rf.predict(X_test)

#Evaluate
gbr_rmse = np.sqrt(mean_squared_error(y_test, gbr_predictions))
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_predictions))
#print("Gradient Boosting Regressor Root mean Squared Error(Simplified):", gbr_rmse)
#print("Random Forest Regressor Root mean Squared Error(Simplified):", rf_rmse) 


#Test Random Forest vs Linear Regression
#Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_prediction = lr.predict(X_test)
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_prediction))
#print("Random Forest RMSE:", rmse) #RF = 0.5053399773665033($50,500)
#print("Linear Regression RMSE:", lr_rmse) #LR = 0.7455813830127751($74,600)
#Note: Lower RMSE = better performance

#Show importance of Features
rf_importances = rf.feature_importances_
df_imp = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_importances
}).sort_values(by='Importance', ascending=False)
#print(df_imp)


#Visulaizations
'''
plt.figure(figsize=(8,5))
plt.barh(df_imp['Feature'], df_imp['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Random Forest Feature Importances')
plt.gca().invert_yaxis()  # highest importance on top
plt.show()
'''

#Test Model with user data
'''
#Get Test data
medinc = float(input("Enter median income (in 10k$ units, ex: 3.5): "))
house_age = float(input("Enter house age (median age of houses in the area): "))
avg_rooms = float(input("Enter the average number of rooms per household: "))
avg_occupany = float(input("Enter the average occpants per household: "))

#Create a single-row 2D array for the model to parse
user_data = np.array([[medinc, house_age, avg_rooms, avg_occupany]])

#Predict with trained model
test_prediction = gbr.predict(user_data)

#Produce result
print(f"Predicted house price (in 100,000s $): {test_prediction[0]: .2f}")
'''

#Cleaner version
'''
# Step 1: Imports
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 2: Load dataset
california = fetch_california_housing()
df = pd.DataFrame(california.data, columns=california.feature_names)
df['MedHouseVal'] = california.target  # add target column

# Step 3: (Optional) drop low-importance features if you want
# For example, let's assume we decided to drop 'Longitude' and 'Latitude'
df = df.drop(['Longitude', 'Latitude'], axis=1)

# Step 4: Prepare features and target
X = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']

# Step 5: Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 6: Train Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Step 7: Predict and evaluate
preds = rf.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print("Random Forest RMSE:", rmse)

# Step 8: Feature importance
importances = rf.feature_importances_
df_imp = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# Step 9: Plot feature importance
plt.figure(figsize=(8,5))
plt.barh(df_imp['Feature'], df_imp['Importance'], color='skyblue')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Random Forest Feature Importances')
plt.gca().invert_yaxis()  # highest importance on top
plt.show()
'''
