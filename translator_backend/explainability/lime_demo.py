import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from lime.lime_text import LimeTextExplainer

# Sample training data
texts = [
    "I love this product",
    "This is amazing",
    "Worst experience ever",
    "I hate this",
    "Really good item",
    "Terrible quality"
]
labels = [1, 1, 0, 0, 1, 0]   # 1 = positive, 0 = negative

# Pipeline: TF-IDF + Logistic Regression
model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression()
)

# Train
model.fit(texts, labels)

# LIME Text Explainer
explainer = LimeTextExplainer(class_names=["Negative", "Positive"])

# FIX: Wrap model.predict_proba into proper function
def classifier_fn(sentence_list):
    """
    LIME sends a list of strings.
    Model expects TF-IDF transformed 2D matrix.
    Pipeline already handles this automatically.
    """
    return model.predict_proba(sentence_list)

# Explain prediction
sample_text = "I really love this product"
exp = explainer.explain_instance(
    sample_text,
    classifier_fn,
    num_features=5
)

# Save HTML
exp.save_to_file("lime_output.html")
print("LIME explanation generated: lime_output.html")
