# explainability/shap_demo.py

import shap
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Sample training data
texts = [
    "I love this product",
    "This is amazing",
    "I hate this",
    "This is terrible",
    "I really like it",
    "Worst experience ever"
]

labels = [1, 1, 0, 0, 1, 0]   # 1 = Positive, 0 = Negative

# Vectorize text
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# Train a simple classifier
model = LogisticRegression()
model.fit(X, labels)

# SHAP explainability
explainer = shap.Explainer(model.predict_proba, X.toarray())
shap_values = explainer(X.toarray())

# Summary plot
shap.summary_plot(
    shap_values[:,:,1], 
    X.toarray(), 
    feature_names=vectorizer.get_feature_names_out()
)
