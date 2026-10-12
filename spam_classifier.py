import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Small dataset
messages = [
    "Win a free lottery now",
    "Hey, how are you?",
    "Claim your free prize",
    "Let's have lunch tomorrow"
]

labels = ["spam", "ham", "spam", "ham"]

# Convert text to numbers
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(messages)

# Train model
model = MultinomialNB()
model.fit(X, labels)

# Test
test_message = ["Free prize waiting for you"]
test_vector = vectorizer.transform(test_message)

prediction = model.predict(test_vector)

print("Prediction:", prediction[0])
