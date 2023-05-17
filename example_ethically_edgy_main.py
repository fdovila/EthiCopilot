
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# create a dataframe with personal data
data = {
    "Name": ["John", "Jane", "Jack", "Jill"],
    "Age": [20, 21, 22, 23],
    "Gender": ["Male", "Female", "Male", "Female"],
    "Income": [10000, 12000, 15000, 18000],
    "Credit Score": [700, 750, 800, 850],
}
df = pd.DataFrame(data)

# create a target variable
df["Approved"] = np.where(df["Credit Score"] > 750, 1, 0)

# split the data into training and test sets
X = df[["Age", "Gender", "Income", "Credit Score"]]
y = df["Approved"]
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# fit the logistic regression model
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

# make predictions on the test set
y_pred = logreg.predict(X_test)

# evaluate the model
from sklearn.metrics import confusion_matrix

confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

# calculate the accuracy of the model
from sklearn.metrics import accuracy_score

print(
    "Accuracy of logistic regression classifier on test set: {:.2f}".format(
        accuracy_score(y_test, y_pred)
    )
)
