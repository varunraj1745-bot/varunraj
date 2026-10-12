# Spam Classifier

print("Spam Classifier is starting up...")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

print("All libraries loaded successfully!")

# Load dataset
data = pd.read_csv("spam.csv")

X = data["message"]
y = data["label"]

vectorizer = CountVectorizer()
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model trained successfully!")
print("Accuracy:", accuracy)

msg = ["Congratulations! You won free money"]
msg_vector = vectorizer.transform(msg)
result = model.predict(msg_vector)

print("Message:", msg[0])
print("Prediction:", result[0])