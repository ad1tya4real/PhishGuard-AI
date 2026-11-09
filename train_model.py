
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Sample email dataset
emails = [
    "Congratulations you won a free prize click here",
    "Your bank account is blocked verify your password",
    "Urgent update your account details immediately",
    "Click this link to claim your lottery reward",
    "Your account has suspicious activity verify now",
    "You have won a free gift claim your reward",
    "Enter your bank details to receive money",
    "Your password will expire click this link",
    "Limited offer claim your free money now",
    "Verify your identity immediately",
    "Your account will be suspended click here",
    "You are selected for a cash prize",

    "Hello, please find the meeting notes attached",
    "Your college timetable has been updated",
    "Thank you for attending our meeting",
    "Your order has been delivered successfully",
    "Please submit your assignment by Monday",
    "Here is the project report you requested",
    "Your appointment is confirmed for tomorrow",
    "The class will begin at ten AM",
    "Please review the attached document",
    "Thank you for your purchase",
    "Your exam results are now available",
    "We look forward to seeing you tomorrow"
]

labels = [
    "Phishing", "Phishing", "Phishing", "Phishing",
    "Phishing", "Phishing", "Phishing", "Phishing",
    "Phishing", "Phishing", "Phishing", "Phishing",
    "Legitimate", "Legitimate", "Legitimate", "Legitimate",
    "Legitimate", "Legitimate", "Legitimate", "Legitimate",
    "Legitimate", "Legitimate", "Legitimate", "Legitimate"
]

# Create machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

# Train the model
model.fit(emails, labels)

# Create model folder
os.makedirs("model", exist_ok=True)

# Save trained model
with open("model/phishing_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("AI model trained successfully!")
print("Model saved inside model folder.")
